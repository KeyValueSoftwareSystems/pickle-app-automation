import os

import pytest

from pickle_automation.config import DEFAULT_OTP, PHONE_NUMBER
from pickle_automation.driver_factory import create_driver
from pickle_automation.pages.generation_page import GenerationPage
from pickle_automation.pages.home_page import HomePage
from pickle_automation.pages.login_page import LoginPage
from pickle_automation.pages.otp_page import OtpPage
from pickle_automation.pages.template_page import TemplatePage


@pytest.mark.mobile
@pytest.mark.smoke
def test_login_otp_template_and_generation_flow():
    if not os.getenv("APP_PATH"):
        pytest.skip("APP_PATH is not set. Configure an app or APK to execute the E2E flow.")

    driver = create_driver()
    try:
        login_page = LoginPage(driver)
        assert login_page.is_login_screen_visible(), "Login screen is not visible"

        login_page.login(PHONE_NUMBER)

        otp_page = OtpPage(driver)
        otp_page.enter_otp(DEFAULT_OTP)
        otp_page.verify_otp()

        home_page = HomePage(driver)
        home_page.open_templates()

        template_page = TemplatePage(driver)
        template_page.select_category("Portrait")
        template_page.choose_template("Classic Portrait")

        generation_page = GenerationPage(driver)
        generation_page.confirm_generation()
        generation_page.upload_photo("/tmp/test_photo.jpg")
        generation_page.start_generation()
        generation_page.wait_for_result(timeout_seconds=120)

        assert generation_page.is_generation_complete(), "Image generation did not complete successfully"
    finally:
        driver.quit()
