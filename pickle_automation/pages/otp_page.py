from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from pickle_automation.pages.base_page import BasePage


class OtpPage(BasePage):
    # Flutter app: one EditText sits behind the 4 visual OTP boxes; labels are accessibility descriptions.
    TITLE = (AppiumBy.ACCESSIBILITY_ID, "Enter Verification Code")
    OTP_INPUT = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    VERIFY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Verify")
    CHANGE_LINK = (AppiumBy.ACCESSIBILITY_ID, "Change")
    WHATSAPP_ICON = (AppiumBy.ACCESSIBILITY_ID, "WhatsApp")
    COUNTDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionStartsWith("Resend code in")')
    RESEND_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Resend Code")
    ERROR_MESSAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Invalid or expired OTP")')
    SUCCESS_MESSAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionStartsWith("Successfully Verified")')

    def is_visible(self, timeout_seconds=15):
        try:
            WebDriverWait(self.driver, timeout_seconds).until(
                lambda d: d.find_elements(*self.TITLE)
            )
            return True
        except Exception:
            return False

    def shows_number(self, digits: str) -> bool:
        return self.is_displayed(
            AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{digits}")'
        )

    def enter_otp(self, otp_code: str):
        """Type the code. The app auto-submits when the 4th digit is entered."""
        self.find_element(*self.OTP_INPUT).send_keys(otp_code)

    def typed_otp(self) -> str:
        return self.find_element(*self.OTP_INPUT).text

    def is_verify_enabled(self) -> bool:
        return self.find_element(*self.VERIFY_BUTTON).get_attribute("clickable") == "true"

    def verify_otp(self):
        self.tap(*self.VERIFY_BUTTON)

    def countdown_seconds(self) -> int:
        description = self.find_element(*self.COUNTDOWN).get_attribute("content-desc")
        return int("".join(ch for ch in description if ch.isdigit()))

    def is_resend_available(self) -> bool:
        return bool(self.driver.find_elements(*self.RESEND_BUTTON))

    def wait_for_resend(self, timeout_seconds=40):
        WebDriverWait(self.driver, timeout_seconds).until(lambda d: d.find_elements(*self.RESEND_BUTTON))

    def resend_code(self):
        self.tap(*self.RESEND_BUTTON)

    def tap_change(self):
        self.tap(*self.CHANGE_LINK)

    def is_error_visible(self, timeout_seconds=8) -> bool:
        try:
            WebDriverWait(self.driver, timeout_seconds).until(lambda d: d.find_elements(*self.ERROR_MESSAGE))
            return True
        except Exception:
            return False

    def is_verified(self, timeout_seconds=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout_seconds).until(lambda d: d.find_elements(*self.SUCCESS_MESSAGE))
            return True
        except Exception:
            return False
