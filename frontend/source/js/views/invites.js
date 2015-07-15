var InvitesView = Backbone.View.extend({
  initialize: function(opt) {
    this.app = opt.app;
  },
  el: $('#invites'),
  template: function(data) {
    return _.template($('#_invites').html())(data);
  },
  render: function() {
    var self = this;
    this.app.invites.fetch().done(function() {
      $(self.el).html(self.template({invites: self.app.invites.models}));
    });
  },
  events: {
    'click .accept': 'accept',
    'click .decline': 'decline'
  },
  accept: function(e) {
    var id = $(e.target).data('invite-id');
    $.put('/invite/' + id, {
      pk: id,
      state: 'A'
    }).done(function(){
      console.log('dione');
    }).fail(function(){
      console.log('foile');
    });
  },
  decline: function(e) {
    var id = $(e.target).data('invite-id');
    $.put('/invite/' + id, {
      pk: id,
      state: 'D'
    }).done(function(){
      console.log('dione');
    }).fail(function(){
      console.log('foile');
    });
  }
});

module.exports = InvitesView;
