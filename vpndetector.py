import requests
import time


def get_ip_address():
    try:
        response = requests.get("http://checkip.dyndns.com/")
        data = response.text
        return data.split(":")[-1].split("<")[0].strip()
    except:
        return "Unable to fetch IP"


def check_ip_security(ip_address):
    API_key = "PASTE_YOUR_REAL_API_KEY_HERE"

    try:
        response = requests.get(
            f"https://vpnapi.io/api/{ip_address}?key={API_key}"
        )
        data = response.json()

        if "security" in data:
            vpn = data["security"].get("vpn", False)
            proxy = data["security"].get("proxy", False)
        else:
            vpn = False
            proxy = False

        return vpn, proxy

    except:
        return False, False


def check_latency():
    try:
        start = time.time()
        requests.get("https://www.google.com", timeout=5)
        end = time.time()
        return (end - start) * 1000
    except:
        return 0


def print_header(title):
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title) + "\n")


while True:

    print_header("VPN IP Address Risk Analyzer")

    ip_address = get_ip_address()
    print(f"IP Address: {ip_address}")

    vpn, proxy = check_ip_security(ip_address)
    latency = check_latency()

    risk_score = 0

    if vpn:
        risk_score += 40

    if proxy:
        risk_score += 30

    if latency > 200:
        risk_score += 20

    if risk_score > 70:
        level = "High Risk"
    elif risk_score > 40:
        level = "Medium Risk"
    else:
        level = "Low Risk"

    if vpn:
        print("IP Address is using a VPN")
    else:
        print("IP Address is not using a VPN")

    if proxy:
        print("IP Address is using a Proxy")
    else:
        print("IP Address is not using a Proxy")

    print(f"Latency        : {int(latency)} ms")
    print(f"Risk Score     : {risk_score}")
    print(f"Risk Level     : {level}")

    choice = input("\nChoose an option:\n1 - Check again\n2 - Close\nOption: ")

    if choice == "1":
        continue
    elif choice == "2":
        break
    else:
        print("\nInvalid choice. Please try again.")