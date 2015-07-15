var NavView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#nav'),
  template: function(data) {
    return _.template($('#_nav').html())(data);
  },
  render: function() {
    $(this.el).html(this.template());
  },
});

module.exports = NavView;
