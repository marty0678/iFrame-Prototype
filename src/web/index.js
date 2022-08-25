window.onload = configureWebSocket();

let backend;

function configureWebSocket() {
  new QWebChannel(qt.webChannelTransport, function (channel) {
    backend = channel.objects.backend;
  });
}

function sendMessage() {
  const message = JSON.stringify({
    message: document.getElementById("message").value,
  });

  backend.set(message);
}

async function getMessage() {
  const message = JSON.parse(await backend.get());

  document.getElementById("returnedValue").innerHTML = message.message;
}
