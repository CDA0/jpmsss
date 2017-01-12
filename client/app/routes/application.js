import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return Ember.$.getJSON('http://localhost:9090/api/stocks');
  }
});
