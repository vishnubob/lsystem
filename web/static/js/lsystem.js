function get_lsystem()
{
    var xmlhttp = new XMLHttpRequest();
    var url = "http://localhost:5000/lsystem";
    $('#lsystem-title').text("Loading...");

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
        {
            resp = JSON.parse(xmlhttp.responseText);
            $('#lsystem-title').text("Title: " + resp["name"]);
            $('#draw-shapes').html(resp["svg"]);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function save_lsystem(resp) 
{
    var xmlhttp = new XMLHttpRequest();
    var url = "http://localhost:5000/save";
    $('#lsystem-title').text("Saving...");

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
        {
            resp = JSON.parse(xmlhttp.responseText);
            $('#lsystem-title').text("Saved " + resp["name"]);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}
