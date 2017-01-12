import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    trade() {
      const symbol = this.get('symbol');
      const quantity = parseInt(this.get('quantity'));
      const price = parseInt(this.get('price'));
      const action = this.get('action');

      const data = {
        symbol,
        quantity,
        price,
        action
      };

      Ember.$.ajax({
        url: 'http://localhost:9090/api/trade',
        type: 'POST',
        data: JSON.stringify(data),
        contentType:"application/json; charset=utf-8",
        dataType: 'json'
      })
      .done(() => {
        // Refetch
        Ember.$.getJSON('http://localhost:9090/api/asi', data => {
          this.set('asi', data.all_share_index.toFixed(3));
        });

        Ember.$.getJSON('http://localhost:9090/api/stocks', data => {
          // this is not great, but in the interests of time
          data.forEach(s => {
            s.pe_ratio = s.pe_ratio ? s.pe_ratio.toFixed(3) : s.pe_ratio;
            s.price = s.price ? s.price.toFixed(3) : s.price;
            s.dividend_yield = s.dividend_yield ? s.dividend_yield.toFixed(3) : s.dividend_yield;
          });

          // clear form
          this.set('model', data);
          this.set('symbol', '');
          this.set('quantity', '');
          this.set('price', '');
          this.set('action', 'buy');
        });
        this.notify.success(`Trade complete for ${quantity} of ${symbol.toUpperCase()} @ ${price}`);
      })
      .fail((err) => this.notify.error(err.responseJSON.message));
    }
  }
});
