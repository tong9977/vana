const photo = require('./photo/photo.service.js');
// eslint-disable-next-line no-unused-vars
module.exports = function (app) {
  app.configure(photo);
};
