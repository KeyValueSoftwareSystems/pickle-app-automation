# Test cases - ptp-login-flow (WhatsApp-based OTP authentication)

Framework: Appium (Python + pytest). Selectors: accessibility ids / text (Flutter app, UiAutomator2). OTP length: 4. Resend timer: 30s.
Test data placeholders: `<PHONE_NUMBER>` (+91, WhatsApp + SMS capable), `<NON_IN_PHONE_NUMBER>` (non-+91, WhatsApp capable), `<OTP>` (read from WhatsApp at run time). Never commit real values.

## Login screen

### TC-001 - Continue is disabled with empty mobile number
- Priority: P0
- Type: smoke
- Traces to: R9
- Preconditions: App freshly launched, logged out; on "Login or Sign Up" screen (Welcome -> Log In / Get Started)
- Test data: none
- Steps:
  1. Open the login screen.
  2. Leave "Your Mobile Number" empty.
- Expected result: "Login to Continue" heading and country selector (+91) shown; Continue is disabled.
- Automate: yes

### TC-002 - Continue is enabled after entering a number
- Priority: P0
- Type: smoke
- Traces to: R9
- Preconditions: On login screen
- Test data: <PHONE_NUMBER>
- Steps:
  1. Enter <PHONE_NUMBER> (without country code) in "Your Mobile Number".
- Expected result: Continue becomes enabled.
- Automate: yes

### TC-003 - Default country code is +91
- Priority: P1
- Type: regression
- Traces to: Flow 1, Screens (Login)
- Preconditions: On login screen
- Test data: none
- Steps:
  1. Observe the country selector.
- Expected result: India +91 is preselected.
- Automate: yes

### TC-004 - Change country code via search
- Priority: P1
- Type: regression
- Traces to: Flow 4
- Preconditions: On login screen
- Test data: search text "Ind"
- Steps:
  1. Tap the country selector.
  2. Verify the "Choose Country Code" sheet and "Search country name" box appear.
  3. Type "Ind".
  4. Select India (+91).
- Expected result: List filters to matching countries; India shows a check mark; the sheet closes and the selector shows +91.
- Automate: yes

### TC-005 - Country search with no match
- Priority: P2
- Type: edge
- Traces to: Flow 4
- Preconditions: "Choose Country Code" sheet open
- Test data: search text "zzzz"
- Steps:
  1. Type "zzzz" in the search box.
- Expected result: No countries listed; app does not crash; clearing the text restores the full list.
- Automate: yes

### TC-006 - No WhatsApp/SMS channel selection before requesting OTP
- Priority: P0
- Type: regression
- Traces to: R6, R1
- Preconditions: On login screen with number entered
- Test data: <PHONE_NUMBER>
- Steps:
  1. Enter number and tap Continue.
- Expected result: App goes straight to "Enter Verification Code" with no channel-choice screen/option.
- Automate: yes

### TC-007 - Invalid (too short) mobile number
- Priority: P1
- Type: negative
- Traces to: R7 (validation unchanged); Open Q3
- Preconditions: On login screen
- Test data: "12345"
- Steps:
  1. Enter "12345" and tap Continue (if enabled).
- Expected result: App does not proceed to the OTP screen; a validation error/message is visible (exact copy TBD).
- Automate: yes

### TC-008 - Terms & Conditions and Privacy Policy links present
- Priority: P2
- Type: regression
- Traces to: Screens (Login), R8
- Preconditions: On login screen
- Test data: none
- Steps:
  1. Observe the area below the number field.
- Expected result: Terms & Conditions and Privacy Policy links are visible.
- Automate: yes

### TC-009 - Continue with no network
- Priority: P2
- Type: negative
- Traces to: R7
- Preconditions: Number entered; device network disabled
- Test data: <PHONE_NUMBER>
- Steps:
  1. Disable network (Appium network toggle).
  2. Tap Continue.
- Expected result: App stays on login (or shows an error); no OTP screen; no crash. Network restored after test.
- Automate: yes

## OTP screen

### TC-010 - OTP screen content after first request (+91)
- Priority: P0
- Type: smoke
- Traces to: R1, R10, Flow 1
- Preconditions: On login screen with <PHONE_NUMBER> (+91) entered
- Test data: <PHONE_NUMBER>
- Steps:
  1. Tap Continue.
- Expected result: "Enter Verification Code" shown with 4 OTP boxes; "Sent to" + WhatsApp indicator + number + "Change"; Verify button; "Resend code in 30s" countdown.
- Automate: yes

### TC-011 - Verify with correct OTP from WhatsApp (happy path)
- Priority: P0
- Type: smoke
- Traces to: R1, R2, R11, Flow 1
- Preconditions: On OTP screen; WhatsApp on device logged in to <PHONE_NUMBER> (D3)
- Test data: <PHONE_NUMBER>, <OTP> (read from WhatsApp)
- Steps:
  1. Read the 4-digit <OTP> from the latest WhatsApp message.
  2. Enter it in the OTP boxes.
  3. Tap Verify.
- Expected result: "Successfully Verified" confirmation shown, then user is logged in (landing screen TBD, Open Q4).
- Automate: yes (OTP read mechanism to be settled in stage 4)

### TC-012 - Manual 4-digit entry enables Verify
- Priority: P1
- Type: regression
- Traces to: Flow 6, Screens (OTP filled)
- Preconditions: On OTP screen
- Test data: "1234" (dummy)
- Steps:
  1. Type 4 digits into the OTP boxes.
- Expected result: All 4 boxes filled; Verify becomes enabled.
- Automate: yes

### TC-013 - Verify disabled with incomplete OTP
- Priority: P1
- Type: negative
- Traces to: Screens (OTP), R7
- Preconditions: On OTP screen
- Test data: "12"
- Steps:
  1. Enter only 2 digits.
- Expected result: Verify stays disabled (or does not verify).
- Automate: yes

### TC-014 - Wrong OTP is rejected
- Priority: P0
- Type: negative
- Traces to: R7
- Preconditions: On OTP screen
- Test data: "1111" (anything other than the valid OTP)
- Steps:
  1. Enter "1111".
  2. Tap Verify.
- Expected result: Error is shown (generic; exact copy TBD, Open Q1); user stays on OTP screen; not logged in.
- Automate: yes

### TC-015 - "Change" returns to number entry
- Priority: P1
- Type: regression
- Traces to: Flow 5; Open Q5
- Preconditions: On OTP screen
- Test data: <PHONE_NUMBER>
- Steps:
  1. Tap "Change".
- Expected result: App returns to the login screen where the number can be edited.
- Automate: yes

### TC-016 - Resend timer counts down from 30s
- Priority: P1
- Type: regression
- Traces to: R7, R10, D4
- Preconditions: On OTP screen right after OTP request
- Test data: none
- Steps:
  1. Observe the countdown text.
  2. Wait a few seconds and observe again.
- Expected result: Starts at "Resend code in 30s", decrements each second; resend is not available until it reaches 0.
- Automate: yes

### TC-017 - Resend is available after timer ends
- Priority: P1
- Type: regression
- Traces to: R7, R10; Open Q2
- Preconditions: On OTP screen
- Test data: none
- Steps:
  1. Wait for the 30s timer to finish.
- Expected result: Countdown is replaced by an enabled resend action (copy TBD).
- Automate: yes

## Resend and channel behaviour

### TC-018 - Resend for +91: OTP via WhatsApp and SMS
- Priority: P1
- Type: regression
- Traces to: R3, Flow 2
- Preconditions: On OTP screen with a +91 number; timer finished
- Test data: <PHONE_NUMBER>
- Steps:
  1. Tap resend.
  2. Check WhatsApp and SMS on the device.
- Expected result: OTP arrives on both WhatsApp and SMS; timer restarts.
- Automate: no (SMS delivery not observable by the app; D3/Open Q7). Automate only the resend tap + timer restart if desired.

### TC-019 - Either channel's OTP verifies after +91 resend
- Priority: P1
- Type: regression
- Traces to: R2, R3
- Preconditions: TC-018 done
- Test data: <OTP> from WhatsApp, <OTP> from SMS
- Steps:
  1. Verify using the WhatsApp OTP (separate run: SMS OTP).
- Expected result: Both succeed with "Successfully Verified"; same OTP value on both channels.
- Automate: no (needs SMS, manual)

### TC-020 - Resend for non-+91: WhatsApp only
- Priority: P1
- Type: regression
- Traces to: R4, Flow 3
- Preconditions: Non-+91 number registered on WhatsApp; Open Q8
- Test data: <NON_IN_PHONE_NUMBER>
- Steps:
  1. Select the country code, enter the number, Continue.
  2. After 30s tap resend.
  3. Check WhatsApp and SMS.
- Expected result: The resend itself adds no SMS (WhatsApp only). Note: an SMS from the 10s fallback of the first request (R12) may legitimately arrive; check timing against the resend.
- Automate: no (no non-+91 test number yet; absence of SMS is manual)

### TC-021 - Autofill of OTP on first request and resend
- Priority: P2
- Type: regression
- Traces to: R5
- Preconditions: Device supporting autofill/auto-read
- Test data: <PHONE_NUMBER>
- Steps:
  1. Request OTP; observe the boxes.
  2. Resend; observe again.
- Expected result: OTP boxes autofill from WhatsApp (and SMS for +91 resend) where supported.
- Automate: no (device/OS dependent, manual)

## SMS fallback after 10s (R12, added 2026-10-27)

### TC-025 - App requests SMS after 10s without auto-read (+91)
- Priority: P1
- Type: regression
- Traces to: R12, Flow 7
- Preconditions: +91 number with WhatsApp and SMS; WhatsApp OTP neither auto-read nor typed
- Test data: <PHONE_NUMBER>
- Steps:
  1. Request OTP via Continue.
  2. Do not enter the OTP; wait 10 seconds after it was sent.
  3. Check SMS on the device.
- Expected result: The app sends a request after 10s and an SMS with the OTP arrives with no user action. This happens before the 30s resend is available.
- Automate: no (SMS delivery not observable by the app; manual)

### TC-026 - SMS fallback also applies to a non-+91 number
- Priority: P1
- Type: regression
- Traces to: R12 (all countries), R4
- Preconditions: Non-+91 number reachable by WhatsApp and SMS; Open Q8
- Test data: <NON_IN_PHONE_NUMBER>
- Steps:
  1. Select the country code, enter the number, Continue.
  2. Wait 10 seconds without entering the OTP.
  3. Check SMS.
- Expected result: SMS OTP arrives after ~10s. A later resend (after 30s) still adds no SMS by itself (R4).
- Automate: no (needs a non-+91 number and SMS, manual)

### TC-027 - Either OTP verifies after the 10s SMS fallback
- Priority: P1
- Type: regression
- Traces to: R2, R12
- Preconditions: TC-025 done
- Test data: WhatsApp <OTP>, SMS <OTP>
- Steps:
  1. Verify with the WhatsApp OTP (separate run: the SMS OTP).
- Expected result: Both succeed; both messages carry the same OTP.
- Automate: no (SMS, manual). With the fixed dev OTP, only the "OTP accepted" part is automatable.

### TC-028 - OTP auto-read within 10s: no SMS requested
- Priority: P2
- Type: edge
- Traces to: R12
- Preconditions: Device where the WhatsApp OTP is auto-read
- Test data: <OTP>
- Steps:
  1. Request OTP and let it auto-fill within 10 seconds; verify.
  2. Wait past 10 seconds and check SMS.
- Expected result: No SMS is requested or received. (Manual typing within 10s is Open Q10.)
- Automate: no (autofill and SMS are device dependent, manual)

### TC-029 - OTP typed within 10s: no SMS requested
- Priority: P1
- Type: regression
- Traces to: R12
- Preconditions: Device where the OTP is not auto-read (or autofill disabled)
- Test data: <PHONE_NUMBER>, <OTP>
- Steps:
  1. Request OTP and type the 4 digits before 10 seconds pass.
  2. Wait past 10 seconds and check SMS (verify, or stay on the screen).
- Expected result: No SMS request is made and no SMS arrives.
- Automate: no (SMS not observable by the app; manual). The typing part can be automated once the fixed dev OTP exists.

### TC-030 - 10s SMS check does not restart after resend
- Priority: P2
- Type: edge
- Traces to: R12, R3, R7
- Preconditions: +91 number; no OTP entered
- Test data: <PHONE_NUMBER>
- Steps:
  1. Request OTP; let the 10s SMS fallback fire; wait for the 30s timer; tap resend.
  2. Wait another 10 seconds and check SMS.
- Expected result: Resend sends WhatsApp and SMS as per R3 (+91); no second 10s fallback request is made.
- Automate: no (SMS, manual)

## Unchanged-rule and visual checks

### TC-022 - OTP expiry
- Priority: P2
- Type: negative
- Traces to: R7; Open Q1
- Preconditions: OTP requested, not used
- Test data: <OTP>
- Steps:
  1. Wait past the expiry window.
  2. Enter the old OTP, Verify.
- Expected result: Rejected as expired.
- Automate: no (expiry value unknown / long wait)

### TC-023 - Retry limit
- Priority: P2
- Type: negative
- Traces to: R7; Open Q1
- Preconditions: On OTP screen
- Test data: wrong OTPs
- Steps:
  1. Enter wrong OTPs repeatedly until blocked.
- Expected result: Blocked/limit message after the configured attempts.
- Automate: no (limit values unknown)

### TC-024 - UI matches Figma
- Priority: P2
- Type: regression
- Traces to: R8
- Preconditions: Login, country sheet, OTP and success screens reachable
- Test data: none
- Steps:
  1. Visually compare each screen with Figma.
- Expected result: Layout, copy, icons match design.
- Automate: no (visual, manual)

## Traceability

| Criterion | Test cases |
|---|---|
| R1 WhatsApp default (SMS may follow, R12) | TC-006, TC-010, TC-011 |
| R2 Same OTP any channel | TC-011, TC-019, TC-027 |
| R3 +91 resend WhatsApp + SMS | TC-018, TC-019 |
| R4 non-+91 resend WhatsApp only (qualified by R12) | TC-020, TC-026 |
| R5 Autofill | TC-021 |
| R12 SMS fallback after 10s, all countries | TC-025, TC-026, TC-027, TC-028, TC-029, TC-030 |
| R6 No channel choice | TC-006 |
| R7 Unchanged rules | TC-007, TC-009, TC-013, TC-014, TC-016, TC-017, TC-022, TC-023 |
| R8 UI per Figma | TC-008, TC-024 |
| R9 Continue disabled until number | TC-001, TC-002 |
| R10 OTP screen elements | TC-010, TC-016, TC-017 |
| R11 Successfully Verified | TC-011 |
| Flow 4 country change | TC-003, TC-004, TC-005 |
| Flow 5 Change number | TC-015 |
| Flow 6 manual OTP | TC-012 |

Criteria with no case: none. Cases that need manual or deferred execution: TC-018 to TC-030.
