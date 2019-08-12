const assert = require('assert');
const app = require('../../src/app');

describe('\'photo\' service', () => {
  it('registered the service', () => {
    const service = app.service('photo');

    assert.ok(service, 'Registered the service');
  });
});
