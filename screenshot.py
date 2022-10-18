#!/usr/bin/env python3
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import random
import signal
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
from datetime import datetime, timedelta
import locale
import time
import os


def signal_handler(sig, frame):
	global browser
	print("You pressed Ctrl+C!")
	browser.close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# geckodriver_autoinstaller.install()

locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")

# CHANGE THIS TO YOUR MOZILLA PROFILE PATH
profile = webdriver.FirefoxProfile(
    "/home/pi/.mozilla/firefox/u41lkvuj.default-esr/")

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference("useAutomationExtension", False)
profile.set_preference("font.size.systemFontScale", 150)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

opts = FirefoxOptions()
# opts.add_argument("--width=758")
# opts.add_argument("--width=1280")
opts.add_argument("--width=1200")
# opts.add_argument("--height=1024")
opts.add_argument("--height=1048")
opts.add_argument("--headless")
opts.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36")

browser = webdriver.Firefox(firefox_profile=profile,
                           desired_capabilities=desired,
                           options=opts)


def night():
    return (datetime.now().hour < 8) or (datetime.now().hour > 21)


try:
	i = -1
	actions = ActionChains(browser)
	# actions.send_keys("d")	# daily view
	actions.send_keys("t")	# goto: now

	# browser.get("https://calendar.google.com")
	# time.sleep(20)
	# browser.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/header/div[2]/div[1]/div[1]").click()
	print("init successful")

	while True:

		i = i+1

		if night():
			gcal = Image.new("RGBA", (758, 1048), (255,255,255,255))
			gcal.save("gcal.png")
			time.sleep(60*60)
			continue

		# refresh page every 60 minutes
		if (i%6) == 0:
			print("refresh page...")
			browser.get("https://calendar.google.com")
			# browser.refresh()
			time.sleep(20 + random.randrange(0,5))
			# browser.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/header/div[2]/div[1]/div[1]").click()

			# zoom in the right amount
			browser.execute_script("document.body.style.MozTransform='scale(1.5)';")


		print("preparing to take a new screenshot...")
		if (i%3) == 0:
			try:
				actions.perform()
			except Exception as e:
				print(e)

		# take a screenshot of the time bar
		browser.execute_script("document.body.style.MozTransformOrigin = 'left 700px';")
		timebar = Image.open(BytesIO(browser.get_screenshot_as_png()))
		# timebar = timebar.crop((25,0,90,timebar.size[1]))
		timebar = timebar.crop((15,0,57,timebar.size[1]))

		# move to the current day position (horizontal)
		if datetime.now().strftime("%A") == "lunedì":
			browser.execute_script("document.body.style.MozTransformOrigin = '120px  700px';")
		if datetime.now().strftime("%A") == "martedì":
			browser.execute_script("document.body.style.MozTransformOrigin = '580px  700px';")
		if datetime.now().strftime("%A") == "mercoledì":
			browser.execute_script("document.body.style.MozTransformOrigin = '1060px 700px';")
		if datetime.now().strftime("%A") == "giovedì":
			browser.execute_script("document.body.style.MozTransformOrigin = '1540px 700px';")
		if datetime.now().strftime("%A") in ["venerdì", "sabato", "domenica"]:
			browser.execute_script("document.body.style.MozTransformOrigin = '2020px 700px';")

		# take a screenshot of google calendar, crop it to screen size and overlay the time bar
		gcal = Image.open(BytesIO(browser.get_screenshot_as_png()))
		gcal = gcal.crop((0,0,758,gcal.size[1]))
		Image.Image.paste(gcal, timebar)

		dateoffsets = [130, 370, 600]

		if datetime.now().strftime("%A") == "sabato":
			daysrange = [-1, 0, 1]
		elif datetime.now().strftime("%A") == "domenica":
			daysrange = [-2, -1, 0]
		else:
			daysrange = [0, 1, 2]

		for i, idx in enumerate(daysrange):
			# datestring = str(datetime.now().day+i) + "/" + str(datetime.now().month)
			dt = datetime.now()+timedelta(days=idx)
			datestring = dt.strftime("%A")[:3] + " " + str(dt.day)
			datemark = Image.new("RGBA", (100, 30), (255,255,255,0))
			font = ImageFont.truetype("DejaVuSansMono-Bold", 26)
			draw = ImageDraw.Draw(datemark)
			draw.text((0, 0),datestring,(0,0,0),font=font)
			Image.Image.paste(gcal, datemark, (dateoffsets[i],0), datemark)

		# if night():
		# 	moon = Image.open("moon.png")
		# 	Image.Image.paste(gcal, moon, (int(gcal.width/2-moon.width/2), int(gcal.height/2-moon.height/2)), moon)

		gcal.save("gcal.png")
		print("screenshot ok")

		time.sleep(600)

finally:
	browser.quit()
