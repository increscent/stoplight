function httpGetAsync(url, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.send(null);
}

function drawState(state)
{
    var c = document.getElementById('intersection').getContext('2d');
    var width = c.canvas.clientWidth;
    var height = c.canvas.clientHeight;

    state = state.split(' ');
    var lon = state[0];
    var lat = state[1];

    c.fillStyle = "#000000";
    c.font = "25px Arial";
    c.fillText(`Longitude: ${lon}`, width/2 - 100, height/2); 
    c.fillText(`Latitude: ${lat}`, width/2 - 100, height/2 + 30); 
    
    c.beginPath();
    c.arc(width/2, height/2, Math.min(width/2, height/2)-50, 0, 2*Math.PI);
    c.stroke();
}

//setInterval(() => httpGetAsync('/state.txt', (state) => drawState(state)), 100);
httpGetAsync('/state.txt', (state) => drawState(state));
