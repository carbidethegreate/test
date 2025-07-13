// Requires: none (uses built-in fetch)
import { readFile, writeFile } from 'fs/promises';
import { Buffer } from 'buffer';

const { OPENAI_API_KEY, CF_API_TOKEN, CF_ACCOUNT_ID } = process.env;

if (!OPENAI_API_KEY || !CF_API_TOKEN || !CF_ACCOUNT_ID) {
  console.error('Missing required environment variables');
  process.exit(1);
}

async function failOnBadStatus(resp) {
  if (!resp.ok) {
    const text = await resp.text();
    console.error(text);
    process.exit(1);
  }
}

async function main() {
  const images = JSON.parse(await readFile('images.json', 'utf8'));
  const result = {};

  for (const item of images) {
    const { label, prompt, size } = item;
    // generate with OpenAI
    const aiResp = await fetch('https://api.openai.com/v1/images/generations', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt, n: 1, size, response_format: 'b64_json' })
    });
    await failOnBadStatus(aiResp);
    const aiData = await aiResp.json();
    const b64 = aiData.data[0].b64_json;
    const buffer = Buffer.from(b64, 'base64');

    const form = new FormData();
    form.append('file', new Blob([buffer], { type: 'image/png' }), `${label}.png`);
    form.append('requireSignedURLs', 'false');
    form.append('id', label);

    const upResp = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/images/v1`,
      {
        method: 'POST',
        headers: { Authorization: `Bearer ${CF_API_TOKEN}` },
        body: form
      }
    );
    await failOnBadStatus(upResp);
    const upData = await upResp.json();
    const url = upData.result.variants[0];
    result[label] = url;
  }

  await writeFile('image_map.json', JSON.stringify(result, null, 2));
  console.log('UPLOAD OK');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
