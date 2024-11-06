function makeSnow() {
    const snow = document.createElement('div');
    const size = Math.random() * 4.5 + 3.5;
    snow.className = 'snow';
    snow.style.width = size + 'px';
    snow.style.height = size + 'px';
    snow.style.left = Math.random() * window.innerWidth + 'px';
    snow.style.opacity = size / 8;
    if (size < 7) {
        snow.style,zIndex = -5;
    }
    snow.style.animationDirection = Math.random() * 3 + 2 + 's';
    document.body.appendChild(snow);
    setTimeout(() => snow.remove(), 5000);
}

setInterval(makeSnow, 40);