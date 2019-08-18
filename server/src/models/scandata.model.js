// See https://vincit.github.io/objection.js/#models
// for more of what you can do here.
const { Model } = require('objection');

class scandata extends Model {

  static get tableName() {
    return 'scandata';
  }
  static get idColumn() {
    return 'Id';
  }

  $beforeInsert() {
    this.ScanTime = new Date().toISOString();
  }

}

module.exports = function (app) {

  return scandata;
};
