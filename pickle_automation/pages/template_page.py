from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.pages.base_page import BasePage


class TemplatePage(BasePage):
    CATEGORY_CARD = (AppiumBy.ID, "com.pickle.app:id/category_card")
    TEMPLATE_CARD = (AppiumBy.ID, "com.pickle.app:id/template_card")
    SEARCH_INPUT = (AppiumBy.ID, "com.pickle.app:id/search_input")

    def select_category(self, category_name: str):
        self.scroll_to_text(category_name)
        self.tap(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{category_name}")')

    def choose_template(self, template_name: str):
        self.scroll_to_text(template_name)
        self.tap(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{template_name}")')

    def search_template(self, template_name: str):
        self.type_text(*self.SEARCH_INPUT, template_name)
