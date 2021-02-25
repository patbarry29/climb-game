let canvas;
let context;
let width;
let height;

let star;
let stars = [];

let speed;

let interval_id;

document.addEventListener('DOMContentLoaded', init, false)

function init() {
    canvas = document.querySelector('canvas');
    context = canvas.getContext('2d');
    width = canvas.width;
    height = canvas.height;

    for (let i =0; i< 800; i++) {
        star = {
            x : getRandomNumber(0,width),
            y : getRandomNumber(0,height),
            z : getRandomNumber(0, width),
            size : getRandomNumber(1,5)
        }
        stars.push(star);
    }
    console.log(stars.length)
    interval_id = window.setInterval(draw, 100);
}

function draw() {
    for (let s of stars) {
        context.fillStyle = 'white';
        context.fillRect(s.x, s.y, s.size, s.size);
    }
}

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}