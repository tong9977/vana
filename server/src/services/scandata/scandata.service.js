// Initializes the `scandata` service on path `/scandata`
const createService = require('feathers-objection');
const createModel = require('../../models/scandata.model');
const hooks = require('./scandata.hooks');

module.exports = function (app) {
  const Model = createModel(app);
  const paginate = app.get('paginate');

  const options = {
    model: Model,
    id:"Id",
    paginate
  };

  // Initialize our service with any options it requires
  app.use('/scandata', createService(options));

  // Get our initialized service so that we can register hooks and filters
  const service = app.service('scandata');

  service.hooks(hooks);
};
