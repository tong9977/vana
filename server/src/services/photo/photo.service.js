// Initializes the `photo` service on path `/photo`
const createService = require('feathers-objection');
const createModel = require('../../models/photo.model');
const hooks = require('./photo.hooks');

module.exports = function (app) {
  const Model = createModel(app);
  const paginate = app.get('paginate');

  const options = {
    model: Model,
    paginate
  };

  // Initialize our service with any options it requires
  app.use('/photo', createService(options));

  // Get our initialized service so that we can register hooks and filters
  const service = app.service('photo');

  service.hooks(hooks);
};
