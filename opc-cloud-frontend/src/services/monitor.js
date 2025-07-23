let socket = null;

export const connectMonitorSocket = (onMessage, onError) => {
  const url = import.meta.env.DEV
    ? 'ws://localhost:8000/ws/monitor'
    : 'ws://backend:8000/ws/monitor';

  socket = new WebSocket(url);

  socket.onopen = () => {
    console.log("✅ WebSocket connected");
    // Example payload: server URL and node IDs
    socket.send(
      JSON.stringify({
        server_url: "opc.tcp://conmicro020:62640/IntegrationObjects/ServerSimulator",  // Update dynamically if needed
        node_ids: ["ns=2;s=Demo.Static.Scalar.Double", "ns=2;s=Demo.Static.Scalar.Float"]
      })
    );
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (onMessage) onMessage(data);
  };

  socket.onerror = (err) => {
    console.error("WebSocket error", err);
    if (onError) onError(err);
  };

  socket.onclose = () => {
    console.warn("WebSocket closed");
  };
};

export const closeMonitorSocket = () => {
  if (socket) socket.close();
};
