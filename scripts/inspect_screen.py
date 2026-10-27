"""Print the interactive/labelled elements on the screen the app is currently showing.

Usage (emulator + Appium server running, app already open):
    source android-env.sh && .venv/bin/python scripts/inspect_screen.py [--tap "Log In"] [--screenshot out.png]

--tap  taps an element by accessibility description first (e.g. to reach the next screen).
Flutter apps expose labels as `content-desc`; text fields expose `hint`.
"""
import argparse
import re
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.config import APP_PACKAGE, APPIUM_SERVER, DEVICE_NAME


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tap", help="accessibility description to tap before dumping")
    parser.add_argument("--screenshot", help="save a screenshot to this path")
    parser.add_argument("--device", default="emulator-5554")
    args = parser.parse_args()

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = args.device or DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.no_reset = True  # attach to the running app, keep its current screen
    driver = webdriver.Remote(APPIUM_SERVER, options=options)
    try:
        if args.tap:
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, args.tap).click()
            time.sleep(3)
        for match in re.finditer(r"<([\w.]+)([^>]*?)/?>", driver.page_source):
            attrs = match.group(2)

            def get(key):
                found = re.search(r' %s="([^"]*)"' % key, attrs)
                return found.group(1) if found else ""

            if get("content-desc") or get("text") or get("hint") or match.group(1).endswith("EditText"):
                print(
                    f"{match.group(1).split('.')[-1]:10} desc={get('content-desc')!r} text={get('text')!r} "
                    f"hint={get('hint')!r} id={get('resource-id')!r} clickable={get('clickable')} bounds={get('bounds')}"
                )
        if args.screenshot:
            driver.get_screenshot_as_file(args.screenshot)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
