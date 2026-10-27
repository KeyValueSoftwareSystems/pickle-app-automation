"""ptp-login-flow: WhatsApp-based OTP login. Cases traced to automation_workspace/ptp-login-flow/testcases.md."""
import pytest

from pickle_automation.pages.country_picker_page import CountryPickerPage

OTP_SCREEN_TODO = "TODO selector: OTP screen not explored yet (needs a real number; Continue sends a real OTP)"


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
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc006_no_channel_selection_before_otp(login_page):
    """TC-006 (R6, R1)"""


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
@pytest.mark.smoke
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc010_otp_screen_content():
    """TC-010 (R1, R10)"""


@pytest.mark.mobile
@pytest.mark.regression
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc012_manual_four_digit_entry_enables_verify():
    """TC-012 (Flow 6)"""


@pytest.mark.mobile
@pytest.mark.regression
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc013_verify_disabled_with_incomplete_otp():
    """TC-013"""


@pytest.mark.mobile
@pytest.mark.regression
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc014_wrong_otp_rejected():
    """TC-014 (R7)"""


@pytest.mark.mobile
@pytest.mark.regression
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc015_change_returns_to_number_entry():
    """TC-015 (Flow 5)"""


@pytest.mark.mobile
@pytest.mark.regression
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc016_resend_timer_counts_down_from_30s():
    """TC-016 (R7, R10, D4)"""


@pytest.mark.mobile
@pytest.mark.regression
@pytest.mark.skip(reason=OTP_SCREEN_TODO)
def test_tc017_resend_available_after_timer_ends():
    """TC-017 (R7, R10)"""
