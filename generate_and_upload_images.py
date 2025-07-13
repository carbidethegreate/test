import os
import json
import requests
from pathlib import Path
import tempfile
import sys

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
        size = item["size"]

        # Generate image via OpenAI
        ai_resp = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"prompt": prompt, "n": 1, "size": size, "response_format": "url"},
        )
        fail_on_bad_status(ai_resp)
        image_url = ai_resp.json()["data"][0]["url"]

        # Download image to temp file
        img_resp = requests.get(image_url)
        fail_on_bad_status(img_resp)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(img_resp.content)
            temp_path = tmp.name

        # Upload to Cloudflare Images
        with open(temp_path, "rb") as f:
            cf_resp = requests.post(
                f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/images/v1",
                headers={"Authorization": f"Bearer {CF_API_TOKEN}"},
                data={"requireSignedURLs": "false"},
                files={"file": f},
            )
        os.unlink(temp_path)
        fail_on_bad_status(cf_resp)
        result[label] = cf_resp.json()["result"]["variants"][0]

    OUTPUT_FILE.write_text(json.dumps(result, indent=2))
    print("UPLOAD OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
