# Gabriel Smith Webtie

This site is built with Eleventy and Cloudflare Pages. Images are generated with DALL·E and uploaded to Cloudflare Images.

## Quick start

1. Run the image pipeline:
   ```bash
   python generate_and_upload_images.py
   ```
2. Build the static site:
   ```bash
   npx @11ty/eleventy
   ```
3. Deploy the `_site` folder to Cloudflare Pages.
4. In your Pages project settings, set the environment variables `OPENAI_API_KEY`, `CF_API_TOKEN`, `CF_ACCOUNT_ID`, and `CF_IMAGE_DELIVERY_KEY` (for signing URLs).
5. Optionally deploy the `sign_image_worker.js` Worker to generate expiring URLs.
6. Purge the cache after the first deploy so new assets appear.
