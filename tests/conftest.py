import pytest

from pickle_automation.driver_factory import create_driver


@pytest.fixture
def driver():
    driver = create_driver()
    try:
        yield driver
    finally:
        driver.quit()
