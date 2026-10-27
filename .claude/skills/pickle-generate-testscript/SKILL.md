---
name: pickle-generate-testscript
description: Stage 4 of the Pickle automation pipeline. Generates the automation script (page objects + tests) from approved test cases, then asks the user for runtime inputs such as phone number before running. Use after pickle-generate-testcases.
---

# Stage 4 - Generate and run the test script

## 1. Framework

**Appium + pytest (Python) only**: `pickle_automation/pages/*.py`, `tests/test_*.py`. Do not ask and do not generate Playwright specs.

## 2. Inspect the live screens (before generating anything)

Invoke the `pickle-inspect-screen` skill for every screen the approved test cases touch, so page objects use **verified selectors**, not guesses.

- Needs the emulator running with the app open and the Appium server up. If they are not, start them as in `pickle-run-tests` steps 1-2 (if the environment or APK is missing, tell the user to run `pickle-setup-environment` / `pickle-add-app` and stop).
- Walk only the screens that can be reached **without side effects**. Never tap Continue / Verify / Resend with a real number just to see the next screen, because it sends a real OTP. For screens that need it, ask the user for a number they control or mark the selectors `# TODO selector`.
- Keep a short table of screen, element and selector from the inspection and use it in step 3. Reuse selectors already present in `pickle_automation/pages/`; update the ones the inspection contradicts.

## 3. Generate

Follow the existing conventions - read `pickle_automation/pages/base_page.py`, `tests/test_pickles_generation_flow.py`, `tests/conftest.py` (or `tests/pickle-flow.spec.ts`) first.

- Appium: reuse/extend page objects (POM); add new pages only when needed. One test per approved TC, named `test_tc001_<slug>`, marked `@pytest.mark.mobile` plus `smoke`/`regression`. Selectors that are unknown go in as clearly marked placeholders (`# TODO selector`) - never fake them as real.
- Playwright: prefer role/label locators; one `test()` per TC.
- Add the TC id in a docstring/comment for traceability.
- **No hardcoded phone numbers, OTPs, or tokens.** Read them from `pickle_automation/config.py` (`PHONE_NUMBER`, `DEFAULT_OTP`, env) or `process.env`. Fix any existing hardcoded values only if the user agrees.

## 4. Collect run inputs (mandatory, before running)

Ask one at a time:

1. **Phone number** (with country code, e.g. `+91...`) - required for login flows.
2. **OTP** - ask whether to use the test OTP (`DEFAULT_OTP`) or enter a real one.
3. **Environment** - Appium: `APP_PATH`, device name, Appium server up?; Playwright: `BASE_URL`.
4. Any other input the chosen cases need (test photo path, template name).

Pass them **only as environment variables on the command**, e.g. `PHONE_NUMBER=... pytest -m smoke`; do not write them to `.env`, source files, or the workspace docs. Do not echo the phone number back in later summaries (mask it: `+91******3210`).

## 5. Confirm and run

Show the exact command (with the phone number masked) and ask: **Run now** / **Don't run - just keep the script**. If the Appium server or device is not available, say so instead of running.

- Appium: `PHONE_NUMBER=... APP_PATH=... .venv/bin/pytest -m <marker> tests/<file>`
- Playwright: `PHONE_NUMBER=... npx playwright test <file>`

## 6. Report

Report pass/fail per TC with failing output verbatim. Skipped tests (e.g. no `APP_PATH`) are reported as skipped, not passed. Update `status.md` to done.
