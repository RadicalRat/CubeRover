import subprocess
import sys

wifi = "CubeRover"

class SetAuto:

    def __init__(self):
        self.availtrue = False
        self.availfalse = False
        self.connectedmes = False

        self.avail_networks = []
        self.profiles = []

    #internal, gives list of all wifi profiles on autoconnect that is also currently available
    def all_wifis(self):
        try:
            output = subprocess.check_output('netsh wlan show profiles', shell=True).decode()
            for line in output.splitlines():
                if "All User Profile" in line:
                    if line.split(":", 1)[1].strip() != wifi and line.split(":", 1)[1].strip() in self.avail_networks:
                        self.profiles.append(line.split(":", 1)[1].strip())
        except:
            pass

    def available(self): #checks if hotspot is available

        #scan available wifi networks
        try:
            output = subprocess.run(['netsh', 'wlan', 'show', 'networks'],
                                    capture_output = True,
                                    text=True,
                                    check = True)
            
            for line in output.stdout.splitlines():
                if "SSID" in line:
                    ssid = line.split(":", 1)[1].strip()
                    if ssid:
                        self.avail_networks.append(ssid)
                        
            #print(self.avail_networks)

            
            
            if wifi in self.avail_networks:
                if not self.availtrue:
                    print("Wifi Detected")
                    self.availtrue = True
                return True
            
            if not self.availfalse:
                print("Wifi not detected.")
                self.availfalse = True

            return False
        except:
            return True


    def if_connect(self): #check if currently connected to hotspot
        try:
            output = subprocess.check_output('netsh wlan show interfaces', shell=True).decode()
            for line in output.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    connected = line.split(":", 1)[1].strip()
            
            if connected == wifi:
                return True
            elif not self.connectedmes:
                print(f"Currently connected to {connected}.")
                self.connectedmes = True
            
            return False
        
        except:
            print("Error detecting connection.")
            return None
        
    
    def disable_auto(self):
        self.all_wifis()
        try:
            for profile in self.profiles:
                subprocess.run(f'netsh wlan set profileparameter name="{profile}" connectionmode=manual', shell=True, capture_output=True)
        except:
            pass


    def enable_auto(self):
        try:
            for profile in self.profiles:
                subprocess.run(f'netsh wlan set profileparameter name="{profile}" connectionmode=auto', shell=True)
        except:
            pass






