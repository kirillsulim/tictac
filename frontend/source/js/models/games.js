var Game = require('./game');

var Games = Backbone.Collection.extend({
  model: Game,
  url: '/games'
});

module.exports = Games;
