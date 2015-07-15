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
      message = 'YOU_WIN';
    }
    else if((state == 'XW' && me == 'O') || (state == 'OW' && me == 'X')) {
      message = 'YOU_LOSE';
    }
    else if(state == 'TT') {
      message = 'TIE';
    }
    else if((state == 'XP' && me == 'O') || (state == 'OP' && me == 'X')) {
      message = 'OP_TURN';
    }
    else if((state == 'XP' && me == 'X') || (state == 'OP' && me == 'O')) {
      message = 'YOUR_TURN';
    }
    else {
      message = '?';
    }
    return message;
  },
  getOpponentPk: function(player_pk){
    var x_player = this.get('x_player');
    var o_player = this.get('o_player');

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
    var op_pk = me == 'X'? o_player : x_player;
    return op_pk;
  }
});

module.exports = Game;
