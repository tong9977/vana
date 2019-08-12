// See https://vincit.github.io/objection.js/#models
// for more of what you can do here.
const { Model } = require('objection');

class photo extends Model {

  static get tableName() {
    return 'photo';
  }
  static get idColumn() {
    return 'Id';
  }
}

module.exports = function (app) {

  return photo;
};
