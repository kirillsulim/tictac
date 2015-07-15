var Game = Backbone.Model.extend({
  urlRoot: '/game',
  idAttribute: 'pk',
  getMessageForPlayer: function(player_pk) {
    var x_player = this.get('x_player');
    var o_player = this.get('o_player');
    var state = this.get('state');

    var me;
    if(player_pk == x_player) {
      me = 'X';
    }
    else if(player_pk === o_player) {
      me = 'O';
    }
    else {
      me = '';
    }

    var message;
    if((state == 'XW' && me == 'X') || (state == 'OW' && me == 'O')) {
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
    else if((state == 'XP' && me == 'X') || (state == 'OP' && me == 'O')) {
      message = 'Your turn.';
    }
    else {
      message = "??????";
    }
    return message;
  },
});

module.exports = Game;
