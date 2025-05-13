from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import socket
import ipaddress
import json
import os

app = Flask(__name__)

VIC_FILE = "victims.json"
ADMIN_PASSWORD = "kader11000"  # كلمة المرور

HTML_LOGIN = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #111; color: #fff; }
        .container { max-width: 400px; margin: auto; padding: 20px; border-radius: 8px; background: #333; box-shadow: 0 0 10px #00ff87; }
        h2 { text-align: center; color: #00d4ff; }
        input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 8px; border: 2px solid #00ff87; background-color: #222; color: #00ff87; }
        button { width: 100%; padding: 10px; background-color: #00ff87; color: #000; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Login</h2>
        <form method="post">
            <input type="password" name="password" placeholder="Enter password" required />
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>QUIC Exploit Scanner</title>
  <style>
    body { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); font-family: 'Segoe UI', sans-serif; color: #fff; padding: 20px; }
    .banner { background: #00ff87; padding: 10px; border-radius: 8px; text-align: center; color: #001c1c; font-size: 1.2em; font-weight: bold; margin-bottom: 20px; box-shadow: 0 0 10px #00ff87; }
    h1 { color: #00d4ff; text-align: center; }
    .container { max-width: 900px; margin: auto; background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; box-shadow: 0 0 10px rgba(0, 255, 255, 0.2); }
    textarea, input { width: 100%; padding: 10px; margin-top: 10px; border-radius: 8px; background: #112; color: #0f0; border: none; }
    label { font-weight: bold; color: #ff0; }
    button { padding: 10px 20px; margin: 5px; background: linear-gradient(45deg, #00ff87, #60efff); color: #000; font-weight: bold; border: none; border-radius: 10px; cursor: pointer; }
    pre { background: #001c1c; padding: 15px; border-radius: 8px; margin-top: 20px; color: #ff0; max-height: 400px; overflow-y: auto; }
  </style>
</head>
<body>
  <div class="banner">
    <h2>powered by <span>kader11000</span></h2>
  </div>
  <h1>QUIC Protocol Vulnerability Scanner</h1>
  <div class="container">
    <label for="attacker_ip">Your IP:</label>
    <input id="attacker_ip" placeholder="192.168.1.100" />
    <label for="attacker_port">Your Port:</label>
    <input id="attacker_port" placeholder="4444" />

    <label for="ips">Target IPs (comma, newline, or CIDR):</label>
    <textarea id="ips" rows="5" placeholder="8.8.8.8\n1.1.1.1\n192.168.0.0/30"></textarea>

    <button onclick="scanIPs()">Start Scan</button>
    <button onclick="showVictims()">عرض النتائج والضحايا</button>
    <pre id="output">Results will appear here...</pre>
  </div>

  <script>
    let attacker_ip = '';
    let attacker_port = '';

    async function scanIPs() {
      const rawInput = document.getElementById('ips').value.trim();
      const ip = document.getElementById('attacker_ip').value.trim();
      const port = document.getElementById('attacker_port').value.trim();

      if (!ip || !port) {
        alert("Please enter your IP and Port.");
        return;
      }

      attacker_ip = ip;
      attacker_port = port;

      let ips = rawInput.split(/\s|,|\n/).filter(x => x);
      const output = document.getElementById('output');
      output.innerHTML = 'Scanning...<br>';

      const response = await fetch('/scan', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ ips })
      });

      const results = await response.json();
      output.innerHTML = '';

      results.forEach(res => {
        let block = `<div><strong>[+] ${res.ip}</strong> => ${res.status}<br>`;
        if (res.libraries && res.libraries.length > 0) {
          res.libraries.forEach(lib => {
            block += `&nbsp;&nbsp;&nbsp;Library: ${lib} <button onclick="exploit('${res.ip}', '${lib}')">Exploit</button><br>`;
          });
        }
        block += `</div><hr>`;
        output.innerHTML += block;
      });
    }

    async function exploit(ip, lib) {
      const output = document.getElementById('output');
      output.innerHTML += `<div style="color:yellow;">[*] Exploiting ${ip} (${lib})...</div>`;
      const response = await fetch('/exploit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ ip, library: lib, attacker_ip, attacker_port })
      });
      const data = await response.json();
      output.innerHTML += `<div style="color:lime;">[+] Result: ${data.result}</div>`;
    }

    async function showVictims() {
      const output = document.getElementById('output');
      const response = await fetch('/victims');
      const data = await response.json();
      output.innerHTML = '<h3>Victims List:</h3>' + JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            return redirect(url_for("index"))
        return "<h1 style='color:red;'>Invalid password</h1>"
    return HTML_LOGIN

@app.route("/index")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
