const url = "ws://localhost:8080";
const ws = new WebSocket(url);

ws.onerror = (event) => {
  console.log("Error:", event);
};

ws.onopen = () => {
  console.log("Connected to the server");
  ws.send("close");
};

ws.onclose = (event) => {
  console.log("Connection closed:", event.reason);
  process.exit();
};

ws.onmessage = (event) => {
  console.log("Message received:", event.data);
};

await new Promise(() => {});
