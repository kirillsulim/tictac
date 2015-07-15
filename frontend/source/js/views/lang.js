var LangView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#lang'),
  template: function(data) {
    return _.template($('#_lang').html())(data);
  },
  render: function() {
    $(this.el).html(this.template());
  },
  events: {
    'click .lang-btn': 'switchLang'
  },
  switchLang: function(e) {
    var lang = $(e.target).data('lang-id');
    this.app.lang = lang;
    _.each(this.app.router.views, function(view) {
      view.render();
    });
  }
});

module.exports = LangView;
