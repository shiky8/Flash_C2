from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Flashlight c2 Encoder</title>
  <style>
  body {
    background: linear-gradient(135deg, #0d0d0d, #1a001f);
    color: #eee;
    text-align: center;
    font-family: Arial, sans-serif;
    height: 100vh;
    margin: 0;
    display: flex;
    justify-content: center;   /* Horizontal center */
    align-items: center;       /* Vertical center */
  }

  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }

  h1 {
    font-size: 2.5rem;
    color: #ff00ff;
    text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff66ff;
    margin-bottom: 20px;
  }

  input[type="text"] {
    font-size: 18px;
    padding: 12px 20px;
    border-radius: 12px;
    border: none;
    outline: none;
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 4px 30px rgba(255, 0, 255, 0.3);
    border: 1px solid rgba(255, 0, 255, 0.2);
    width: 300px;
    transition: all 0.3s ease;
    text-align: center;
  }

  input[type="text"]::placeholder {
    color: rgba(255, 200, 255, 0.6);
  }

  input[type="text"]:focus {
    box-shadow: 0 0 20px #ff33cc, 0 0 40px #ff00ff;
    border-color: #ff33cc;
  }

  button {
    font-size: 18px;
    padding: 12px 20px;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    background: linear-gradient(135deg, #ff00cc, #6600ff);
    color: white;
    box-shadow: 0 0 10px #ff00ff, 0 0 20px #6600ff;
    transition: all 0.3s ease;
  }

  button:hover {
    box-shadow: 0 0 20px #ff00ff, 0 0 40px #6600ff;
    transform: scale(1.05);
  }

  #status {
    font-size: 20px;
    color: #ff66ff;
    text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff33cc;
    margin-top: 10px;
  }
</style>
</head>
<body>
  <div class="container">
    <h1>Flashlight c2</h1>
    <input type="text" id="message" placeholder="Enter text to send">
    <button onclick="sendMessage()">Send</button>
    <div id="status">Status: idle</div>
  </div>

  

  

<script>
async function sendMessage() {
  const text = document.getElementById("message").value + "  ";
  if (!text) return alert("Enter a message first!");

  // Convert text to binary
  let bits = "";
  for (let i = 0; i < text.length; i++) {
    bits += text.charCodeAt(i).toString(2).padStart(8, "0");
  }

  // Add start (11111110) and end (00000000) markers
  const START_MARKER = "11111110";
  const END_MARKER = "00000000";
  bits = START_MARKER + bits + END_MARKER;

  const status = document.getElementById("status");
  status.innerText = "Encoding: " + bits;

  // Access flashlight
  const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
  const track = stream.getVideoTracks()[0];

  if (!track.getCapabilities().torch) {
    alert("Torch not supported on this device!");
    return;
  }

  let bitIndex = 0;
  const BIT_DURATION = 500; // ms per bit

  function sendBit() {
    if (bitIndex >= bits.length) {
      track.stop();
      status.innerText = "Done sending!";
      return;
    }
    const bit = bits[bitIndex];
    track.applyConstraints({ advanced: [{ torch: bit === "1" }] });
    bitIndex++;
    setTimeout(sendBit, BIT_DURATION);
  }

  sendBit();
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
