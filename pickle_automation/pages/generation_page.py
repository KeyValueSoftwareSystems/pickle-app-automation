from appium.webdriver.common.appiumby import AppiumBy

from pickle_automation.pages.base_page import BasePage


class GenerationPage(BasePage):
    UPLOAD_BUTTON = (AppiumBy.ID, "com.pickle.app:id/upload_photo_button")
    GENERATE_BUTTON = (AppiumBy.ID, "com.pickle.app:id/generate_button")
    CONFIRM_BUTTON = (AppiumBy.ID, "com.pickle.app:id/confirm_button")
    GENERATION_STATUS = (AppiumBy.ID, "com.pickle.app:id/generation_status")
    RESULT_IMAGE = (AppiumBy.ID, "com.pickle.app:id/generated_image")

    def upload_photo(self, file_path: str):
        self.tap(*self.UPLOAD_BUTTON)
        # Appium can select a system file picker for image upload.
        # This is intentionally generic; real implementation depends on OS/UI.
        self.driver.push_file(file_path, file_path)

    def start_generation(self):
        self.tap(*self.GENERATE_BUTTON)

    def confirm_generation(self):
        if self.is_displayed(*self.CONFIRM_BUTTON):
            self.tap(*self.CONFIRM_BUTTON)

    def wait_for_result(self, timeout_seconds=120):
        self.wait_for_text("Generating", timeout_seconds)
        self.wait_for_text("Complete", timeout_seconds)

    def is_generation_complete(self):
        return self.is_displayed(*self.RESULT_IMAGE)
