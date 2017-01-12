import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return Ember.RSVP.hash({
      stocks: Ember.$.getJSON('http://localhost:9090/api/stocks'),
      asi: Ember.$.getJSON('http://localhost:9090/api/asi')
    });
  },
  setupController: function(controller, model) {
    // this is not great, but in the interests of time
    model.stocks.forEach(s => {
      s.pe_ratio = s.pe_ratio ? s.pe_ratio.toFixed(3) : s.pe_ratio;
      s.price = s.price ? s.price.toFixed(3) : s.price;
      s.dividend_yield = s.dividend_yield ? s.dividend_yield.toFixed(3) : s.dividend_yield;
    });
    controller.set('model', model.stocks);
    controller.set('asi', model.asi.all_share_index.toFixed(3));
    controller.set('action', 'buy');
  }
});
