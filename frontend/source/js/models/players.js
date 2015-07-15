var Player = require('./player');

var Players = Backbone.Collection.extend({
  model: Player,
  url: '/players',
});

module.exports = Players;
