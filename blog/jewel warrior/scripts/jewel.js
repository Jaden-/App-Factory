var jewel = (function() {
	var scriptQueue = [],
		numResourcesLoaded = 0,
		numResources = 0,
		executeRunning,
		settings = {
			rows: 8,
			cols: 8,
			baseScore: 100,
			numJewelTypes: 7,
			baseLevelTimer: 60000,
			baseLevelScore: 1500,
			baseLevelExp: 1.05
		};

	function hasWebWorkers() {
		return ('worker' in window);
	}

	function preload(src) {
		var image = new Image();
		image.src = src;
	}

	function getLoadProgress() {
		console.log('Resources: ' + numResourcesLoaded + ' / ' + numResources);
		return numResourcesLoaded/numResources;
	}

	function executeScriptQueue() {
		var next = scriptQueue[0],
			first, script;
		if(next && next.loaded) {
			executeRunning = true;
			// remove the first element in the queue
			scriptQueue.shift();
			first = document.getElementsByTagName("script")[0];
			script = document.createElement("script");
			script.onload = function() {
				if(next.callback) {
					next.callback();
				}
				// try to execute more scripts
				executeScriptQueue();
			};
			script.src = next.src;
			first.parentNode.insertBefore(script, first);
		}else {
			executeRunning = false;
		}
	}

	function load(src, callback) {
		console.log('loading ' + src + ', numResources: ' + (numResources + 1));
		var image, queueEntry;
			numResources++;

		// add this resource to the execution queue
		queueEntry = {
			src: src,
			callback: callback,
			loaded: false
		};

		scriptQueue.push(queueEntry);

		image = new Image();
		image.onload = image.onerror = function() {
			numResourcesLoaded++;
			queueEntry.loaded = true;
			if(!executeRunning) {
				executeScriptQueue();
			}
		};
		image.src = src;
	}

	function setup() {
		jewel.showScreen("splash-screen");
	}

	// hide the active screen (if any) and show the screen
	// with the specified id
	function showScreen(screenId) {
		var dom = jewel.dom,
			$ = dom.$,
			activeScreen = $("#game .screen.active")[0],
			screen = $("#" + screenId) [0];
		if(!jewel.screens[screenId]) {
			alert("This module is not implemented yet!");
			return;
		}
		if(activeScreen) {
			dom.removeClass(activeScreen, "active");
		}
		dom.addClass(screen, "active");
		// run the screen module
		jewel.screens[screenId].run();
	}

	// expose public methods
	return {
		getLoadProgress: getLoadProgress,
		preload: preload,
		load: load,
		setup: setup,
		showScreen: showScreen,
		screens: {},
		hasWebWorkers: hasWebWorkers,
		settings: settings
	};
})();
