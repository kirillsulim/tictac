var GameView = require('./views/game');
var PlayersView = require('./views/players');
var LoginView = require('./views/login');
var RegisterView = require('./views/register');
var InvitesView = require('./views/invites');
var GamesView = require('./views/games');
var NavView = require('./views/nav');
var LangView = require('./views/lang');


var Router = Backbone.Router.extend({
  initialize: function(opt) {
    this.app = opt.app;
    this.views.nav = new NavView({app: this.app});
    this.views.nav.render();
    this.views.lang = new LangView({app: this.app});
    this.views.lang.render();
  },
  views: {},
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
    var self = this;
    $.get('/rest-auth/user/').
      done(function(data){
        self.app.user = data;
        self.navigate('players', {trigger: true});
      }).
      fail(function(){
        self.navigate('login', {trigger: true});
      });
  },
  register: function() {
    if(!this.views.register) {
      this.views.register = new RegisterView({app: this.app});
    }
    this.views.register.render();
    $('.part').hide();
    $('.nav').hide();
    $('#start').show();
    $('#register').show();
  },
  login: function() {
    if(!this.views.login) {
      this.views.login = new LoginView({app: this.app});
    }
    this.views.login.render();
    $('.part').hide();
    $('.nav').hide();
    $('#start').show();
    $('#login').show();
  },
  players: function() {
    if(!this.app.user) {
      this.navigate('start', {trigger: true});
    }
    if(!this.views.players) {
      this.views.players = new PlayersView({app: this.app});
    }
    this.views.players.render();
    $('.part').hide();
    $('.nav').show();
    $('#players').show();
  },
  invites: function() {
    if(!this.app.user) {
      this.navigate('start', {trigger: true});
    }
    if(!this.views.invites) {
      this.views.invites = new InvitesView({app: this.app});
    }
    this.views.invites.render();
    $('.part').hide();
    $('.nav').show();
    $('#invites').show();
  },
  games: function() {
    if(!this.app.user) {
      this.navigate('start', {trigger: true});
    }
    if(!this.views.games) {
      this.views.games = new GamesView({app: this.app});
    }
    this.views.games.render();
    $('.part').hide();
    $('.nav').show();
    $('#games').show();
  },
  game: function(id) {
    if(!this.app.user) {
      this.navigate('start', {trigger: true});
    }
    if(!this.views.game) {
      this.views.game = new GameView({app: this.app});
    }
    this.views.game.render(id);
    $('.part').hide();
    $('.nav').show();
    $('#game').show();
  },
  logout: function() {
    var self = this;
    $.post('/rest-auth/logout/').done(function(){
      self.app.user = undefined;
      self.navigate('start', {trigger: true});
    });
  }
});

module.exports = Router;
