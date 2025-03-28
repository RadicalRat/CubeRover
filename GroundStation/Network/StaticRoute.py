import subprocess
import sys

def available():
    try:
        #scan available wifi networks
        networks = subprocess.run(['netsh', 'wlan', 'show', 'networks'],
                                  capture_output = True,
                                  text=True,
                                  check = True)
        print(networks)
        
        if "cuberover" in networks.stdout.lower():
            return True
        
        return False

    except subprocess.CalledProcessError as e:
        print("error", e)
        return False

def add_route():
    try:
        cmd = ["route", "add", "10.42.0.1", "mask", "255.255.255.255",
               "10.42.0.255", "metric", "1", "if", str()]
        #subprocess.run("sudo")
    except:
        return
    

print(available())
