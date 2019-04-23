setInterval(() => httpGetAsync('/state.txt', (state) => drawState(state)), 100);
//httpGetAsync('/state.txt', (state) => drawState(state));

function httpGetAsync(url, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.setRequestHeader('cache-control', 'no-cache, must-revalidate, post-check=0, pre-check=0');
    xmlHttp.setRequestHeader('cache-control', 'max-age=0');
    xmlHttp.send(null);
}

function drawState(state)
{
    var c = document.getElementById('intersection').getContext('2d');
    var width = c.canvas.clientWidth;
    var height = c.canvas.clientHeight;
    c.clearRect(0, 0, width, height);
    var radius = Math.min(width/2, height/2) - 100;

    state = state.split(' ');
    var lon = state[0];
    var lat = state[1];

    c.font = "25px Arial";
    c.fillText(`Longitude: ${lon}`, width/2 - 100, height/2); 
    c.fillText(`Latitude: ${lat}`, width/2 - 100, height/2 + 30); 
    
    c.beginPath();
    c.arc(width/2, height/2, radius, 0, 2*Math.PI);
    c.stroke();

    var num_directions = parseInt(state[2]);
    var directions = state.slice(3).map(x => parseInt(x));
    for (var i = 0; i < num_directions; i++)
    {
        drawLight(c, radius, directions[i*4], directions[i*4+1], directions[i*4+2], directions[i*4+3]);
    }
}

function drawLight(context, radius, color, left, direction, time)
{
    var c = context;
    var width = c.canvas.clientWidth;
    var height = c.canvas.clientHeight;

    var angle = ((direction/32 * 2*Math.PI) + Math.PI/2) % (2*Math.PI);

    var x = width/2 + Math.cos(angle)*radius - 20;
    var y = height/2 - Math.sin(angle)*radius - 60;

    if (left)
        x -= 50;

    c.fillStyle = "#000000";
    c.fillRect(x, y, 40, 120);

    // red
    c.fillStyle = color == 3 && !left ? "#fe0010" : "#590006";

    c.beginPath();
    c.arc(x+20, y+25, 15, 0, 2*Math.PI);
    c.fill();

    if (color == 3 && left)
    {
        c.fillStyle = "#fe0010";
        c.font = "45px Arial";
        c.fillText('￩', x+10, y+43);
    }

    // yellow
    c.fillStyle = color == 2 && !left ? "#fbd21a" : "#594809";

    c.beginPath();
    c.arc(x+20, y+60, 15, 0, 2*Math.PI);
    c.fill();

    if (color == 2 && left)
    {
        c.fillStyle = "#fbd21a";
        c.font = "45px Arial";
        c.fillText('￩', x+10, y+78);
    }

    // green
    c.fillStyle = color == 1 && !left ? "#79fe00" : "#2b5900";

    c.beginPath();
    c.arc(x+20, y+95, 15, 0, 2*Math.PI);
    c.fill();

    if (color == 1 && left)
    {
        c.fillStyle = "#79fe00";
        c.font = "45px Arial";
        c.fillText('￩', x+10, y+113);
    }

    // time
    c.fillStyle = "#000000";
    c.font = "25px Arial";
    c.fillText(time, x+10, y+145);
}
