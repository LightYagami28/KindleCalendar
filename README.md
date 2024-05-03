# KindleCalendar
Automate screenshots of your calendar and view them on the Kindle browser using Selenium.

![KindleCalendar](https://raw.githubusercontent.com/morrolinux/KindleCalendar/main/kindleCalendar.png?token=GHSAT0AAAAAABZERVYNQVD7HKC52IKX5PHWYZXAWEA)

## Getting Started

1. Log in to your Raspberry Pi or desired device.
2. Clone this repository: `git clone https://github.com/morrolinux/KindleCalendar.git`
3. Install Python dependencies: 
   ```bash
   cd KindleCalendar
   pip install -r requirements.txt
   cd ..
   ```
4. Install systemd user services: 
   ```bash
   cp KindleCalendar/config/systemd/user/* ~/.config/systemd/user/
   ```
5. Enable systemd services: 
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable kindleserver
   systemctl --user enable screenshot
   ```
6. Install Firefox and log in with your Google account.
7. Visit Google Calendar to ensure it loads correctly.
8. Install the Selenium WebDriver for Firefox. [Instructions here](https://firefox-source-docs.mozilla.org/testing/geckodriver/ARM.html)
9. Edit `KindleCalendar/screenshot.py` and set your Firefox profile path under `profile = webdriver.FirefoxProfile(...)`.
10. Install Node.js and npm: 
    ```bash
    sudo apt install nodejs npm
    ```
11. Install project dependencies with npm: 
    ```bash
    cd KindleCalendar
    npm i
    ```

If everything went well, you should be able to visit your Pi's IP address on port 8080 with any browser, including Kindle, but ensure JavaScript is enabled in the browser settings.

Enjoy!

Special thanks to [noxquest](https://bitbucket.org/ocampos/noxquest_kindle-tty/src/master/) for the awesome project and the `hixie` bridge node library :)
```