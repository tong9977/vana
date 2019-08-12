const feathers = require('@feathersjs/feathers');
const configuration = require('@feathersjs/configuration');
let conf = configuration();
let app = feathers().configure(conf);

module.exports = function (options = {}) {
  return  function uploadRes(req, res, next) {
    const baseUploadUrl = app.get('uploadResources');


    let output = req.files.map((item) => {

      let url = baseUploadUrl + item.path.replace('public/uploads/', '')
      return {
        ...item,
        url: url
      }
    })

    res.json(output);
  };
};
