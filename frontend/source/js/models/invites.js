var Invite = require('./invite');

var Invites = Backbone.Collection.extend({
  model: Invite,
  url: '/invites',
});

module.exports = Invites;
