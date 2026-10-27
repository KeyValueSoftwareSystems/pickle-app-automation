---
name: pickle-inspect-screen
description: Discover real element selectors from the running Pickle app (accessibility descriptions, hints, bounds, enabled state) so page objects use verified selectors instead of placeholders. Use before writing or fixing page objects and tests, or when a test cannot find an element.
---

# Inspect the live app for selectors

Never invent selectors. Read them from the running app.

## Prerequisites

Emulator running with the app open on the screen of interest, Appium server up (`pickle-run-tests` steps 1-2).

## Dump the current screen

```bash
source android-env.sh && .venv/bin/python scripts/inspect_screen.py --screenshot <scratchpad>/screen.png
```

`--tap "<accessibility description>"` taps an element first, to reach the next screen (for example `--tap "Log In"`). It attaches to the running app without resetting it. Look at the screenshot too (Read the PNG) to match elements to what is on screen.

## Reading the output (Flutter app)

- Labels appear as `content-desc` (use `AppiumBy.ACCESSIBILITY_ID`). List rows are `"<Name>\n<value>"`, for example `India\n+91`; match with `UiSelector().descriptionStartsWith("India\n")`.
- Text fields are `android.widget.EditText` with the placeholder in `hint`. The hint disappears once text is typed.
- A Flutter button's disabled state is **not** `enabled`. Compare `clickable`: `false` = disabled, `true` = enabled (verified for the Continue button).
- Images and icons usually have no label. Prefer accessibility ids; if there are none, ask the developers for Semantics labels rather than using coordinates.
- Elements rebuild when state changes (typing, opening sheets). Re-find them instead of holding a reference.

## Gotchas seen so far

- Google's **"Choose a phone number"** system sheet (`com.google.android.gms:id/cancel` closes it) appears when the login screen opens and when the phone field gets focus.
- Never tap **Continue** with a real number just to see the next screen: it sends a real OTP. Use a number the user controls, or wait for the fixed dev OTP.

## Output

Report a table of screen, element, selector strategy and value, then update or create the page object under `pickle_automation/pages/`. Replace any `# TODO selector` stubs that the new information resolves.
