from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.config import TIMEOUT_SECONDS


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT_SECONDS)

    def find_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def tap(self, by, value):
        element = self.find_element(by, value)
        element.click()

    def type_text(self, by, value, text):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def is_displayed(self, by, value):
        try:
            self.find_element(by, value)
            return True
        except Exception:
            return False

    def wait_for_text(self, text, timeout_seconds=None):
        timeout = timeout_seconds or TIMEOUT_SECONDS
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')))

    def wait_for_description(self, description, timeout_seconds=None):
        wait = WebDriverWait(self.driver, timeout_seconds or TIMEOUT_SECONDS)
        return wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, description)))

    def scroll_to_text(self, text):
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))',
        )
