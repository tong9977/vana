/* eslint-disable no-unused-vars */
const { NotFound, GeneralError, BadRequest } = require('@feathersjs/errors');

class Service {
  constructor(options) {
    this.options = options || {};
  }

  async patch(id, data, params) {
    const cmd = id

    if (cmd == "IsTaken") {
      const result = this.IsTaken(data);
      return result
    }

    if (cmd == "ClearScanData") {
      const result = this.ClearScanData(data);
      return result
    }

    return new NotFound('Command Not Found');

  }

  async IsTaken(data) {
    const Station = data.Station;
    const ScanUnixtime = data.ScanUnixtime;

    const photo = require('../../models/photo.model')();
    const takenphoto = await photo.query()
      .where('Station', '=', Station)
      .where('UnixTime', '>', ScanUnixtime)

    console.log(takenphoto.length)

    if (takenphoto.length > 0) {
      return { Taken: true };
    } else {
      return { Taken: false };
    }
  }
  async ClearScanData(data) {
    return {}
  }
}

module.exports = function (options) {
  return new Service(options);
};

module.exports.Service = Service;
