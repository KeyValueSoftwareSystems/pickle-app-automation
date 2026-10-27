from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.pages.base_page import BasePage


class HomePage(BasePage):
    TEMPLATES_TAB = (AppiumBy.ID, "com.pickle.app:id/nav_templates")
    MY_STUDIO_TAB = (AppiumBy.ID, "com.pickle.app:id/nav_my_studio")
    PROFILE_TAB = (AppiumBy.ID, "com.pickle.app:id/nav_profile")

    def open_templates(self):
        self.tap(*self.TEMPLATES_TAB)

    def open_my_studio(self):
        self.tap(*self.MY_STUDIO_TAB)

    def open_profile(self):
        self.tap(*self.PROFILE_TAB)
