// === Utility: Resize SVG to match viewport ===
function updateViewBoxToViewport(svg) {
    const width = window.innerWidth;
    const height = window.innerHeight;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
}

// === Easing Function (with optional delay at the beginning) ===
function easeInOutCubic(t) {
    const delay = 0.4; // 0.0–1.0 range for pause
    if (t < delay) return 0;
    t = (t - delay) / (1 - delay);
    return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// === DOM References ===
const svg = document.getElementById('pieces');
const polygon1 = document.getElementById('path1');
const polygon2 = document.getElementById('path2');

// === Animation State ===
let startTime = null;
const duration = 1400;
const delayPolygon2 = 300;
const pointDelays1 = [0, 600, 600, 600, 600];
const pointDelays2 = [0, 0, 400, 400, 900, 1000]; // 6 points in polygon2
const durationPerPoint = 1000; // how long each point takes once it starts

let currentPointsStart1 = [], currentPointsEnd1 = [];
let currentPointsStart2 = [], currentPointsEnd2 = [];

// === Helper Functions ===
function interpolatePointsWithDelays(pointsA, pointsB, elapsed, delays) {
    return pointsA.map((start, i) => {
        const end = pointsB[i];
        const delay = delays[i] || 0;

        let localT = (elapsed - delay) / durationPerPoint;
        localT = Math.max(0, Math.min(localT, 1));
        const easedT = easeInOutCubic(localT);

        const x = start[0] + (end[0] - start[0]) * easedT;
        const y = start[1] + (end[1] - start[1]) * easedT;
        return [x, y];
    });
}

function pointsToString(points) {
    return points.map(p => p.join(',')).join(' ');
}

// === Main Animation Loop ===
function animate(timestamp) {
    if (!startTime) startTime = timestamp;
    const elapsed = timestamp - startTime;

    const interpolated1 = interpolatePointsWithDelays(currentPointsStart1, currentPointsEnd1, elapsed, pointDelays1);
    const interpolated2 = interpolatePointsWithDelays(currentPointsStart2, currentPointsEnd2, elapsed, pointDelays2);

    polygon1.setAttribute('points', pointsToString(interpolated1));
    polygon2.setAttribute('points', pointsToString(interpolated2));

    const lastDelay = Math.max(
        ...pointDelays1,
        ...pointDelays2
    );

    if (elapsed < durationPerPoint + lastDelay) {
        requestAnimationFrame(animate);
    }
}

// === Setup Animation on Load ===
function setupAndAnimate() {
    startTime = null;
    const width = window.innerWidth;
    const height = window.innerHeight;
    updateViewBoxToViewport(svg);

    currentPointsStart1 = [
        [0, 0],
        [900, 550],
        [900, 550],
        [350, height],
        [0, height]
    ];

    currentPointsEnd1 = [
        [0, 0],
        [width, height],
        [width, height],
        [width, height],
        [0, height]
    ];

    currentPointsStart2 = [
        [0, 0],
        [450, 248],
        [1000, 550],
        [1000, 550],
        [400, height],
        [0, height]
    ];

    currentPointsEnd2 = [
        [0, 0],
        [width * 0.2, 0],
        [width * 0.75, height],
        [width * 0.75, height],
        [width * 0.75, height],
        [0, height]
    ];

    polygon1.setAttribute('points', pointsToString(currentPointsStart1));
    polygon2.setAttribute('points', pointsToString(currentPointsStart2));

    requestAnimationFrame(animate);
}

// === Animate Again on Resize ===
function animateOnResize() {
    startTime = null;
    const width = window.innerWidth;
    const height = window.innerHeight;
    updateViewBoxToViewport(svg);

    const parsePoints = el =>
        el.getAttribute('points')
            .trim()
            .split(' ')
            .map(pt => pt.split(',').map(Number));

    currentPointsStart1 = parsePoints(polygon1);
    currentPointsStart2 = parsePoints(polygon2);

    currentPointsEnd1 = [
        [0, 0],
        [width, height],
        [width, height],
        [width * 0.4, height],
        [0, height]
    ];

    currentPointsEnd2 = [
        [0, 0],
        [width * 0.2, 0],
        [width * 0.75, height],
        [width * 0.75, height],
        [width * 0.75, height],
        [0, height]
    ];

    requestAnimationFrame(animate);
}

// === Event Listeners ===
window.addEventListener('load', setupAndAnimate);
window.addEventListener('resize', animateOnResize);
