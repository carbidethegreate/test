module.exports = function(eleventyConfig){
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addGlobalData("img", () => {
    const map = require("./image_map.json");
    return (label, alt) => `<img src="${map[label]}" alt="${alt}" loading="lazy" width="100%">`;
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
