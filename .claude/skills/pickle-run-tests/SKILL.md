---
name: pickle-run-tests
description: Boot the emulator, start the Appium server and run Pickle pytest suites (by file, marker or test id), then report pass/fail per test case. Use when the user asks to run, rerun or debug the Pickle automation.
---

# Run the Pickle Appium tests

Appium + pytest only. Prerequisites: `pickle-setup-environment` and `pickle-add-app` done.

## 1. Start the emulator (skip if `adb devices` already lists one)

```bash
source android-env.sh
nohup emulator -avd Pixel_6_API_34 -no-snapshot -no-audio > <scratchpad>/emu.log 2>&1 &
timeout 280 bash -c 'until [ "$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d "\r")" = 1 ]; do sleep 5; done'
adb devices
```

Run it in the background; boot takes about 30 s with KVM.

## 2. Start Appium (skip if `curl -s localhost:4723/status` answers)

```bash
source android-env.sh && setsid nohup appium > <scratchpad>/appium.log 2>&1 < /dev/null &
```

The driver factory uses `APPIUM_SERVER` from `.env` as-is (default `http://127.0.0.1:4723`, **no `/wd/hub`**).

## 3. Collect run inputs (ask one at a time, only what the chosen tests need)

- Which tests: a file, a marker (`smoke`, `regression`, `mobile`) or a test id.
- Phone number (with country code) only for tests that submit a real login; most login-screen tests only type a number and send nothing.
- OTP: use the fixed dev OTP once the backend provides it; never write it to files.

Pass secrets only as env vars on the command, e.g. `PHONE_NUMBER=... pytest ...`. **Never echo them back**; mask as `+91******3210`. Warn the user before any test that taps Continue with a real number, because it sends a real OTP.

## 4. Confirm, then run

Show the exact command (numbers masked) and ask **Run now** / **Don't run**.

```bash
source android-env.sh && .venv/bin/pytest tests/<file> -m mobile -v -p no:cacheprovider
# optional HTML report: --html=report.html --self-contained-html
```

Each test resets the app, so a full file takes minutes (8 tests took about 4 min). Use a long timeout or run in the background.

## 5. Report

Pass/fail/skip per TC id (docstrings carry the TC id), failing output verbatim. **Skipped is not passed.** Name any common cause you recognise:

| Symptom | Cause |
|---|---|
| `404` on session create | Server URL has `/wd/hub` (Appium 2 has no base path) |
| `NoSuchElement` on the phone field | Google "Choose a phone number" sheet covers the app; `LoginPage.dismiss_phone_hint_dialog()` handles it |
| `StaleElementReferenceException` on Flutter fields | Re-find the element after typing (the field is rebuilt) |
| Session creation hangs or `INSTALL_FAILED_*` | Re-run `pickle-add-app` |
| `adb devices` empty / UiAutomator2 "instrumentation process is not running" mid-run | The emulator froze (usually the post-login home screen on a small or software-rendered AVD). Check the AVD sizing in `pickle-setup-environment`, then `adb kill-server`, stop the emulator by exact process name (`kill $(pgrep -x qemu-system-x86)`, never a broad `pkill -f`, which can kill Appium/your shell), and boot it again |
| Tests that tap Continue are skipped | They need `PHONE_NUMBER` set in the environment (a number you control) and `DEFAULT_OTP` for the verify tests |

Leave the emulator and Appium running unless the user asks to stop them.
