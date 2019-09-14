/* eslint-disable no-unused-vars */
const { NotFound, GeneralError, BadRequest } = require('@feathersjs/errors');

class Service {
  constructor(options) {
    this.options = options || {};
  }

  async patch(id, data, params) {
    const cmd = id

    if (cmd == "IsTaken") {
      const result = this.execIsTaken(data);
      return result
    }

    return new NotFound('Command Not Found');

  }

  async execIsTaken(data) {
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
}

module.exports = function (options) {
  return new Service(options);
};

module.exports.Service = Service;
