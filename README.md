# Keylogger-WifiGraber
Keylogger: Logs user keyboard inputs, captures text, and saves it into a file for analysis.
WiFi Credential Extractor: Retrieves saved WiFi profiles and password and the IP Address of the user and logs them into a file.

**Disclaimer: This code is for educational purposes only. Always ensure you have permission before running this program on any system.**

# Requirements
- Python 3.8 or later
- Required Python libraries: pynput
- Windows OS (as code runs in terminal)

# Installation
1. Clone the repository
 `git clone https://github.com/Codexx121/Keylogger-WifiGrabert.git`


 - **Install Dependencies if not yet installed**
 `pip install pynput`


2. Run using python
   `python keylogger_wifi.py`

   **Altenatively it can be run using the executable (.exe) file**
3. To Exit terminate via task manager or `Ctrl + C` 

# Functionality
**Keylogger**
- The keylogger runs in the background and logs all keyboard activity to logs.txt.
- Pressed keys are buffered and written to the file every 5 seconds so that special keys and inputs can be accounted for.
- Handles backspace, space, Enter, Shift, and Caps Lock inputs correctly.

  
**WiFi Credential Extractor**
- Uses netsh commands to retrieve saved WiFi profiles and their passwords.
- Logs extracted WiFi credentials and the IPv6 address to wifi.txt.

# Warnings
Unauthorized use of this tool can have serious legal consequences.
Use at own risk. 
I am not liable for any damages incurred in the usage of this tool.
