class Stopwatch {
    constructor(display, results) {
        this.running = false;
        this.display = display;
        this.results = results;
        this.laps = [];
        this.reset();
        this.print(this.times);
    }
    
    reset() {
        this.ms = 0;
				this.s = 0;
				this.m = 0
    }
    
    start() {
        if (!this.time) this.time = performance.now();
        if (!this.running) {
            this.running = true;
            requestAnimationFrame(this.step.bind(this));
        }
    }
    
    lap() {
        let times = this.times;
        let li = document.createElement('li');
        li.innerText = this.format(times);
        this.results.appendChild(li);
    }
    
    stop() {
        this.running = false;
        this.time = null;
    }

    restart() {
        if (!this.time) this.time = performance.now();
        if (!this.running) {
            this.running = true;
            requestAnimationFrame(this.step.bind(this));
        }
        this.reset();
    }
    
    /*clear() {
        clearChildren(this.results);
    }*/
    
    step(timestamp) {
        if (!this.running) return;
        this.calculate(timestamp);
        this.time = timestamp;
        this.print();
        requestAnimationFrame(this.step.bind(this));
    }
    
    calculate(timestamp) {
        var diff = timestamp - this.time;
        // Hundredths of a second are 100 ms
        this.ms += diff / 10;
        // Seconds are 100 hundredths of a second
        if (this.ms >= 100) {
            this.s += 1;
            this.ms -= 100;
        }
        // Minutes are 60 seconds
        if (this.s >= 60) {
            this.m += 1;
            this.s -= 60;
        }
    }
    
    print() {
        this.display.innerText = "Time: " + this.format(this.ms, this.s, this.m);
    }
    
    format(ms, s, m) {
        return `\
${pad0(m, 2)}:\
${pad0(s, 2)}:\
${pad0(Math.floor(ms), 2)}`;
    }
}

function pad0(value, count) {
    var result = value.toString();
    for (; result.length < count; --count)
        result = '0' + result;
    return result;
}

function clearChildren(node) {
    while (node.lastChild)
        node.removeChild(node.lastChild);
}