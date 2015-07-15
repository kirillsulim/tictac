var RegisterView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#register'),
  template: function(data) {
    return _.template($('#_register').html())(data);
  },

  render: function() {
    $(this.el).html(this.template);
  },
  events: {
    'click #do-register': 'doRegister'
  },
  doRegister: function() {
    var username = $('#register #username').val();
    var pass1 = $('#register #password1').val();
    var pass2 = $('#register #password2').val();

    $.post('/rest-auth/registration/', {
      username: username,
      password1: pass1,
      password2: pass2
    }).done(function(){
      $.post('/rest-auth/login/', {
        username: username,
        password: pass1
      }).then(function(){
        window.router.navigate('start', {trigger: true});
      });
    }).fail(function(){
    });
  }
});

module.exports = RegisterView;
