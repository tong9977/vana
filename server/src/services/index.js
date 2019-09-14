const photo = require('./photo/photo.service.js');
const scandata = require('./scandata/scandata.service.js');
const camera = require('./camera/camera.service.js');
// eslint-disable-next-line no-unused-vars
module.exports = function (app) {
  app.configure(photo);
  app.configure(scandata);
  app.configure(camera);
};
