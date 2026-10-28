from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.pages.base_page import BasePage


class HomePage(BasePage):
    # Verified against the dev build (accessibility descriptions on the bottom navigation).
    HOME_TAB = (AppiumBy.ACCESSIBILITY_ID, "Home")
    SEARCH_TAB = (AppiumBy.ACCESSIBILITY_ID, "Search")
    MY_STUDIO_TAB = (AppiumBy.ACCESSIBILITY_ID, "My Studio")
    PROFILE_TAB = (AppiumBy.ACCESSIBILITY_ID, "Profile")
    EXPLORE_TAB = (AppiumBy.ACCESSIBILITY_ID, "Explore")
    # TODO selector: placeholder, there is no "Templates" tab on the home screen of this build.
    TEMPLATES_TAB = (AppiumBy.ID, "com.pickle.app:id/nav_templates")

    def is_loaded(self, timeout_seconds=15):
        try:
            self.wait_for_description("Explore", timeout_seconds)
            return self.is_displayed(*self.SEARCH_TAB)
        except Exception:
            return False

    def open_templates(self):
        self.tap(*self.TEMPLATES_TAB)

    def open_my_studio(self):
        self.tap(*self.MY_STUDIO_TAB)

    def open_profile(self):
        self.tap(*self.PROFILE_TAB)
