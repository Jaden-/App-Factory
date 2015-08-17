jewel.input = (function() {
  var inputHandlers;
  var controls = {
    // keyboard
    KEY_UP: 'moveUp',
    KEY_LEFT: 'moveLeft',
    KEY_DOWN: 'moveDown',
    KEY_RIGHT: 'moveRight',
    KEY_ENTER: 'selectJewel',
    KEY_SPACE: 'selectJewel',

    // mouse and touch
    CLICK: 'selectJewel',
    TOUCH: 'selectJewel',

    // gamepad
    BUTTON_A: 'selectJewel',
    LEFT_STICK_UP: 'moveUp',
    LEFT_STICK_DOWN:'moveDown',
    LEFT_STICK_LEFT: 'moveLeft',
    LEFT_STICK_RIGHT:'moveRight'
  };
  var keys = {
    37: 'KEY_LEFT',
    38: 'KEY_UP',
    39: 'KEY_RIGHT',
    40: 'KEY_DOWN',
    13: 'KEY_ENTER',
    32: 'KEY_SPACE',
    65: 'KEY_A',
    66: 'KEY_B',
    67: 'KEY_C'
  };

  function initialize() {
    var dom = jewel.dom,
        $ = dom.$,
        board = $('#game-screen .game-board')[0];

    inputHandlers = {};
    dom.bind(board, 'mousedown', function(event) {
      handleClick(event, 'CLICK', event);
    });

    dom.bind(board, 'touchstart', function(event) {
      handleClick(event, 'TOUCH', event.targetTouches[0]);
    });

    dom.bind(document, 'keydown', function(event) {
      var keyName = keys[event.keyCode]
      if(keyName && keys[keyName]) {
        event.preventDefault();
        trigger(controls[keyName]);
      }
    });
  }

  function handleClick(event, control, click) {
    // is any action bound to this input control?
    var settings = jewel.settings;
    var action = controls[control];
    if(!action) {
      return;
    }

    var board = jewel.dom.$('#game-screen .game-board')[0],
        rect = board.getBoundingClientRect(),
        relX, relY,
        jewelX, jewelY;

    // click position relative to board
    relX = click.clientX - rect.left;
    relY = click.clientY - rect.top;

    // jewel coordinates
    jewelX = Math.floor(relX / rect.width * settings.cols);
    jewelY = Math.floor(relY / rect.height * settings.rows);

    // trigger functions bound to action
    trigger(action, jewelX, jewelY);

    // prevent default click behavior
    event.preventDefault();
  }

  function bind(action, handler) {
    if(!inputHandlers[action]) {
      inputHandlers[action] = [];
    }
    inputHandlers[action].push(handler);
  }

  function trigger(action) {
    var handlers = inputHandlers[action],
        args = Array.prototype.slice.call(arguments, 1);
    if(handlers) {
      for(var i = 0; i<handlers.length; i++) {
        handlers[i].apply(null, args);
      }
    }
  }

  return {
    initialize: initialize,
    bind: bind
  }

})();
