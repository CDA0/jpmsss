import Ember from 'ember';
import { moduleFor, test } from 'ember-qunit';

moduleFor('route:application', 'Unit | Route | application', {
  // Specify the other units that are required for this test.
  // needs: ['controller:foo']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});

test('it sets the controller', function(assert) {
  assert.expect(3);

  const controller = Ember.Object.create();
  const model = {
    stocks: [],
    asi: { all_share_index: 1 }
  };

  const route = this.subject();
  route.setupController(controller, model);

  assert.equal(controller.get('model'), model.stocks);
  assert.equal(controller.get('asi'), 1);
  assert.equal(controller.get('action'), 'buy');
});
