var GamesView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#games'),
  template: function(data) {
    return _.template($('#_games').html())(data);
  },
  render: function() {
    var self = this;
    this.app.games.fetch().done(function() {
      $(self.el).html(self.template({
        games: self.app.games.models,
        player_pk: self.app.user.pk,
      }));
    });
  },
  events: {
    'click .to-game': 'toGame'
  },
  toGame: function(e){
    var id = $(e.target).data('game-id');
    this.app.router.navigate('game/' + id, {trigger: true});
  }
});

module.exports = GamesView;
