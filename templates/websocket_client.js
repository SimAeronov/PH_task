// Wait for my client to load page
document.addEventListener("DOMContentLoaded", function(){
    // Establich new websocket connection
    const websocketClient = new WebSocket("ws://localhost:12345/");
    // Get tag by id = message_container
    const messagesContainer = document.querySelector("#message_container");
    // When a client connects send a "Client_connected" message, later I use this as a keyword to trigger next func
    websocketClient.onopen = function(){
        websocketClient.send("Client_Connected");
    };
    // Upon receiving "Client_Connected" I start sending data messages to all clients, I assign that data to my <tag>
    websocketClient.onmessage = function(message){
        messagesContainer.textContent  = message.data;
    };

}, false);

