# Pickle Mobile Automation

This project contains a starter Appium automation suite for the Pickle mobile app, covering:

- Login flow
- OTP verification
- Template selection
- Image generation flow

## Tech stack

- Python 3.10+
- Pytest
- Appium Python Client
- Page Object Model (POM)

## Project layout

- `pickle_automation/` – reusable page objects and app driver helpers
- `tests/` – scenario tests for the app flows

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Appium server:
   ```bash
   appium
   ```

4. Configure your device/app in a `.env` file or by editing the capability values in `pickle_automation/config.py`.

## Example `.env`

```bash
APP_PATH=/path/to/pickle.apk
PLATFORM_NAME=Android
DEVICE_NAME=Pixel_6_API_34
APP_PACKAGE=com.pickleit.app.dev
APPIUM_SERVER=http://127.0.0.1:4723
``` 

## Claude Code skills

Open the project in Claude Code. Skills live in `.claude/skills/`.

**One-time / occasional (standalone, run only when needed):**

1. `pickle-setup-environment` - Java / Android SDK / emulator / Appium setup, once per machine (`source android-env.sh` sets the paths)
2. `pickle-add-app` - drop the APK in `apps/`; run again only when the build changes. It validates the build and updates `.env`

**Every automation:**

3. `pickle-automation-pipeline` - write a new automation from Jira / PRD / Figma (assumes setup is done)
4. `pickle-inspect-screen` - read real selectors from the running app (`scripts/inspect_screen.py`); the pipeline calls it automatically before generating the script
5. `pickle-run-tests` - start emulator + Appium and run the tests

## Running tests

```bash
source android-env.sh && source .venv/bin/activate
pytest tests/<file> -m mobile -v
```

Tests that tap Continue request a real OTP. They skip unless you pass a number you control and the dev OTP as environment variables (never commit them):

```bash
PHONE_NUMBER=+91XXXXXXXXXX DEFAULT_OTP=XXXX pytest tests/<file> -m mobile -v
```

## Notes

Selectors must come from the running app (`scripts/inspect_screen.py`), never be guessed. Any selector still marked `TODO selector` is an unverified placeholder.

The flow is intentionally structured around the product requirements:

- login by phone number
- OTP entry and validation
- template browsing and selection
- upload/pose validation
- generation trigger and result verification
