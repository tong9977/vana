const assert = require('assert');
const app = require('../../src/app');

describe('\'camera\' service', () => {
  it('registered the service', () => {
    const service = app.service('camera');

    assert.ok(service, 'Registered the service');
  });
});
