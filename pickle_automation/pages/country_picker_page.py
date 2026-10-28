from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.pages.base_page import BasePage


class CountryPickerPage(BasePage):
    TITLE = (AppiumBy.ACCESSIBILITY_ID, "Choose Country Code")
    SEARCH_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText")',
    )

    @staticmethod
    def _row(country: str):
        # Rows are exposed as "<Country>\n<+code>".
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionStartsWith("{country}\n")',
        )

    def is_visible(self):
        return self.is_displayed(*self.TITLE)

    def search(self, text: str):
        self.find_element(*self.SEARCH_INPUT).click()
        self.find_element(*self.SEARCH_INPUT).send_keys(text)

    def clear_search(self):
        self.find_element(*self.SEARCH_INPUT).clear()

    def has_country(self, country: str) -> bool:
        return self.is_displayed(*self._row(country))

    def listed_countries(self):
        return self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("\n+")',
        )

    def select_country(self, country: str):
        self.tap(*self._row(country))
