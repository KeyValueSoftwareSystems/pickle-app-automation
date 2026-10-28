# AGENTS.md

Guidance for AI coding agents working in this repo. Humans: see `README.md`.

## What this project is

Appium + pytest (Python 3.10+) UI automation for the **Pickle** Android app (Flutter, dev debug build `com.pickleit.app.dev`), run on an Android emulator. **Appium only: do not add Playwright, Selenium web tests, npm or TypeScript.**

## Layout

```
pickle_automation/        config.py, driver_factory.py, pages/ (page objects, one class per screen)
tests/                    conftest.py (fixtures), test_*.py (one test per approved test case)
automation_workspace/<feature>/   sources.md, context.md, testcases.md, status.md for each feature
scripts/inspect_screen.py dump the live screen's selectors
android-env.sh            source it first: JAVA_HOME, ANDROID_HOME, PATH
apps/                     the APK (gitignored; never commit binaries)
.claude/skills/           Claude Code skills (see below)
```

## Run

```bash
source android-env.sh && source .venv/bin/activate
emulator -avd Pixel_6_API_34 -no-snapshot -no-audio -no-window -gpu host &   # wait for boot: adb devices
appium &                                                   # port 4723, no /wd/hub base path
pytest tests/<file> -m mobile -v
```

Config comes from `.env` (gitignored) and environment variables: `APP_PATH`, `APP_PACKAGE`, `APPIUM_SERVER`, `PHONE_NUMBER`, `DEFAULT_OTP`.

## Hard rules

1. **Never write phone numbers, OTPs or tokens into any file** (code, docs, `.env`, commits, memory). Pass them as env vars on the command, and mask them (`+91******1234`) when reporting.
2. **Tapping Continue on the login screen requests a real OTP.** Only do it with a number the user gave you for this purpose. Tests that do so must skip unless `PHONE_NUMBER` is set in the environment (see the `otp_page` fixture). `PHONE_NUMBER` and `DEFAULT_OTP` default to `None` in `config.py` and are blank in `.env.example`, so nothing can send an OTP by accident.
3. **Never invent selectors.** Read them from the running app (`scripts/inspect_screen.py`). If unknown, use a clearly marked `# TODO selector`, never a fake that looks real.
4. Do not change or delete files outside the task. Ask before large downloads, `sudo`, or editing shell profiles.
5. Report results faithfully: failing output verbatim, skipped is not passed.

## Conventions

- Page Object Model: one class per screen in `pickle_automation/pages/`, extending `BasePage`. Tests contain assertions, page objects contain locators and actions.
- Test naming: `test_tc<NNN>_<slug>`, docstring starts with the TC id and the rule it traces to (`"""TC-014 (R7)"""`).
- Markers (see `pytest.ini`): `@pytest.mark.mobile` on every test, plus `smoke` or `regression`.
- Keep `testcases.md` in sync: every test maps to a TC; manual-only cases are listed there with `Automate: no`.
- Match the surrounding code's style and comment density.

## Flutter / UiAutomator2 gotchas

- Labels are `content-desc` -> `AppiumBy.ACCESSIBILITY_ID`. List rows look like `"India\n+91"`. Text fields are `android.widget.EditText` (placeholder in `hint`).
- A Flutter button is disabled when `clickable == "false"` (not `enabled`).
- Fields rebuild when text changes: re-find the element instead of reusing it (`StaleElementReferenceException`).
- Google's "Choose a phone number" sheet (`com.google.android.gms:id/cancel`) covers the login screen on arrival and when the phone field is focused: `LoginPage.dismiss_phone_hint_dialog()`.
- The OTP field is one `EditText` behind 4 boxes and **auto-submits on the 4th digit**.
- Do not send raw keycodes like backspace to Flutter fields mid-test.
- The emulator needs 4 GB RAM (`hw.ramSize = 4096`) and must run **headless with hardware rendering**: `emulator -avd Pixel_6_API_34 -no-snapshot -no-audio -no-window -gpu host`. Software rendering segfaults it on the post-login home screen, and `-gpu host` with a visible window can lose its GL context mid-run.
- Never use broad `pkill -f`: stop the emulator with `kill $(pgrep -x qemu-system-x86)`.

## Claude Code skills (`.claude/skills/`)

| Skill | Purpose |
|---|---|
| `pickle-setup-environment` | One-time machine setup (standalone, not part of the pipeline) |
| `pickle-add-app` | Validate and register a new APK (standalone) |
| `pickle-automation-pipeline` | Entry point: Jira/PRD/Figma -> context -> test cases -> script (with approval gates) |
| `pickle-collect-docs`, `pickle-generate-context`, `pickle-generate-testcases`, `pickle-generate-testscript` | Pipeline stages 1 to 4 |
| `pickle-inspect-screen` | Read real selectors from the running app (called first in stage 4) |
| `pickle-run-tests` | Start emulator and Appium, run tests, report per TC |

Other AI tools can follow the same steps by reading the `SKILL.md` files directly.
