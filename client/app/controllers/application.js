import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    refresh() {
      console.log('REFRESH')
    },
    trade() {
      console.log('TRADE', this.get('symbol'))
      this.notify.info('Hello there!');
    }
  }
});
