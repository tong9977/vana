/* eslint-disable no-unused-vars */
const { NotFound, GeneralError, BadRequest } = require('@feathersjs/errors');

class Service {
  constructor(options) {
    this.options = options || {};
  }

  async patch(id, data, params) {
    const cmd = id

    if (cmd == "IsTaken") { return this.IsTaken(data); }
    if (cmd == "ClearScanData") { return this.ClearScanData(data); }
    if (cmd == "RFIDWaitInQueue") { return this.RFIDWaitInQueue(data); }

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
  async RFIDWaitInQueue(data) {
    const scandata = require('../../models/scandata.model')();
    const now = (+new Date()) / 1000;
    const station = data.Station

    const rfidInQueue = await scandata.query()
      .where('UnixTime', '<', now)
      .where('UnixTime', '>', now - 60)
      .where('Station', '=', station)
      .where('SetNo', '=', '')

    return { RFIDWaitInQueue: rfidInQueue.length }
  }
}

module.exports = function (options) {
  return new Service(options);
};

module.exports.Service = Service;
