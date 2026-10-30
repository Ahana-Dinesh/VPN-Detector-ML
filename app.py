from flask import Flask, request, render_template, redirect, url_for, session
import requests
import time
import joblib
import numpy as np
import datetime
import os

app = Flask(__name__)
app.secret_key = "secret_key"

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

API_KEY = os.environ.get("VPNAPI_KEY")
IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN")

model = joblib.load("model.pkl")

request_count = {}
last_location = {}
logs = []


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]

    ip_address = get_real_ip()

    vpn_api, proxy = check_ip_security(ip_address)
    latency = check_latency()
    frequency = get_frequency(ip_address)

    city, country = get_location(ip_address)
    location = f"{city}, {country}"

    location_change = get_location_change(ip_address, location)

    vpn = vpn_api
    if vpn == 0 and country != "IN":
        vpn = 1

    features = np.array([[vpn, proxy, latency, frequency, location_change]])
    prediction = model.predict(features)[0]

    risk_score = 0

    if vpn:
        risk_score += 30
    if proxy:
        risk_score += 25
    if latency > 800:
        risk_score += 15
    if frequency > 5:
        risk_score += 15
    if location_change == 1:
        risk_score += 15

    if vpn == 1:
        if prediction == 1 or risk_score > 60:
            level = "High Risk"
        elif risk_score > 30:
            level = "Medium Risk"
        else:
            level = "Medium Risk"
    else:
        if latency > 1500 or frequency > 10:
            level = "Medium Risk"
        else:
            level = "Low Risk"

    logs.append({
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": username,
        "ip": ip_address,
        "location": location,
        "vpn": vpn,
        "proxy": proxy,
        "latency": int(latency),
        "frequency": frequency,
        "location_change": location_change,
        "risk": level
    })

    if username.lower() != "admin":
        return f"<h1>Hi {username} 👋</h1>"

    return f"""
    <h1>Hi Admin 👨‍💻</h1>

    <h2>🤖 VPN Risk Detection Result</h2>

    <p><b>User:</b> {username}</p>
    <p><b>IP:</b> {ip_address}</p>
    <p><b>Location:</b> {location}</p>
    <p><b>VPN:</b> {bool(vpn)}</p>
    <p><b>Proxy:</b> {bool(proxy)}</p>
    <p><b>Latency:</b> {int(latency)} ms</p>
    <p><b>Frequency:</b> {frequency}</p>
    <p><b>Location Change:</b> {location_change}</p>
    <p><b>Risk Level:</b> {level}</p>

    <br><br>
    <a href="/logs">View All Logs</a>
    """


@app.route("/logs")
def view_logs():
    if "user" not in session or session["user"].lower() != "admin":
        return "<h2>Access Denied ❌</h2>"

    output = """
    <h1>📊 Admin Log Dashboard</h1>
    <table border="1" cellpadding="10">
    <tr>
        <th>Time</th>
        <th>User</th>
        <th>IP</th>
        <th>Location</th>
        <th>VPN</th>
        <th>Proxy</th>
        <th>Latency</th>
        <th>Frequency</th>
        <th>Risk</th>
    </tr>
    """

    for log in logs:
        output += f"""
        <tr>
            <td>{log['time']}</td>
            <td>{log['user']}</td>
            <td>{log['ip']}</td>
            <td>{log['location']}</td>
            <td>{log['vpn']}</td>
            <td>{log['proxy']}</td>
            <td>{log['latency']}</td>
            <td>{log['frequency']}</td>
            <td>{log['risk']}</td>
        </tr>
        """

    output += "</table>"
    return output


def get_real_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    if ip.startswith(("127.", "10.", "192.168", "172.")):
        try:
            return requests.get("https://api.ipify.org").text
        except:
            return ip

    return ip


def check_ip_security(ip_address):
    try:
        response = requests.get(f"https://vpnapi.io/api/{ip_address}?key={API_KEY}")
        data = response.json()

        if "security" in data:
            vpn = int(data["security"].get("vpn", False))
            proxy = int(data["security"].get("proxy", False))
        else:
            vpn = 0
            proxy = 0

        return vpn, proxy
    except:
        return 0, 0


def check_latency():
    try:
        start = time.time()
        requests.get("https://www.google.com", timeout=5)
        end = time.time()
        return (end - start) * 1000
    except:
        return 0


def get_frequency(ip):
    request_count[ip] = request_count.get(ip, 0) + 1
    return request_count[ip]


def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}")
        data = response.json()
        return data.get("city", "Unknown"), data.get("country", "Unknown")
    except:
        return "Unknown", "Unknown"


def get_location_change(ip, current_location):
    change = 1 if ip in last_location and last_location[ip] != current_location else 0
    last_location[ip] = current_location
    return change


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)