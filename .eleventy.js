const crypto = require('crypto');

function signUrl(url){
  const key = process.env.CF_IMAGE_DELIVERY_KEY;
  if(!key) return url;
  const u = new URL(url);
  const expiry = Math.floor(Date.now()/1000) + 60*60*24; // 1 day
  u.searchParams.set('exp', expiry);
  const toSign = u.pathname + '?' + u.searchParams.toString();
  const sig = crypto.createHmac('sha256', key).update(toSign).digest('hex');
  u.searchParams.set('sig', sig);
  return u.toString();
}

module.exports = function(eleventyConfig){
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addGlobalData("img", () => {
    const map = require("./image_map.json");
    return (label, alt) => `<img src="${signUrl(map[label])}" alt="${alt}" loading="lazy" width="100%">`;
  });
  eleventyConfig.addLayoutAlias("base", "layouts/base.njk");
  return {
    dir: {
      input: "src",
      includes: "_includes",
      output: "_site"
    }
  };
};
