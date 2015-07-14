$(function() {
  var Player = Backbone.Model.extend({
  });

  var Game = Backbone.Model.extend({
  });

  var Invite = Backbone.Model.extend({
  });

  var Move = Backbone.Model.extend({
  });

  var Router = Backbone.Router.extend({
    views: {},
    user: undefined,
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
    start: function() {
      $.get('/rest-auth/user/').
        done(function(data){
          window.router.user = data;
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
      $('.nav').hide();
      $('#start').show();
      $('#register').show();
    },
    login: function() {
      if(!this.views.login) {
        this.views.login = new LoginView();
        this.views.login.render();
      }
      $('.part').hide();
      $('.nav').hide();
      $('#start').show();
      $('#login').show();
    },
    players: function() {
      if(!window.router.user) {
        window.router.navigate('start', {trigger: true});
      }
      if(!this.views.players) {
        this.views.players = new PlayersView();
        this.views.players.render();
      }
      $('.part').hide();
      $('.nav').show();
      $('#players').show();
    },
    invites: function() {
      if(!window.router.user) {
        window.router.navigate('start', {trigger: true});
      }
      if(!this.views.invites) {
        this.views.invites = new InvitesView();
        this.views.invites.render();
      }
      $('.part').hide();
      $('.nav').show();
      $('#invites').show();
    },
    games: function() {
      if(!window.router.user) {
        window.router.navigate('start', {trigger: true});
      }
      if(!this.views.games) {
        this.views.games = new GamesView();
        this.views.games.render();
      }
      $('.part').hide();
      $('.nav').show();
      $('#games').show();
    },
    game: function(id) {
      if(!window.router.user) {
        window.router.navigate('start', {trigger: true});
      }
      if(!this.views.game) {
        this.views.game = new GameView();
      }
      this.views.game.render(id);

      $('.part').hide();
      $('.nav').show();
      $('#game').show();
    },
    logout: function() {
      $.post('/rest-auth/logout/');
      window.router.navigate('start', {trigger: true});
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

  var Players = Backbone.Collection.extend({
    model: Player,
    url: '/players',
  });

  var players = new Players();
  var PlayersView = Backbone.View.extend({
    el: $('#players'),
    template: _.template($('#_players').html()),
    render: function() {
      var self = this;
      players.fetch().done(function() {
        $(self.el).html(self.template({plList: players.models}));
      });
    },
    events: {
      'click .invite': 'invite'
    },
    invite: function(e) {
      var id = $(e.target).data('player-id');
      $.post('/invites', {
        from_player: window.router.user.pk,
        to_player: id,
        state: 'I'
      }).done(function(){
        console.log('done');
      }).fail(function(){
        console.log('fail');
      });
    }
  });

  var Invites = Backbone.Collection.extend({
    model: Invite,
    url: '/invites',
  });

  var invites = new Invites();
  var InvitesView = Backbone.View.extend({
    el: $('#invites'),
    template: _.template($('#_invites').html()),
    render: function() {
      var self = this;
      invites.fetch().done(function() {
        $(self.el).html(self.template({inviteList: invites.models}));
      });
    },
    events: {
      'click .accept': 'accept',
      'click .decline': 'decline'
    },
    accept: function(e) {
      var id = $(e.target).data('invite-id');
      $.put('/invite/' + id, {
        pk: id,
        state: 'A'
      }).done(function(){
        console.log('dione');
      }).fail(function(){
        console.log('foile');
      });
    },
    decline: function(e) {
      var id = $(e.target).data('invite-id');
      $.put('/invite/' + id, {
        pk: id,
        state: 'D'
      }).done(function(){
        console.log('dione');
      }).fail(function(){
        console.log('foile');
      });
    }
  });

  var Games = Backbone.Collection.extend({
    model: Game,
    url: '/games'
  });

  var games = new Games();
  var GamesView = Backbone.View.extend({
    el: $('#games'),
    template: _.template($('#_games').html()),
    render: function() {
      var self = this;
      games.fetch().done(function() {
        $(self.el).html(self.template({games: games.models}));
      });
    },
    events: {
      'click .to-game': 'toGame'
    },
    toGame: function(e){
      var id = $(e.target).data('game-id');
      window.router.navigate('game/' + id, {trigger: true});
    }
  });

  var GameView = Backbone.View.extend({
    el: $('#game'),
    template: _.template($('#_game').html()),
    game_id: undefined,
    render: function(id) {
      if(id) {
        game_id = id;
      } else {
        id = game_id;
      }
      var self = this;
      games.fetch().done(function() {
        var game = games.findWhere({pk: parseInt(id)});
        var map = {};
        var x_player = game.get('x_player');
        var o_player = game.get('o_player');
        _.each(game.get('moves'), function(m){
          var s;
          if(m.player == x_player) {
            s = 'X';
          }
          else if(m.player == o_player) {
            s = 'O';
          }
          map[m.code] = s;
        });
        console.log(map);
        $(self.el).html(self.template({game: game, map: map}));
      });
      setTimeout(this.render.bind(this), 1000);
    },
    events: {
      'click .tile': 'move'
    },
    move: function(e) {
      var self = this;
      var code = $(e.target).data('code');
      $.post('/move', {
        for_game: game_id,
        code: code
      }).done(function(){
        self.render();
      }).fail(function(e){
        console.log('ERROR!' + e);
      });
    }
  });

  window.router = new Router();
  Backbone.history.start();
});
