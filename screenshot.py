#!/usr/bin/env python3
import random
import signal
import sys
import os
import time
import locale
import logging
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import geckodriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Firefox, FirefoxOptions

# Constants
MOZILLA_PROFILE_PATH = "/home/pi/.mozilla/firefox/u41lkvuj.default-esr/"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1048
REFRESH_INTERVAL = 60 * 60  # 1 hour
SCREENSHOT_INTERVAL = 10 * 60  # 10 minutes
NIGHT_START_HOUR = 21
NIGHT_END_HOUR = 8
DATE_OFFSET_X = [130, 370, 600]

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Signal handler for graceful shutdown
def signal_handler(sig, frame: signal.Signals) -> None:
    logging.info("You pressed Ctrl+C! Closing browser.")
    browser.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Set locale
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")
geckodriver_autoinstaller.install()

# Configure Firefox profile and options
def create_browser() -> webdriver.Firefox:
    profile = webdriver.FirefoxProfile(MOZILLA_PROFILE_PATH)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference("useAutomationExtension", False)
    profile.set_preference("font.size.systemFontScale", 150)
    profile.update_preferences()

    opts = FirefoxOptions()
    opts.add_argument(f"--width={SCREEN_WIDTH}")
    opts.add_argument(f"--height={SCREEN_HEIGHT}")
    opts.add_argument("--headless")
    opts.set_preference("general.useragent.override", USER_AGENT)

    return webdriver.Firefox(firefox_profile=profile, desired_capabilities=DesiredCapabilities.FIREFOX, options=opts)

# Check if it's night time
def is_night_time() -> bool:
    current_hour = datetime.now().hour
    return NIGHT_END_HOUR < current_hour < NIGHT_START_HOUR

# Main function to capture screenshots
def capture_screenshots() -> None:
    browser = create_browser()
    actions = ActionChains(browser)
    actions.send_keys("t")  # goto: now
    logging.info("Initialization successful")

    try:
        i = 0
        while True:
            if is_night_time():
                logging.info("It's night time. Skipping screenshot.")
                time.sleep(REFRESH_INTERVAL)
                continue

            # Refresh the page every 60 minutes
            if i % 6 == 0:
                logging.info("Refreshing Google Calendar page...")
                browser.get("https://calendar.google.com")
                time.sleep(20 + random.randint(0, 5))  # Wait for the page to load

                # Zoom in the right amount
                browser.execute_script("document.body.style.MozTransform='scale(1.5)';")

            logging.info("Preparing to take a new screenshot...")
            if i % 3 == 0:
                try:
                    actions.perform()
                except Exception as e:
                    logging.error(f"Action chains error: {e}")

            # Take a screenshot of the time bar
            browser.execute_script("document.body.style.MozTransformOrigin = 'left 700px';")
            timebar = Image.open(BytesIO(browser.get_screenshot_as_png()))
            timebar = timebar.crop((15, 0, 57, timebar.size[1]))

            # Move to the current day position (horizontal)
            days_offsets = {
                "lunedì": '120px 700px',
                "martedì": '580px 700px',
                "mercoledì": '1060px 700px',
                "giovedì": '1540px 700px',
                "venerdì": '2020px 700px',
                "sabato": '2020px 700px',
                "domenica": '2020px 700px'
            }
            current_day_offset = days_offsets.get(datetime.now().strftime('%A'), '2020px 700px')
            browser.execute_script(f"document.body.style.MozTransformOrigin = '{current_day_offset}';")

            # Take a screenshot of Google Calendar and overlay the time bar
            gcal = Image.open(BytesIO(browser.get_screenshot_as_png()))
            gcal = gcal.crop((0, 0, 758, gcal.size[1]))
            Image.Image.paste(gcal, timebar)

            # Add date markers
            daysrange = [-1, 0, 1] if datetime.now().strftime("%A") in ["sabato", "domenica"] else [0, 1, 2]

            for idx, day_offset in enumerate(daysrange):
                dt = datetime.now() + timedelta(days=day_offset)
                datestring = dt.strftime("%A")[:3] + " " + str(dt.day)
                datemark = Image.new("RGBA", (100, 30), (255, 255, 255, 0))
                font = ImageFont.truetype("DejaVuSansMono-Bold", 26)
                draw = ImageDraw.Draw(datemark)
                draw.text((0, 0), datestring, (0, 0, 0), font=font)
                Image.Image.paste(gcal, datemark, (DATE_OFFSET_X[idx], 0), datemark)

            gcal.save("gcal.png")
            logging.info("Screenshot saved as gcal.png")
            time.sleep(SCREENSHOT_INTERVAL)
            i += 1

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    capture_screenshots()
