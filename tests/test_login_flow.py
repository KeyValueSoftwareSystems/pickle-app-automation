"""ptp-login-flow: WhatsApp-based OTP login. Cases traced to automation_workspace/ptp-login-flow/testcases.md."""
import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.pages.country_picker_page import CountryPickerPage
from pickle_automation.pages.home_page import HomePage

# Never equal to the dev OTP; used to exercise the invalid-OTP path.
WRONG_OTP = "1111"

# Tests taking the `otp_page` fixture tap Continue, which requests a real OTP.
# They are skipped unless PHONE_NUMBER is set in the environment (see tests/conftest.py).


@pytest.mark.mobile
@pytest.mark.smoke
def test_tc001_continue_disabled_with_empty_number(login_page):
    """TC-001 (R9)"""
    assert login_page.is_login_screen_visible()
    assert not login_page.is_continue_enabled()


@pytest.mark.mobile
@pytest.mark.smoke
def test_tc002_continue_enabled_after_entering_number(login_page, phone_digits):
    """TC-002 (R9)"""
    login_page.enter_phone_number(phone_digits)
    assert login_page.is_continue_enabled()


@pytest.mark.mobile
@pytest.mark.regression
def test_tc003_default_country_is_india(login_page):
    """TC-003"""
    assert login_page.selected_country_description().startswith("+91")


@pytest.mark.mobile
@pytest.mark.regression
def test_tc004_change_country_code_via_search(login_page):
    """TC-004 (Flow 4)"""
    login_page.open_country_picker()
    picker = CountryPickerPage(login_page.driver)
    assert picker.is_visible()

    picker.search("Ind")
    assert picker.has_country("India")
    assert picker.has_country("Indonesia")
    assert not picker.has_country("Afghanistan")

    picker.select_country("India")
    assert login_page.is_login_screen_visible()
    assert login_page.selected_country_description().startswith("+91")


@pytest.mark.mobile
@pytest.mark.regression
def test_tc005_country_search_with_no_match(login_page):
    """TC-005"""
    login_page.open_country_picker()
    picker = CountryPickerPage(login_page.driver)
    picker.search("zzzz")
    assert picker.listed_countries() == []

    picker.clear_search()
    assert picker.has_country("Afghanistan")


@pytest.mark.mobile
@pytest.mark.regression
def test_tc007_invalid_short_number_does_not_reach_otp(login_page):
    """TC-007 (R7)"""
    login_page.enter_phone_number("12345")
    if login_page.is_continue_enabled():
        login_page.submit_phone_number()
    assert not login_page.is_otp_screen_visible(timeout_seconds=4)
    assert login_page.is_login_screen_visible()


@pytest.mark.mobile
@pytest.mark.regression
def test_tc008_terms_and_privacy_links_present(login_page):
    """TC-008 (R8)"""
    assert login_page.is_displayed(*login_page.TERMS_LINK)
    assert login_page.is_displayed(*login_page.PRIVACY_LINK)


@pytest.mark.mobile
@pytest.mark.regression
def test_tc009_continue_with_no_network(login_page, phone_digits):
    """TC-009 (R7)"""
    driver = login_page.driver
    login_page.enter_phone_number(phone_digits)
    driver.execute_script("mobile: setConnectivity", {"wifi": False, "data": False})
    try:
        login_page.submit_phone_number()
        assert not login_page.is_otp_screen_visible(timeout_seconds=6)
    finally:
        driver.execute_script("mobile: setConnectivity", {"wifi": True, "data": True})


@pytest.mark.mobile
@pytest.mark.regression
def test_tc006_no_channel_selection_before_otp(otp_page):
    """TC-006 (R6, R1): Continue goes straight to the OTP screen, with no WhatsApp/SMS choice."""
    driver = otp_page.driver
    assert otp_page.is_visible()
    assert driver.find_elements(
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("SMS")'
    ) == []
    assert otp_page.is_displayed(*otp_page.WHATSAPP_ICON)  # indicator only, not an option


@pytest.mark.mobile
@pytest.mark.smoke
def test_tc010_otp_screen_content(otp_page, phone_digits):
    """TC-010 (R1, R10): OTP screen shows number, WhatsApp indicator, Change, Verify and a 30s countdown."""
    assert otp_page.is_displayed(*otp_page.TITLE)
    assert otp_page.is_displayed(*otp_page.WHATSAPP_ICON)
    assert otp_page.shows_number(phone_digits)
    assert otp_page.is_displayed(*otp_page.CHANGE_LINK)
    assert otp_page.is_displayed(*otp_page.OTP_INPUT)
    assert not otp_page.is_verify_enabled()
    assert 25 <= otp_page.countdown_seconds() <= 30


@pytest.mark.mobile
@pytest.mark.smoke
def test_tc011_verify_with_correct_otp(otp_page, otp_value):
    """TC-011 (R1, R2, R11): the dev OTP verifies, "Successfully Verified" shows, then Home loads."""
    otp_page.enter_otp(otp_value)
    assert otp_page.is_verified(), "Successfully Verified message did not appear"
    assert HomePage(otp_page.driver).is_loaded(), "Home screen did not load after verification"


@pytest.mark.mobile
@pytest.mark.regression
def test_tc012_manual_four_digit_entry_enables_verify(otp_page):
    """TC-012 (Flow 6): typing 4 digits fills the boxes and enables Verify.

    Observed: the app also auto-submits on the 4th digit, so an invalid code shows the error.
    """
    otp_page.enter_otp(WRONG_OTP)
    assert otp_page.typed_otp() == WRONG_OTP
    assert otp_page.is_verify_enabled()


@pytest.mark.mobile
@pytest.mark.regression
def test_tc013_verify_disabled_with_incomplete_otp(otp_page):
    """TC-013"""
    otp_page.enter_otp("12")
    assert otp_page.typed_otp() == "12"
    assert not otp_page.is_verify_enabled()


@pytest.mark.mobile
@pytest.mark.regression
def test_tc014_wrong_otp_rejected(otp_page):
    """TC-014 (R7): a wrong OTP shows "Invalid or expired OTP" and keeps the user on the OTP screen."""
    otp_page.enter_otp(WRONG_OTP)
    assert otp_page.is_error_visible()
    assert otp_page.is_displayed(*otp_page.TITLE)
    assert not otp_page.is_verified(timeout_seconds=2)


@pytest.mark.mobile
@pytest.mark.regression
def test_tc015_change_returns_to_number_entry(otp_page, login_page):
    """TC-015 (Flow 5)"""
    otp_page.tap_change()
    assert login_page.is_login_screen_visible()
    assert login_page.is_displayed(*login_page.PHONE_INPUT)


@pytest.mark.mobile
@pytest.mark.regression
def test_tc016_resend_timer_counts_down_from_30s(otp_page):
    """TC-016 (R7, R10, D4)"""
    first = otp_page.countdown_seconds()
    assert 25 <= first <= 30
    time.sleep(4)
    assert otp_page.countdown_seconds() < first
    assert not otp_page.is_resend_available()


@pytest.mark.mobile
@pytest.mark.regression
def test_tc017_resend_available_after_timer_ends(otp_page):
    """TC-017 (R7, R10): after ~30s the countdown is replaced by an enabled "Resend Code" button."""
    otp_page.wait_for_resend(timeout_seconds=40)
    assert otp_page.is_resend_available()
    assert not otp_page.driver.find_elements(*otp_page.COUNTDOWN)
