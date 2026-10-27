---
name: pickle-setup-environment
description: STANDALONE one-time skill, not part of the automation pipeline. Machine setup for Pickle Appium automation - checks and installs Java, Android SDK, an emulator (AVD), Appium + the uiautomator2 driver, and the Python venv. Use when a teammate is new to the project, when `adb`/`appium`/`emulator` is missing, or when tests fail with environment errors.
---

# Set up the Pickle automation environment

Standalone and one-time per machine. Run it only when asked (or when the environment is broken); it is never called by the automation pipeline.

Goal: a machine that can run `pytest -m mobile` against an Android emulator. **Check first, install only what is missing**, and report a short checklist at the end.

## Rules

- Ask before any large download (Android SDK + system image is about 5 GB) and before using `sudo`.
- **Never edit `~/.bashrc`, `~/.zshrc` or other shell profiles.** Environment variables live in `android-env.sh` at the repo root (`source android-env.sh`). Tell the user they can source it from their profile themselves.
- Never write secrets or phone numbers to files.

## 1. Check what exists

Run these and note what is missing:

```bash
source android-env.sh 2>/dev/null
java -version; node --version; python3 --version
which adb emulator sdkmanager avdmanager appium
ls -l /dev/kvm            # Linux: emulator needs KVM (user must be in the `kvm` group or have ACL access)
appium --version; appium driver list --installed
ls .venv >/dev/null 2>&1 && echo venv-ok
```

Requirements: Java 17+ (21 works), Node 18+, Python 3.10+, 16 GB RAM recommended, ~10 GB free disk.

## 2. Python environment

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## 3. Android SDK (skip if `ANDROID_HOME` already has `platform-tools` and `emulator`)

1. Download the command-line tools zip from `https://developer.android.com/studio#command-line-tools-only` into a scratch dir (not the repo), unzip, and move the `cmdline-tools` folder to `$ANDROID_HOME/cmdline-tools/latest` (default `ANDROID_HOME=$HOME/Android/Sdk`).
2. `source android-env.sh`, then accept licences and install:
   ```bash
   yes | sdkmanager --licenses
   sdkmanager "platform-tools" "emulator" "platforms;android-34" "build-tools;34.0.0" \
              "system-images;android-34;google_apis;x86_64"
   ```
   Use a `google_apis` image, **not** `google_apis_playstore` (Play images block adb root and some automation).
3. Create the emulator (the name matches `DEVICE_NAME` in `.env.example`):
   ```bash
   echo no | avdmanager create avd -n Pixel_6_API_34 \
     -k "system-images;android-34;google_apis;x86_64" -d pixel_6 --force
   ```
   Apple-silicon Macs need an `arm64-v8a` image instead of `x86_64`.

## 4. Appium + driver

Appium server and driver versions must be compatible. The newest uiautomator2 driver can require Appium 3.

```bash
appium driver install uiautomator2          # try the latest first
```

If it errors with "server version it requires ... does not meet the currently installed one", **pin an older driver that supports your server** instead of upgrading Appium globally:

```bash
npm view appium-uiautomator2-driver@3 version peerDependencies --json   # pick a version whose peer range includes your Appium
appium driver install uiautomator2@3.10.0
```

Verify: `appium driver doctor uiautomator2`. `JAVA_HOME` and `ANDROID_HOME` must be set (source `android-env.sh` first). A `bundletool.jar` warning is optional and only matters for `.aab` files.

## 5. Config

`cp .env.example .env` if `.env` does not exist, then hand off to `pickle-add-app` to set `APP_PATH` / `APP_PACKAGE`. `.env` is gitignored.

## 6. Finish

Print a checklist: Java, Node, Python venv, SDK, AVD name, Appium version, driver version, `.env`. Then tell the user the next one-time step is `pickle-add-app`; after that they can start automations with `pickle-automation-pipeline`.
