$(function() {
  var User = Backbone.Model.extend({
  });

  var Game = Backbone.Model.extend({
  });

  var Invite = Backbone.Model.extend({
  });

  var Move = Backbone.Model.extend({
  });

  var Router = Backbone.Router.extend({
    routes: {
      '': 'start',
      'start': 'start',
      'players': 'players',
      'invites': 'invites',
      'games': 'games',
      'game/:id': 'game',
      'logout': 'logout',
      'login': 'login',
      'register': 'register'
    },
    views: {},
    user: undefined,
    start: function() {
      $.get('/rest-auth/user/').
        done(function(data){
          this.user = data;
          window.router.navigate('players', {trigger: true});
        }).
        fail(function(){
          window.router.navigate('login', {trigger: true});
        });
    },
    register: function() {
      if(!this.views.register) {
        this.views.register = new RegisterView();
        this.views.register.render();
      }
      $('.part').hide();
      $('#start').show();
      $('#register').show();
    },
    login: function() {
      if(!this.views.login) {
        this.views.login = new LoginView();
        this.views.login.render();
      }
      $('.part').hide();
      $('#start').show();
      $('#login').show();
    },
    players: function() {
      if(!this.views.players) {
        this.views.players = new PlayersView();
        this.views.players.render();
      }
      $('.part').hide();
      $('#players').show();
    },
    invites: function() {
      console.log('invites hitted');
    },
    games: function() {
      console.log('games hitted');
    },
    logout: function() {
      $.post('/rest-auth/logout/');
      this.start();
    }
  });

  var LoginView = Backbone.View.extend({
    el: $('#login'),
    template: _.template($('#_login').html()),
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

  var RegisterView = Backbone.View.extend({
    el: $('#register'),
    template: _.template($('#_register').html()),
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

  var PlayersView = Backbone.View.extend({
    el: $('#players'),
    template: _.template($('#_players').html()),
    render: function() {
      var self = this;
      var _players;
      $.get('/players').done(function(data){
        _players = data;
        console.log(data);
        console.log(_players);
      }).always(function(){
        console.log(_players);
        $(self.el).html(self.template({players: _players}));
      });
    }
  });

  var PlayerList = Backbone.Collection.extend({});

  var players = new PlayerList();




  window.router = new Router();
  Backbone.history.start();
});
