import os

from dotenv import load_dotenv

load_dotenv()

APP_PATH = os.getenv("APP_PATH")
PLATFORM_NAME = os.getenv("PLATFORM_NAME", "Android")
DEVICE_NAME = os.getenv("DEVICE_NAME", "Pixel_6_API_34")
APP_PACKAGE = os.getenv("APP_PACKAGE", "com.pickleit.app.dev")
APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "20"))

# Pass these per run via the environment and never commit real values.
# Unset or empty means "not provided": tests that need them skip.
DEFAULT_OTP = os.getenv("DEFAULT_OTP") or None
PHONE_NUMBER = os.getenv("PHONE_NUMBER") or None
