import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException

from pickle_automation.pages.base_page import BasePage


class LoginPage(BasePage):
    # Flutter app: elements are exposed through accessibility descriptions / hints.
    WELCOME_LOGIN_LINK = (AppiumBy.ACCESSIBILITY_ID, "Log In")
    HEADING = (AppiumBy.ACCESSIBILITY_ID, "Login to Continue")
    PHONE_INPUT = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    COUNTRY_SELECTOR = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Choose Country Code")',
    )
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue")
    TERMS_LINK = (AppiumBy.ACCESSIBILITY_ID, "Terms & Conditions")
    PRIVACY_LINK = (AppiumBy.ACCESSIBILITY_ID, "Privacy Policy")
    OTP_SCREEN_TITLE = (AppiumBy.ACCESSIBILITY_ID, "Enter Verification Code")

    # Google "Choose a phone number" system sheet shown over the login screen.
    GOOGLE_HINT_CANCEL = (AppiumBy.ID, "com.google.android.gms:id/cancel")

    def open_from_welcome(self):
        self.tap(*self.WELCOME_LOGIN_LINK)
        self.dismiss_phone_hint_dialog()
        self.find_element(*self.HEADING)

    def dismiss_phone_hint_dialog(self, timeout_seconds=6):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            cancel = self.driver.find_elements(*self.GOOGLE_HINT_CANCEL)
            if cancel:
                cancel[0].click()
                return True
            time.sleep(0.5)
        return False

    def is_login_screen_visible(self):
        return self.is_displayed(*self.HEADING)

    def enter_phone_number(self, number: str):
        # The Flutter field is rebuilt on input, so re-find it before typing.
        self.find_element(*self.PHONE_INPUT).click()
        # Focusing the field can re-open the Google phone-number hint sheet.
        self.dismiss_phone_hint_dialog(timeout_seconds=3)
        self.find_element(*self.PHONE_INPUT).click()
        for _ in range(3):
            try:
                self.find_element(*self.PHONE_INPUT).send_keys(number)
                break
            except StaleElementReferenceException:
                time.sleep(0.5)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    def is_continue_enabled(self) -> bool:
        return self.find_element(*self.CONTINUE_BUTTON).get_attribute("clickable") == "true"

    def submit_phone_number(self):
        self.tap(*self.CONTINUE_BUTTON)

    def selected_country_description(self) -> str:
        return self.find_element(*self.COUNTRY_SELECTOR).get_attribute("content-desc")

    def open_country_picker(self):
        self.tap(*self.COUNTRY_SELECTOR)

    def is_otp_screen_visible(self, timeout_seconds=5):
        try:
            self.wait_for_description(self.OTP_SCREEN_TITLE[1], timeout_seconds)
            return True
        except Exception:
            return False

    def login(self, phone_number: str):
        """Enter the number and tap Continue. WhatsApp is the default channel; there is no channel choice."""
        self.enter_phone_number(phone_number)
        self.submit_phone_number()
