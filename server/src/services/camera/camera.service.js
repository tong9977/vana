// Initializes the `camera` service on path `/camera`
const createService = require('./camera.class.js');
const hooks = require('./camera.hooks');

module.exports = function (app) {
  
  const paginate = app.get('paginate');

  const options = {
    paginate
  };

  // Initialize our service with any options it requires
  app.use('/camera', createService(options));

  // Get our initialized service so that we can register hooks
  const service = app.service('camera');

  service.hooks(hooks);
};
