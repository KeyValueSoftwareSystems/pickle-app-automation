import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value if value is not None else default


APP_PATH = get_env("APP_PATH")
PLATFORM_NAME = get_env("PLATFORM_NAME", "Android")
DEVICE_NAME = get_env("DEVICE_NAME", "Pixel_6_API_34")
APP_PACKAGE = get_env("APP_PACKAGE", "com.pickle.app")
APPIUM_SERVER = get_env("APPIUM_SERVER", "http://127.0.0.1:4723")
TIMEOUT_SECONDS = int(get_env("TIMEOUT_SECONDS", "20"))
DEFAULT_OTP = get_env("DEFAULT_OTP", "123456")
PHONE_NUMBER = get_env("PHONE_NUMBER", "+919876543210")
