var Players = require('./models/players');
var Games = require('./models/games');
var Invites = require('./models/invites');

var Router = require('./router');


var en_text = {
  'YOU_WIN': 'You win!',
  'YOU_LOSE': 'You lose :-(',
  'TIE': 'Tie.',
  'OP_TURN': 'Opponent turn.',
  'YOUR_TURN': 'Your turn.',

  'INVITES': 'Invites',
  'GAMES': 'Games',
  'PLAYERS': 'Players',

  'TO_GAME': 'To game',
  'ACCEPT': 'Accept',
  'DECLINE': 'Decline',
  'INVITE': 'Invite',

  'USERNAME': 'Username',
  'PASSWORD': 'Password',
  'PASSWORD2': 'Retype password',
  'LOGIN': 'Login',
  'LOG_IN': 'Log in!',
  'REGISTER': 'Register',
  'LOGOUT': 'Logout',

  '?': '??????',
};

var ru_text = {
  'YOU_WIN': 'Вы выиграли!',
  'YOU_LOSE': 'Вы проиграли :-(',
  'TIE': 'Ничья.',
  'OP_TURN': 'Ход противника.',
  'YOUR_TURN': 'Ваш ход.',

  'INVITES': 'Вызовы',
  'GAMES': 'Игры',
  'PLAYERS': 'Игроки',

  'TO_GAME': 'К игре',
  'ACCEPT': 'Принять',
  'DECLINE': 'Отклонить',
  'INVITE': 'На дуэль!',

  'USERNAME': 'Пользователь',
  'PASSWORD': 'Пароль',
  'PASSWORD2': 'Повторить пароль',
  'LOGIN': 'Войти',
  'LOG_IN': 'Войти',
  'REGISTER': 'Зарегистрироваться',
  'LOGOUT': 'Выйти',

  '?': '??????',

};

$(function() {
  app = {};

  app.lang = 'ru';
  app.text = function(message) {
    var res;
    if(this.lang == 'ru') {
      res = ru_text[message];
    }
    else if(this.lang == 'en') {
      res = en_text[message];
    }
    if(!res) {
      return 'Error! Cant find ' + message;
    }
    else {
      return res;
    }
  };

  app.players = new Players({app: app});
  app.invites = new Invites({app: app});
  app.games = new Games({app: app});

  setInterval(function(){
    app.players.fetch().done(function(){
      var v = app.router.views.players;
      if(v) {
        v.render();
      }
    });
  }, 1000 * 20);

  setInterval(function(){
    app.invites.fetch().done(function(){
      var v = app.router.views.players;
      if(v) {
        v.render();
      }
    });
  }, 1000 * 10);

  setInterval(function(){
    app.games.fetch().done(function(){
      var v = app.router.views.games;
      if(v) {
        v.render();
      }
    });
  }, 1000 * 2);

  app.router = new Router({app: app});
  Backbone.history.start();
});
