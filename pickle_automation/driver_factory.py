from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from pickle_automation.config import (
    APP_PACKAGE,
    APP_PATH,
    APPIUM_SERVER,
    DEVICE_NAME,
    PLATFORM_NAME,
)


def create_driver():
    if not APP_PATH:
        raise RuntimeError(
            "APP_PATH is not configured. Set the APK or app bundle path in the environment or .env file."
        )

    if PLATFORM_NAME.lower() == "android":
        options = UiAutomator2Options()
        options.platform_name = PLATFORM_NAME
        options.device_name = DEVICE_NAME
        options.app = APP_PATH
        options.app_package = APP_PACKAGE
        options.auto_grant_permissions = True
        options.no_reset = False
        return webdriver.Remote(APPIUM_SERVER, options=options)

    options = XCUITestOptions()
    options.platform_name = PLATFORM_NAME
    options.device_name = DEVICE_NAME
    options.app = APP_PATH
    options.auto_accept_alerts = True
    return webdriver.Remote(APPIUM_SERVER, options=options)
