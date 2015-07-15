var LoginView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#login'),
  template: function(data) {
    return _.template($('#_login').html())(data);
  },

  render: function() {
    $(this.el).html(this.template());
  },
  events: {
    'click #do-login': 'doLogin'
  },
  doLogin: function() {
    var username = $('#username').val();
    var pass = $('#password').val();

    $.post('/rest-auth/login/', {
      username: username,
      password: pass
    }).done(function() {
      window.router.navigate('start', {trigger: true});
    }).fail(function() {
    });
  }
});

module.exports = LoginView;
