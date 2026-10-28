from selenium.common.exceptions import TimeoutException
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

    def is_present(self, by, value, timeout=2, poll_frequency=0.5):
        """True if the element appears within `timeout` seconds.

        Only a timeout means "absent"; other errors (e.g. a dropped Appium session) propagate.
        Use this for negative checks and for short-lived UI such as toasts.
        """
        try:
            WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def is_displayed(self, by, value):
        """Wait up to TIMEOUT_SECONDS for the element (for checks that are expected to pass)."""
        return self.is_present(by, value, timeout=TIMEOUT_SECONDS)

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
