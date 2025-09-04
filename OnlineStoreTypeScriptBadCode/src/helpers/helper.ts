// Bad practice: vague filename with unclear purpose
// Code smell: utility functions with no clear responsibility

// Bad practice: function that does too many things
export function doSomething(input: any, type: string) {
    if (type == "validate") {
        // Bad practice: weak validation
        if (input) {
            return true;
        } else {
            return false;
        }
    } else if (type == "format") {
        // Bad practice: assuming input type
        return input.toString().toUpperCase();
    } else if (type == "calculate") {
        // Bad practice: magic numbers
        return input * 1.5 + 10;
    } else {
        // Bad practice: returning different types
        return null;
    }
}

// Bad practice: function with side effects and unclear name
export function processData(data: any) {
    // Bad practice: modifying global state from helper
    if (data.error) {
        // Assuming globals exist
        console.log("Error occurred: " + data.error);
    }
    
    // Bad practice: random processing
    const result = Math.random() > 0.5 ? data : null;
    
    // Bad practice: logging sensitive data
    console.log("Processing: " + JSON.stringify(data));
    
    return result;
}

// Bad practice: function that's too generic
export function convertValue(value: any, from: string, to: string) {
    // Bad practice: incomplete implementation
    if (from == "string" && to == "number") {
        return parseInt(value); // no error handling
    } else if (from == "number" && to == "string") {
        return value + ""; // implicit conversion
    } else {
        // Bad practice: throwing generic error
        throw "Conversion not supported";
    }
}

// Bad practice: utility function with hardcoded values
export function getDiscount(customerType: string) {
    // Bad practice: hardcoded business logic in helper
    switch (customerType) {
        case "gold":
            return 0.20;
        case "silver":
            return 0.10;
        case "bronze":
            return 0.05;
        default:
            return 0; // no discount
    }
}

// Bad practice: function that returns different types
export function checkSomething(input: any) {
    if (!input) {
        return false;
    }
    if (input.length > 10) {
        return "too long";
    }
    if (input.length < 3) {
        return -1;
    }
    return true;
}

// Bad practice: async function that's not really async
export async function fakeAsync(data: any) {
    // Bad practice: fake delay
    const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
    await delay(100);
    
    // Bad practice: no real async operation
    return data + " processed";
}

// Bad practice: function with too many parameters
export function complexCalculation(a: number, b: number, c: number, d: number, e: number, f: string, g: boolean) {
    // Bad practice: incomprehensible logic
    let result = a + b;
    if (g) {
        result *= c;
    } else {
        result -= d;
    }
    
    if (f == "special") {
        result = result / e;
    }
    
    // Bad practice: returning NaN possible
    return result;
}

// Bad practice: empty functions
export function futureFeature() {
    // TODO: implement this
}

export function deprecated() {
    // This function is deprecated but still exported
}

// Bad practice: console.log in production code
export function debugLog(message: any) {
    console.log("DEBUG: " + message);
    console.log("Stack trace: " + new Error().stack);
}