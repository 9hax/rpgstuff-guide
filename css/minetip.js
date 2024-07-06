// Get all elements with the class 'minetext'
const minetextElements = document.querySelectorAll('.minetext');
const minetip = document.getElementById('minetip-tooltip'); // Assuming minetip is defined elsewhere

// Add mouseover event listener to each element
minetextElements.forEach(element => {
  element.addEventListener('mouseover', function(event) {
    minetip.innerHTML = event.target.parentElement.getAttribute("title");
    minetip.style.display = "block";
  });

  // Add mouseout event listener to each element
  element.addEventListener('mouseout', function() {
    minetip.style.display = "none";
  });

  // Add mousemove event listener to each element
  element.addEventListener('mousemove', function(event) {
    pos(minetip, 5, -30, event);
  });
});

var pos = function (o, x, y, event) {
    var posX = 0, posY = 0;
    var e = event || window.event;
    if (e.pageX || e.pageY) {
        posX = e.pageX;
        posY = e.pageY;
    } else if (e.clientX || e.clientY) {
        posX = event.clientX + document.documentElement.scrollLeft + document.body.scrollLeft;
        posY = event.clientY + document.documentElement.scrollTop + document.body.scrollTop;
    }
    o.style.position = "absolute";
    o.style.top = (posY + y) + "px";
    o.style.left = (posX + x) + "px";
}

minetip.style.display = "none";