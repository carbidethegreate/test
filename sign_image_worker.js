const KEY = "YOUR_KEY_FROM_IMAGES_DASHBOARD"; // replace via Wrangler secret
const EXPIRATION = 60 * 60 * 24; // 1 day

const bufferToHex = (buffer) =>
  [...new Uint8Array(buffer)]
    .map((x) => x.toString(16).padStart(2, "0"))
    .join("");

async function generateSignedUrl(url) {
  const encoder = new TextEncoder();
  const secretKeyData = encoder.encode(KEY);
  const key = await crypto.subtle.importKey(
    "raw",
    secretKeyData,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const expiry = Math.floor(Date.now() / 1000) + EXPIRATION;
  url.searchParams.set("exp", expiry);
  const stringToSign = url.pathname + "?" + url.searchParams.toString();
  const mac = await crypto.subtle.sign(
    "HMAC",
    key,
    encoder.encode(stringToSign),
  );
  const sig = bufferToHex(mac);
  url.searchParams.set("sig", sig);
  return new Response(url);
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const imageDeliveryURL = new URL(
      url.pathname.slice(1).replace("https:/imagedelivery.net", "https://imagedelivery.net"),
    );
    return generateSignedUrl(imageDeliveryURL);
  },
};
