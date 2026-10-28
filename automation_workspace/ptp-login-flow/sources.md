# Sources - ptp-login-flow

## Jira
- Reference: "WhatsApp Based OTP authentication" (no ticket key provided)
- Status: pasted
- Content:
  - Objective: improve OTP login reliability/accessibility by making WhatsApp the primary OTP channel, with SMS as fallback for Indian users. A new login/OTP UI is part of the change (final designs in Figma, shared separately).
  - First OTP request: send OTP via WhatsApp; enable OTP auto-read/autofill wherever supported; same OTP is valid regardless of delivery channel.
  - Resend, Indian number (+91): send OTP via both WhatsApp and SMS; auto-read/autofill for both; either channel allows verification.
  - Resend, non-Indian number: resend via WhatsApp only; no SMS fallback initially (international SMS cost).
  - UI: new login + OTP verification UI per Figma; existing login functionality retained unless stated; no additional features/behaviour changes; must work with the WhatsApp/SMS flow.
  - Expected flow: enter mobile number -> OTP received -> OTP autofilled -> login.
  - Expected behaviour: WhatsApp is default channel; user is NOT asked to choose WhatsApp or SMS before requesting OTP; autofill stays active for first request and resend; existing OTP expiry, resend timer, retry limits, validation and security rules unchanged.
  - Out of scope: any functional change other than WhatsApp/SMS OTP behaviour and the Figma UI.
  - Rationale (context only): global login support, lower OTP cost, brand visibility, no extra user friction.

## PRD
- Status: not provided (skipped by user)

## Figma
- Reference: no URL; user shared a screenshot of the Figma frames (/tmp/claude-1001/-home-maria-Projects-pickleautomation/21aa8920-e02c-466e-857f-3bb9bcc75a2e/images/1.png)
- Status: pasted (screenshot; small text read visually, so exact copy/labels need confirmation)
- Screens/flows (left to right, with keyboard-open variants shown below the first row):
  1. **Login or Sign Up** - heading "Login to Continue", subtext about verifying/securing the account, country-code selector (default +91 with flag and dropdown), "Your Mobile Number" field, terms line ("Terms & Conditions" and "Privacy Policy" links), "Continue" button disabled (pale) while the number is empty.
  2. **Login or Sign Up, keyboard open, empty** - Continue still disabled.
  3. **Login or Sign Up, number entered** - Continue enabled (red-to-purple gradient); shown with and without keyboard.
  4. **Country code select** - bottom sheet "Choose Country Code", search box ("Search country name"), scrollable list of countries with dial codes (Afghanistan +93, Albania +355, Algeria +213, ...).
  5. **Country code search** - typing "Ind" filters to British Indian Ocean Territory +246, India +91 (selected, check mark), Indonesia +62; shown with and without keyboard.
  6. **Enter Verification Code (empty)** - 4 OTP input boxes, "Sent to" + WhatsApp icon + masked/entered number + "Change" link, Verify button, "Resend code in 30s" timer text; with and without keyboard.
  7. **Enter Verification Code (filled)** - 4 boxes filled, Verify button enabled.
  8. **Successfully Verified** - green check icon and "Successfully Verified" confirmation.
  - Asset: "BG Downloadable" (collage background image used on the login/OTP screens).
- Observations to confirm (go to open questions): OTP boxes show **4 digits** while the repo's DEFAULT_OTP is 6 digits; no screen shows the resend state after the timer ends (resend button, WhatsApp+SMS copy for +91); no error states (wrong/expired OTP, invalid number, retry limit) are in the screenshot.

## Additional documents
- Status: not provided (skipped by user)
