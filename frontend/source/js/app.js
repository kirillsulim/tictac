var Players = require('./models/players');
var Games = require('./models/games');
var Invites = require('./models/invites');

var Router = require('./router');


$(function() {
  var app = {};
  app.players = new Players({app: app});
  app.invites = new Invites({app: app});
  app.games = new Games({app: app});

  setInterval(function(){
    app.players.fetch();
  }, 1000 * 20);

  setInterval(function(){
    app.invites.fetch();
  }, 1000 * 10);

  setInterval(function(){
    app.games.fetch();
  }, 1000 * 1);

  app.router = new Router({app: app});
  Backbone.history.start();
});
