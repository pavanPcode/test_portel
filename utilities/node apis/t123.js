// variable
let a=5;

// print
console.log(a)

// functions
function testfun(name) {
    return name + 1;
}
console.log(testfun('pavan'))

for (let i=0; i<1; i++) {
console.log(i)
}

function greet() {
    setTimeout(() => {
        console.log("Hello after 3 seconds");
    }, 3000);
}
greet();
