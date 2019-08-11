const uploadRes = require('./upload-res');
const multer = require('multer');
const path = require('path');
const crypto = require("crypto");
const mkdirp = require('mkdirp');

const feathers = require('@feathersjs/feathers');
const configuration = require('@feathersjs/configuration');
let conf = configuration();
let app = feathers().configure(conf);

const allowedExtentions = ['.png', '.PNG', '.jpeg', '.jpg', '.JPG']
const storagePath = app.get('uploadStoragePath')
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    //console.log(req.query);
    var unixtimestamp = parseInt(req.query.unixtime);
    var station = req.query.station;
    var size = req.query.size;

    // Convert timestamp to milliseconds
    var date = new Date(unixtimestamp * 1000);
    var year = date.getFullYear();
    var month = date.getMonth().toString().padStart(2, "0");
    var day = date.getDate().toString().padStart(2, "0");

    const dir = storagePath + '/'+ year +'/'+month+'/'+day+'/'+station+'/'+size;

    mkdirp(dir, err => cb(err, dir));
  },
  filename: (req, file, cb) => {    
    let id = crypto.randomBytes(2).toString('hex');
    let ext = path.extname(file.originalname);
    cb(null, `${file.originalname}`)
  }
});

const upload = multer({
  storage,
  limits: {
    fieldSize: 100 // 100 MB
  },
  fileFilter: (req, file, cb) => cb(null, allowedExtentions.includes(path.extname(file.originalname)))
});

// eslint-disable-next-line no-unused-vars
module.exports = function (app) {
  app.post('/upload', upload.array('files'), uploadRes());
};
