var GameView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#game'),
  template: function(data) {
    return _.template($('#_game').html())(data);
  },
  game_id: undefined,
  render: function(id) {
    if(id) {
      game_id = id;
    } else {
      id = game_id;
    }
    var self = this;
    if(games) {
      this.app.games.fetch().done(function() {
        var game = self.app.games.findWhere({pk: parseInt(id)});
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
    }
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

module.exports = GameView;
