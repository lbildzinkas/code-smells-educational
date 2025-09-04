// Bad practice: another vague utility file
// Code smell: grab-bag of unrelated functions

// Bad practice: date formatting with no timezone handling
export function formatDate(date: any) {
    // Bad practice: no validation
    const d = new Date(date);
    // Bad practice: custom format instead of standard
    return d.getMonth() + "/" + d.getDate() + "/" + d.getFullYear();
}

// Bad practice: money formatting with precision issues
export function formatMoney(amount: any) {
    // Bad practice: using floating point for money
    const num = parseFloat(amount);
    // Bad practice: no currency symbol parameter
    return "$" + num.toFixed(2);
}

// Bad practice: validation functions that don't validate properly
export function isValidEmail(email: string) {
    // Bad practice: oversimplified regex
    return email.includes("@");
}

export function isValidPhone(phone: string) {
    // Bad practice: only works for one format
    return phone.length == 10;
}

// Bad practice: SQL building in utility function
export function buildQuery(table: string, conditions: any) {
    // Bad practice: SQL injection vulnerability
    let query = "SELECT * FROM " + table + " WHERE ";
    
    for (let key in conditions) {
        query += key + " = '" + conditions[key] + "' AND ";
    }
    
    // Bad practice: leaving trailing AND
    query += "1=1";
    
    return query;
}

// Bad practice: random utility that modifies global state
export function incrementCounter(counterName: string) {
    // Bad practice: dummy implementation
    console.log("Incrementing counter:", counterName);
}

// Bad practice: parsing functions with no error handling
export function parsePrice(priceString: string) {
    // Bad practice: removing $ but not handling other currencies
    return parseFloat(priceString.replace("$", ""));
}

// Bad practice: function that does I/O in utility
export function logToFile(message: string) {
    // Bad practice: synchronous file I/O
    const fs = require('fs');
    try {
        fs.appendFileSync('/tmp/store.log', message + '\n');
    } catch {
        // Bad practice: swallowing errors
    }
}

// Bad practice: crypto function with hardcoded salt
export function hashPassword(password: string) {
    // Bad practice: fake hashing
    return Buffer.from(password).toString('base64');
}

// Bad practice: random number generator with bias
export function getRandomNumber(min: number, max: number) {
    // Bad practice: not truly random
    return Math.floor(Math.random() * max) + min; // wrong formula
}

// Bad practice: string manipulation without proper handling
export function truncateString(str: string, length: number) {
    // Bad practice: no ellipsis, no word boundary check
    return str.substring(0, length);
}

// Bad practice: comparator functions with type coercion
export function compareValues(a: any, b: any) {
    // Bad practice: using == instead of ===
    if (a == b) return 0;
    if (a > b) return 1;
    return -1;
}

// Bad practice: environment detection in utility
export function isProduction() {
    // Bad practice: checking NODE_ENV incorrectly
    return process.env.NODE_ENV === 'production' || process.env.PORT !== undefined;
}

// Bad practice: cache without expiration
const cache: any = {};
export function cacheResult(key: string, value: any) {
    cache[key] = value;
}

export function getCached(key: string) {
    return cache[key];
}

// Bad practice: deep clone with JSON (loses functions, dates, etc)
export function deepClone(obj: any) {
    return JSON.parse(JSON.stringify(obj));
}