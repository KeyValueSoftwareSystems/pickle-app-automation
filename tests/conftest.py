import re

import pytest

from pickle_automation.config import PHONE_NUMBER
from pickle_automation.driver_factory import create_driver
from pickle_automation.pages.login_page import LoginPage


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
