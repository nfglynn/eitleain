var ws = new WebSocket("ws://127.0.0.1:8765", "protocolOne");

ws.onconnect = function(event) {
    console.log("connected!");
};


ws.onmessage = function(event) {
    message = event.data; //JSON.parse(event.data)
    console.log(message);
    $.growl.notice({ message: message });
};
