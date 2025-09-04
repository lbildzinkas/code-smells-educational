// Bad practice: meaningless filename
// Code smell: junk drawer anti-pattern

// Bad practice: constants that aren't constant
export let TEMP_VALUE = 42;
export let FLAG = false;
export let COUNTER = 0;

// Bad practice: array of magic values
export const MAGIC_NUMBERS = [3.14, 2.71, 1.41, 42, 69, 420, 1337];

// Bad practice: function that does nothing useful
export function doStuff(stuff: any) {
    // Bad practice: useless operations
    const x = stuff;
    const y = x;
    const z = y;
    return z;
}

// Bad practice: boolean function with side effects
export function checkFlag() {
    // Bad practice: modifying what we're checking
    FLAG = !FLAG;
    return FLAG;
}

// Bad practice: timer functions that leak
export function startTimer() {
    // Bad practice: no way to stop this timer
    setInterval(() => {
        COUNTER++;
        console.log("Timer: " + COUNTER);
    }, 1000);
}

// Bad practice: random globals manipulation
export function messWithGlobals() {
    // Bad practice: dummy implementation
    console.log("Messing with globals");
}

// Bad practice: error generator
export function generateError(type: string) {
    switch (type) {
        case "null":
            // @ts-ignore
            return null.toString();
        case "undefined":
            // @ts-ignore
            return undefined.toString();
        case "throw":
            throw new Error("Generated error");
        default:
            return 1 / 0; // Infinity
    }
}

// Bad practice: recursive function without base case
export function infiniteLoop(n: number): any {
    // This will cause stack overflow
    return infiniteLoop(n + 1);
}

// Bad practice: function that depends on execution order
let callCount = 0;
export function orderDependent() {
    callCount++;
    if (callCount % 2 === 0) {
        return "even";
    } else {
        return "odd";
    }
}

// Bad practice: monkey patching
export function patchArray() {
    // @ts-ignore
    Array.prototype.badMethod = function() {
        return "This is bad!";
    };
}

// Bad practice: eval usage
export function runCode(code: string) {
    // Security vulnerability
    return eval(code);
}

// Bad practice: blocking operation
export function blockThread(seconds: number) {
    const start = Date.now();
    while (Date.now() - start < seconds * 1000) {
        // Blocking the thread
    }
}

// Bad practice: memory leak creator
const leakyArray: any[] = [];
export function createMemoryLeak() {
    for (let i = 0; i < 1000000; i++) {
        leakyArray.push(new Array(1000).fill(Math.random()));
    }
}

// Bad practice: console spam
export function spamConsole() {
    console.log("SPAM");
    console.warn("SPAM WARNING");
    console.error("SPAM ERROR");
    console.info("SPAM INFO");
    console.debug("SPAM DEBUG");
}

// Bad practice: type confusion
export function confuseTypes(input: any) {
    if (typeof input === "string") {
        return parseInt(input);
    }
    if (typeof input === "number") {
        return input.toString();
    }
    if (typeof input === "boolean") {
        return input ? 1 : "0"; // returning different types
    }
    return null;
}

// Bad practice: exports object that can be modified
export const mutableExport = {
    value: "initial",
    change: function() {
        this.value = "changed";
    }
};