var PlayersView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#players'),
  template: function(data) {
    var d = _.template($('#_players').html())(data);
    return d;
  },

  render: function() {
    var self = this;
    this.app.players.fetch().done(function() {
      $(self.el).html(self.template({players: self.app.players.models}));
    });
  },
  events: {
    'click .invite': 'invite'
  },
  invite: function(e) {
    var id = $(e.target).data('player-id');
    $.post('/invites', {
      from_player: this.app.user.pk,
      to_player: id,
      state: 'I'
    }).done(function(){
      console.log('done');
    }).fail(function(){
      console.log('fail');
    });
  }
});

module.exports = PlayersView;
