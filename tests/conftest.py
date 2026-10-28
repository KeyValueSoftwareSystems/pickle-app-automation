import os
import re

import pytest

from pickle_automation.config import DEFAULT_OTP, PHONE_NUMBER
from pickle_automation.driver_factory import create_driver
from pickle_automation.pages.login_page import LoginPage
from pickle_automation.pages.otp_page import OtpPage


@pytest.fixture
def driver():
    driver = create_driver()
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def phone_digits():
    """National part of PHONE_NUMBER (last 10 digits), taken from env/config, never hardcoded."""
    return re.sub(r"\D", "", PHONE_NUMBER)[-10:]


@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open_from_welcome()
    return page


@pytest.fixture
def otp_value():
    """Fixed dev OTP from the environment (DEFAULT_OTP); never hardcoded."""
    if not DEFAULT_OTP:
        pytest.skip("DEFAULT_OTP is not set (pass the dev OTP as an environment variable)")
    return DEFAULT_OTP


@pytest.fixture
def otp_page(login_page, phone_digits):
    """Request an OTP and land on the OTP screen.

    Tapping Continue sends a real OTP, so this only runs when PHONE_NUMBER is set explicitly
    in the environment (the config default is a dummy number that must never be used here).
    """
    if not os.getenv("PHONE_NUMBER"):
        pytest.skip("PHONE_NUMBER is not set in the environment; refusing to request a real OTP")
    login_page.login(phone_digits)
    page = OtpPage(login_page.driver)
    assert page.is_visible(), "OTP screen did not appear after Continue"
    return page
