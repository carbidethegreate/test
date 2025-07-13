# Requires: requests pillow
import os
import json
import requests
from pathlib import Path
from io import BytesIO
import sys
from PIL import Image

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
CF_API_TOKEN = os.environ.get("CF_API_TOKEN")
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")

if not (OPENAI_API_KEY and CF_API_TOKEN and CF_ACCOUNT_ID):
    print("Missing required environment variables", file=sys.stderr)
    sys.exit(1)

IMAGES_FILE = Path("images.json")
OUTPUT_FILE = Path("image_map.json")


def fail_on_bad_status(resp: requests.Response):
    if resp.status_code != 200:
        print(resp.text, file=sys.stderr)
        sys.exit(1)


def main():
    images = json.loads(IMAGES_FILE.read_text())
    result = {}

    for item in images:
        label = item["label"]
        prompt = item["prompt"]

        # Generate base image via OpenAI (1024x1024 PNG)
        ai_resp = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"prompt": prompt, "n": 1, "size": "1024x1024", "response_format": "url"},
        )
        fail_on_bad_status(ai_resp)
        image_url = ai_resp.json()["data"][0]["url"]

        # Download and process the image
        img_resp = requests.get(image_url)
        fail_on_bad_status(img_resp)
        base_img = Image.open(BytesIO(img_resp.content))

        def upload_bytes(key: str, data: bytes, mime: str) -> str:
            resp = requests.post(
                f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/images/v1",
                headers={"Authorization": f"Bearer {CF_API_TOKEN}"},
                data={"requireSignedURLs": "false", "id": f"{label}-{key}"},
                files={"file": (f"{label}-{key}", data, mime)},
            )
            fail_on_bad_status(resp)
            return resp.json()["result"]["variants"][0]

        result[label] = {}
        # Upload original
        buffer = BytesIO()
        base_img.save(buffer, format="PNG")
        result[label]["orig"] = upload_bytes("orig", buffer.getvalue(), "image/png")

        sizes = {
            "og": (1200, 630),
            "hero": (1600, 900),
            "sm": (640, 640),
        }

        for key, sz in sizes.items():
            resized = base_img.resize(sz, Image.LANCZOS)
            buffer = BytesIO()
            if key == "sm":
                resized.save(buffer, format="PNG")
                mime = "image/png"
            else:
                resized.save(buffer, format="JPEG", quality=85)
                mime = "image/jpeg"
            result[label][key] = upload_bytes(key, buffer.getvalue(), mime)

    OUTPUT_FILE.write_text(json.dumps(result, indent=2))
    print("UPLOAD OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
