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

    const dir = storagePath + '/' + year + '/' + month + '/' + day + '/' + station + '/' + size;

    mkdirp(dir, err => cb(err, dir));
  },
  filename: (req, file, cb) => {
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

const savetodb = async (req, res, next) => {
  const baseUploadUrl = app.get('uploadResources');

  var takenUnixTime = parseInt(req.query.unixtime);
  var station = req.query.station;
  var size = req.query.size;
  var setno = req.query.setno;
  var takendate = new Date(takenUnixTime * 1000);

  let files = req.files;
  const photo = require('../models/photo.model')();
  const scandata = require('../models/scandata.model')();

  var rfidString = '';

  if (size == 's') {
    // size s หา rfid โดยการดูจากเวลา scandata ว่ามีการ  scan ก่อนถ่าย 1 นาทีหรือไม่ และ SetNo ต้องเป็นค่าว่างด้วย   
    const owner_scandata = await scandata.query()
      .where('UnixTime', '<', takenUnixTime)
      .where('UnixTime', '>', takenUnixTime - 60)
      .where('Station','=',station)
      .where('SetNo', '=', '')

    if (owner_scandata.length > 0) {
      console.log(owner_scandata);

      rfidString = owner_scandata[0].TagNo;
      //เจอแล้ว ให้เอา SetNo ขาก Photo ไปใส่ใน scandata ที่เจอเพื่อบอกว่า scandata นี้เจอรูปแล้ว
      const candataUpdated = await scandata.query()
        .findById(owner_scandata[0].Id)
        .patch({
          SetNo: setno,
          TakenUnixTime: takenUnixTime
        })

    }

  } else {
    // size m l 
    // เอา rfid จาก scandata จาก SetNo ที่ตรงกันกับ Photo ที่ส่งมา

  }


  files.forEach(async (item) => {
    var newphoto = await photo.query().insert({
      Station: station,
      SetNo: setno,
      Unixtime: takenUnixTime,
      TakenTime: takendate.toISOString(),
      Size: size,
      Url: baseUploadUrl + item.path.replace('public/uploads/', ''),
      LocalPath: item.path,
      RFIDString: rfidString
    });
  });

  next();
}

// eslint-disable-next-line no-unused-vars
module.exports = function (app) {
  app.post('/upload', upload.array('files'), savetodb, uploadRes());
};
