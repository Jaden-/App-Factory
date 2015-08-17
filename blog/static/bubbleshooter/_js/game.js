console.log('game.js: creating var BubbleShoot');
var BubbleShoot = window.BubbleShoot || {};
BubbleShoot.Game = (function($) {
  var Game = function(){
    var curBubble;
    var board;
    var numBubbles;
    var bubbles = [];
    var requestAnimationID;
    var MAX_BUBBLES = 70;
    var POINTS_PER_BUBBLE = 50;
    var MAX_ROWS = 11;
    var level = 0;
    var score = 0;
    var highScore = 0;
    this.init = function() {
      console.log('Renderer: ' + BubbleShoot.Renderer);
      console.log(BubbleShoot.Renderer);
      if(BubbleShoot.Renderer) {
        console.log('game.js init() Renderer exists');
        BubbleShoot.Renderer.init(function() {
          $('.but_start_game').click('click', startGame);
        });
      } else {
        console.log('Starting regular Game.init');
        $('.but_start_game').bind('click', startGame);
      };
      if(window.localStorage && localStorage.getItem('high_score')) {
        highScore = parseInt(localStorage.getItem('high_score'));
      }
      BubbleShoot.ui.drawHighScore(highScore);
    };
    var startGame = function() {
      console.log('game.js: startGame');
      $('.but_start_game').unbind('click');
      $('#board .bubble').remove();
      numBubbles = MAX_BUBBLES - level * 5;
      BubbleShoot.ui.hideDialog();
      board = new BubbleShoot.Board();
      bubbles = board.getBubbles();
      if(BubbleShoot.Renderer) {
        // console.log('startGame() Renderer exists');
        if(!requestAnimationID) {
          // console.log('startGame() requestAnimationID exists');
          requestAnimationID = requestAnimationFrame(renderFrame);
        } else {
          // console.log('startGame() requestAnimationID does not exist. Drawing board.');
          BubbleShoot.ui.drawBoard(board);
        };
        curBubble = getNextBubble();
        $('#game').bind('click', clickGameScreen);
        BubbleShoot.ui.drawScore(score);
        BubbleShoot.ui.drawLevel(level);
      };
    };
    var renderFrame = function() {
      // console.log('game.js renderFrame()');
      $.each(bubbles, function() {
        if(this.getSprite().updateFrame)
          this.getSprite().updateFrame();
      });
      BubbleShoot.Renderer.render(bubbles);
      requestAnimationID = requestAnimationFrame(renderFrame);
    };

    var getNextBubble = function() {
      var bubble = BubbleShoot.Bubble.create();
      bubbles.push(bubble);
      bubble.setState(BubbleShoot.BubbleState.CURRENT);
      bubble.getSprite().addClass('cur_bubble');
      var top = 470;
      var left = ($('#board').width() - BubbleShoot.ui.BUBBLE_DIMS) / 2;
      bubble.getSprite().css({
        top: top,
        left: left
      });
      $('#board').append(bubble.getSprite());
      BubbleShoot.ui.drawBubblesRemaining(numBubbles);
      numBubbles--;
      return bubble;
    };

    var clickGameScreen = function(e) {
      var angle = BubbleShoot.ui.getBubbleAngle(curBubble.getSprite(), e);
      var duration = 750;
      var distance = 1000;
      var collision = BubbleShoot.CollisionDetector.findIntersection(curBubble, board, angle);

      if(collision) {
        var coords = collision.coords;
        duration = Math.round(duration * collision.distToCollision / distance);
        board.addBubble(curBubble, coords);
        var group = board.getGroup(curBubble, {});
        if(group.list.length >= 3) {
          popBubbles(group.list, duration);
          var topRow = board.getRows()[0];
          var topRowBubbles = [];
          for(var i = 0; i < topRow.length; i++) {
            if(topRow[i])
              topRowBubbles.push(topRow[i]);
          };
          if(topRowBubbles.length <= 5) {
            popBubbles(topRowBubbles, duration);
            group.list.concat(topRowBubbles);
          };
          var orphans = board.findOrphans();
          var delay = duration + 200 + 30 * group.list.length;
          dropBubbles(orphans, delay);
          var popped = [].concat(group.list, orphans);
          var points = popped.length * POINTS_PER_BUBBLE;
          score += points;
          setTimeout(function() {
            BubbleShoot.ui.drawScore(score);
          }, delay);
        };
      } else {
        var distX = Math.sin(angle) * distance;
        var distY = Math.cos(angle) * distance;
        var bubbleCoords = BubbleShoot.ui.getBubbleCoords(curBubble.getSprite());
        var coords = {
          x: bubbleCoords.left + distX,
          y: bubbleCoords.top - distY
        };
      }
      BubbleShoot.ui.fireBubble(curBubble, coords, duration);
      if(board.getRows().length > MAX_ROWS) {
        endGame(false);
      } else if(numBubbles == 0) {
        endGame(false);
      } else if(board.isEmpty()) {
        endGame(true);
      } else {
        curBubble = getNextBubble();
      }
    };
    var dropBubbles = function(bubbles, delay) {
      $.each(bubbles, function() {
        var bubble = this;
        board.popBubbleAt(bubble.getRow(), bubble.getCol());
        setTimeout(function() {
          bubble.setState(BubbleShoot.BubbleState.FALLING);
          bubble.getSprite().kaboom({
            callback: function() {
              bubble.getSprite().remove();
              bubble.setState(BubbleShoot.BubbleState.FALLEN);
            }
          })
        }, delay);
      });
      return;
    };

    var endGame = function(hasWon) {
      if(score > highScore) {
        highScore = score;
        $('#new_high_score').show();
        BubbleShoot.ui.drawHighScore(highScore);
        if(window.localStorage) {
          localStorage.setItem('high_score', highScore);
        }
      } else {
        $('#new_high_score').hide();
      };
      if(hasWon) {
        level++;
      } else {
        score = 0;
        level = 0;
      };
      $('.but_start_game').click('click', startGame);
      $('#board .bubble').remove();
      BubbleShoot.ui.endGame(hasWon, score);
    };

    var popBubbles = function(bubbles, delay) {
      console.log('(game.js) popBubbles');
      $.each(bubbles, function() {
        var bubble = this;
        setTimeout(function() {
          bubble.setState(BubbleShoot.BubbleState.POPPING);
          bubble.animatePop();
        }, delay);
        board.popBubbleAt(this.getRow(), this.getCol());
        setTimeout(function() {
          bubble.setState(BubbleShoot.BubbleState.POPPED);
          bubble.getSprite().remove();
        }, delay + 200);
        delay += 60;
      });
    };
  };
  window.requestAnimationFrame = Modernizr.prefixed('requestAnimationFrame',
    window) || function(callback) {
      window.setTimeout(function() {
      callback();
    }, 40);
  }
  return Game;
})(jQuery);
