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
    var self = this;
    if(id) {
      game_id = parseInt(id);
      this.app.games.fetch().done(function() {
        var game = self.app.games.findWhere({pk: game_id});
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
          var message = game.getMessageForPlayer(self.app.user.pk);
        });
        $(self.el).html(self.template({
          game: game,
          map: map,
          message: message,
        }));
      });
      setTimeout(this.render.bind(this), 1000);
    } else {
      var game = this.app.games.findWhere({pk: game_id});
      game.fetch().done(function(){
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
        var message = game.getMessageForPlayer(self.app.user.pk);

        $(self.el).html(self.template({
          game: game,
          map: map,
          message: message,
        }));
      });
      setTimeout(this.render.bind(this), 1000);
    }
  },
  _getMessage: function(state, me) {
    var message;
    if((state == 'XW' && me == 'X') || (state == 'OW' && me == 'Y')) {
      message = 'You win!';
    }
    else if((state == 'XW' && me == 'O') || (state == 'OW' && me == 'X')) {
      message = 'You lose :-(';
    }
    else if(state == 'TT') {
      message = 'Tie.';
    }
    else if((state == 'XP' && me == 'O') || (state == 'OP' && me == 'X')) {
      message = 'Opponent turn.';
    }
    else if((state == 'XP' && me == 'X') || (state == 'OP' && me == 'Y')) {
      message = 'Your turn.';
    }
    return message;
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
