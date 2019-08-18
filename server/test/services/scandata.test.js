const assert = require('assert');
const app = require('../../src/app');

describe('\'scandata\' service', () => {
  it('registered the service', () => {
    const service = app.service('scandata');

    assert.ok(service, 'Registered the service');
  });
});
