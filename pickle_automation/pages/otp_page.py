from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.pages.base_page import BasePage


class OtpPage(BasePage):
    OTP_INPUT = (AppiumBy.ID, "com.pickle.app:id/otp_input")
    VERIFY_BUTTON = (AppiumBy.ID, "com.pickle.app:id/verify_otp_button")
    RESEND_BUTTON = (AppiumBy.ID, "com.pickle.app:id/resend_code_button")

    def enter_otp(self, otp_code: str):
        self.type_text(*self.OTP_INPUT, otp_code)

    def verify_otp(self):
        self.tap(*self.VERIFY_BUTTON)

    def resend_code(self):
        self.tap(*self.RESEND_BUTTON)
