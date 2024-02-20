function connectToStatsStream() {
    var source = new EventSource("/stream");
    
    source.onmessage = function(event) {
        var data = JSON.parse(event.data);
        document.getElementById("visitor_count").innerText = data.visitor_count;
        document.getElementById("unique_visitors").innerText = data.unique_visitors;
        document.getElementById("user_visits").innerText = data.user_visits;
    };
    
    source.onerror = function(event) {
        console.error("Error occurred in stream:", event);
        setTimeout(connectToStatsStream, 3000);
    };
}

window.onload = connectToStatsStream;
