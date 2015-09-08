function Map(gameData) {
    this.map = gameData;
    var rows = gameData.length;
    var cons = gameData[0].length;
    var count = 0;
    var REMOVE_ON = 22;
    var NUM_COLORS = 8;
    var DEBUG_MODE = false;


    this.createEmptyMap = function () {
        var map = [];
        for (var y = 0; y < rows; y++) {
            map[y] = [];
            for (var x = 0; x < cons; x++) {
                map[y][x] = false;
            }
        }
        return map;
    };
    var checkMap;

    this.checkAndRemovePeices = function () {
        for (var y = 0; y < rows; y++) {
            for (var x = 0; x < cons; x++) {
                for (var col = 1; col <= NUM_COLORS; col++) {

                    checkMap = this.createEmptyMap();
                    this.checkPosition(x, y, col);

                    if (count >= REMOVE_ON) {
                        this.resetMap();
                        if (DEBUG_MODE) {
                            console.log("Count: " + count + ", of Color nr.: " + col);
                            console.log(this.toString());
                        }
                    }
                    count = 0;
                }
            }
        }
    };

    this.resetMap = function () {
        for (var y = 0; y < rows; y++) {
            for (var x = 0; x < cons; x++) {
                this.map[y][x] = 0;
            }
        }
    }


    this.checkPosition = function (x, y, code) {
        if (this.map[y][x] != undefined && this.map[y][x] == code && !checkMap[y][x]) {

            checkMap[y][x] = true;
            count++;

            if (this.peiceExists(x + 1, y)) {
                this.checkPosition(x + 1, y, code);
            }
            if (this.peiceExists(x, y + 1)) {
                this.checkPosition(x, y + 1, code);
            }
            if (this.peiceExists(x - 1, y)) {
                this.checkPosition(x - 1, y, code);
            }
            if (this.peiceExists(x, y - 1)) {
                this.checkPosition(x, y - 1, code);
            }

        }
    };
    this.removePeices = function (x, y, code) {
        if (this.map[y][x] != undefined && this.map[y][x] == code) {

            this.map[y][x] = 0;
            if (this.peiceExists(x + 1, y)) {
                this.removePeices(x + 1, y, code);
            }
            if (this.peiceExists(x, y + 1)) {
                this.removePeices(x, y + 1, code);
            }
            if (this.peiceExists(x - 1, y)) {
                this.removePeices(x - 1, y, code);
            }
            if (this.peiceExists(x, y - 1)) {
                this.removePeices(x, y - 1, code);
            }
        }
    };

    this.peiceExists = function (x, y) {
        if (x < cons && x >= 0 && y < rows && y >= 0) {
            return true;
        }
        return false;
    };


    this.toString = function () {

        var log = "";
        for (var y = 0; y < rows; y++) {
            for (var x = 0; x < cons; x++) {
                log += this.map[y][x];
            }
            log += "\n";
        }
        return log;
    };

}
