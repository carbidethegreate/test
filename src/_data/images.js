const fs = require('fs');
module.exports = JSON.parse(fs.readFileSync('image_map.json'));
