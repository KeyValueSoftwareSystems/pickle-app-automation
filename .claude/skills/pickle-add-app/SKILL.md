---
name: pickle-add-app
description: STANDALONE skill, not part of the automation pipeline; run only when the app build changes. Register a new Pickle app build (APK) for automation - puts it in apps/, validates it (package, launcher activity, ABI, min SDK, file type), points .env at it, and checks it installs and launches on the emulator. Use when the user has a new or updated APK, says the APK "is not supporting", or when install/launch fails.
---

# Add or update the app build

Standalone. Run it when there is a new or updated APK (or install/launch fails), not at the start of every automation; the pipeline never calls it.

The app under test is the **dev debug APK** of Pickle (a Flutter app). Builds live in `apps/` (large binaries; never commit them).

## 1. Get the file

Ask the user where the APK is. If it is elsewhere, copy it into `apps/` (ask before overwriting an existing file). Spaces and brackets in the name (e.g. `app-dev-debug (1).apk`) are fine for Appium, but suggest a clean name like `pickle-dev.apk`; rename only if the user agrees.

## 2. Validate

```bash
source android-env.sh
file "apps/<file>"                                    # must say "Android package (APK)"
unzip -l "apps/<file>" | grep -oE "lib/[^/]+/" | sort -u   # ABIs
$ANDROID_HOME/build-tools/34.0.0/aapt dump badging "apps/<file>" | grep -E "^package|sdkVersion|launchable-activity"
```

If `build-tools` is missing: `sdkmanager "build-tools;34.0.0"`.

Interpret and fix:

| Finding | Meaning / what to do |
|---|---|
| Not an APK (`.aab`, `.apks`, `.xapk`) | Appium needs a single universal `.apk`. Ask for one from the developers. |
| ABIs lack `x86_64` (only `arm64-v8a`/`armeabi-v7a`) | `INSTALL_FAILED_NO_MATCHING_ABIS` on an x86_64 emulator. Ask for an x86_64/universal debug build, or use a physical phone. |
| `sdkVersion` above the emulator's Android version | `INSTALL_FAILED_OLDER_SDK`. Use a newer system image. |
| Release build / signature mismatch with an installed copy | `adb uninstall <package>` then reinstall. |

## 3. Point the config at it

Update `.env` (gitignored; create from `.env.example` if missing):

```
APP_PATH=/absolute/path/to/apps/<file>
APP_PACKAGE=<package from aapt>
```

Edit only those two lines. Never put phone numbers or OTPs in `.env`.

## 4. Smoke check (needs a running emulator, see `pickle-run-tests` step 1)

```bash
adb install -r -g "apps/<file>"
adb shell am start -n <package>/<launchable-activity>
sleep 10; adb exec-out screencap -p > <scratchpad>/launch.png
```

Look at the screenshot: the app should reach its welcome screen (it shows a dim splash first, wait ~10 s). Report package, version, ABIs and the result. If it crashes, check `adb logcat -d | grep -i <package>` and report the error verbatim.
