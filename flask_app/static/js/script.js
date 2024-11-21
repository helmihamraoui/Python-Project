(function () {
    const link = document.querySelectorAll('nav > .hover-this');
    const cursor = document.querySelector('.cursor');
    const animateit = function (e) {
        const span = this.querySelector('span');
        const { offsetX: x, offsetY: y } = e,
        { offsetWidth: width, offsetHeight: height } = this,
        move = 25,
        xMove = x / width * (move * 2) - move,
        yMove = y / height * (move * 2) - move;
        span.style.transform = `translate(${xMove}px, ${yMove}px)`;
        if (e.type === 'mouseleave') span.style.transform = '';
};
const editCursor = e => {
        const { clientX: x, clientY: y } = e;
        cursor.style.left = x + 'px';
        cursor.style.top = y + 'px';
    };
    link.forEach(b => b.addEventListener('mousemove', animateit));
    link.forEach(b => b.addEventListener('mouseleave', animateit));
    window.addEventListener('mousemove', editCursor);
})();
const toggle = document.getElementById("toggle")
const nav = document.getElementById('nav')
const ul = document.querySelector("nav.active ul")
toggle.addEventListener('click',()=>{
    nav.classList.toggle('active');
})
// Get references to the image and the popup list
const image = document.getElementById("clickable-image");
const popup = document.getElementById("popup-list");

// Add an event listener to the image
image.addEventListener("click", function() {
    // Toggle the popup visibility
    popup.style.display = popup.style.display === "block" ? "none" : "block";
});

// Optionally close the popup if clicked outside (optional)
window.addEventListener("click", function(event) {
    if (!popup.contains(event.target) && event.target !== image) {
        popup.style.display = "none";
    }
});
