# Context - ptp-login-flow (WhatsApp-based OTP authentication)

Sources: Jira (pasted, no key), Figma (screenshot), user clarification 2026-10-27 (SMS fallback, not in Jira). PRD: not provided.

## Goal
Make WhatsApp the default OTP channel for login, with SMS added on resend for Indian (+91) numbers, and ship a new login/OTP UI per Figma. Everything else about login (expiry, resend timer, retry limits, validation, security) stays unchanged.

## User flows
1. **First OTP request (any country)**: enter mobile number (country code selected) -> Continue -> OTP sent via WhatsApp only -> OTP autofilled -> Verify -> "Successfully Verified" -> logged in. [Jira, Figma]
2. **Resend, +91 number**: on the OTP screen wait for the resend timer -> tap resend -> OTP sent via WhatsApp **and** SMS -> either one can be used (autofilled or typed) to verify. [Jira]
3. **Resend, non-+91 number**: resend -> OTP sent via WhatsApp only; no SMS. [Jira]
4. **Change country code**: tap the country selector -> "Choose Country Code" sheet -> search (e.g. "Ind") -> pick a country (e.g. India +91). [Figma]
5. **Change number**: tap "Change" on the OTP screen to go back and edit the number. [Figma]
6. **Manual OTP entry** (when autofill is unsupported): type the 4 digits -> Verify. [Figma]

7. **SMS fallback after 10s (all countries)**: after the WhatsApp OTP is sent, if the OTP is **neither auto-read nor typed within 10 seconds**, the **app sends a request** to the backend and the backend then sends the OTP via SMS; either OTP works. No user action. This happens once, **before the 30s resend becomes available** (it does not restart after a resend). If the OTP is auto-read or typed within 10s, no SMS is requested. [User 2026-10-27]

## Screens
| Screen | Key elements |
|---|---|
| Login or Sign Up (empty) | "Login to Continue" heading, subtext, country selector (default +91), "Your Mobile Number" input, Terms & Conditions / Privacy Policy links, Continue (disabled) |
| Login (number entered) | same, Continue enabled; keyboard variants |
| Choose Country Code | bottom sheet, "Search country name" box, list of country + dial code |
| Country search results | filtered list; selected country shows a check mark |
| Enter Verification Code | 4 OTP boxes, "Sent to [WhatsApp icon] <number> Change", Verify button, "Resend code in 30s" |
| Enter Verification Code (filled) | boxes filled, Verify enabled |
| Successfully Verified | green check + "Successfully Verified" |

No channel-selection screen/option exists in the new design.

## Business rules & acceptance criteria
- R1 WhatsApp is the default channel; first request goes via WhatsApp. SMS may follow after 10s (R12). [Jira, qualified]
- R2 The same OTP is valid regardless of delivery channel. [Jira]
- R3 Resend for +91: OTP sent via both WhatsApp and SMS; either channel completes verification. [Jira]
- R4 Resend for non-+91: the resend itself is WhatsApp only (no SMS added by resend). **Qualified by R12**: a non-+91 user can still receive SMS from the 10s fallback after a request. [Jira, qualified]
- R5 Autofill/auto-read active on first request and resend, wherever supported (WhatsApp and SMS for +91). [Jira]
- R6 The user is not asked to choose WhatsApp or SMS before requesting the OTP. [Jira, Figma]
- R7 OTP expiry, resend timer, retry limits, validation and security rules are unchanged. [Jira]
- R8 UI follows Figma; no other functional change. [Jira]
- R9 Continue is disabled until a mobile number is entered. [Figma]
- R10 OTP screen shows the destination number, the WhatsApp channel indicator, a Change link, and a resend countdown (30s shown). [Figma]
- R12 NEW: Only if the WhatsApp OTP is **neither auto-read nor typed within 10 seconds of being sent**, the app sends a request and the backend sends the OTP by SMS, for **all countries**. If it is auto-read or typed in time, no SMS request is made. The check runs once per OTP send, before the 30s resend (R7) is available, and is not restarted by a resend. The OTP is the same on both channels (R2). No user action. [User 2026-10-27, not in Jira]
- R11 Successful verification shows a "Successfully Verified" confirmation. [Figma]

## Test data needs
- A real +91 number that can receive both WhatsApp and SMS (for R3, R5). OTP will be read from WhatsApp on the device (see Decisions).
- A non-+91 number that can receive WhatsApp (for R4).
- Real OTP delivery cannot be observed by Appium from the app alone; decide between real device with WhatsApp/SMS, a backend/test OTP, or a mocked OTP (see open questions).
- Environment: Appium server, device/emulator, `APP_PATH`, `APP_PACKAGE`; phone number/OTP supplied at run time via env vars (`PHONE_NUMBER`, `DEFAULT_OTP`), never committed.

## Existing automation (reusable)
- `pickle_automation/pages/login_page.py` - `LoginPage`: `PHONE_INPUT`, `CONTINUE_BUTTON`, `enter_phone_number`, `submit_phone_number`. **Outdated for this change**: has `WHATSAPP_OPTION`/`SMS_OPTION` and `choose_otp_channel`, and `login()` calls it, which contradicts R6 (no channel choice). Needs updating.
- `pickle_automation/pages/otp_page.py` - `OtpPage`: single `OTP_INPUT`, `VERIFY_BUTTON`, `RESEND_BUTTON`, `enter_otp`, `verify_otp`, `resend_code`. Design has 4 separate boxes, countdown and Change link, none modelled yet.
- `pickle_automation/pages/base_page.py` - find/tap/type/wait helpers (Android UiAutomator-based text waits).
- `pickle_automation/config.py` - `PHONE_NUMBER` (+919876543210 default), `DEFAULT_OTP` (123456), `TIMEOUT_SECONDS`.
- `tests/test_pickles_generation_flow.py` - end-to-end flow; calls `login(..., preferred_channel="whatsapp")` (will break/need change when channel step is removed); skips when `APP_PATH` unset.
- `tests/pickle-flow.spec.ts` - Playwright variant with hardcoded phone/OTP; targets a web app, not the Figma mobile flow.
- All element IDs in the page objects are placeholders (`com.pickle.app:id/...`), unverified against the real build.
- No page objects exist yet for the country-code picker or success screen.

## Decisions (answered by user, 2026-10-23)
- D1 Framework: **Appium (Python + pytest)**. Playwright suite is out of scope for this feature.
- D2 OTP length: **4 digits** (matches Figma). `DEFAULT_OTP` (123456) is stale for this flow and must not be used.
- D3 OTP source: **read from WhatsApp** on the device. Mechanism not specified yet (e.g. open WhatsApp via Appium and read the latest message, or read the notification shade); to be settled in stage 4. Requires a device/emulator with WhatsApp installed and logged in to the test number. SMS delivery and autofill for +91 resend are not covered by this and are marked manual or deferred unless the user says otherwise.
- D4 Resend timer: **30 seconds** (matches Figma).
- D5 (2026-10-27) SMS fallback: **applies to all countries**, **triggered by the app** (a request after 10s with no auto-read; the backend then sends the SMS), and the **existing resend rules stay unchanged** (R3/R4). WhatsApp OTP will not be read on the emulator; the plan is a **fixed dev OTP from the backend** (pending) instead of reading WhatsApp/SMS.

## Conflicts (resolved)
- R12 vs R4/R1 (Jira): the Jira says non-+91 gets no SMS fallback and the first request is WhatsApp only. The newer user clarification wins: SMS fallback after 10s applies to all countries; R4 now only describes what resend does.
- OTP length: resolved to 4 digits (D2).
- Channel choice step: Jira/Figma win; existing `LoginPage.choose_otp_channel`/`WHATSAPP_OPTION`/`SMS_OPTION` and `login(preferred_channel=...)` are to be removed or deprecated, and the existing e2e test updated.
- Suite: resolved to Appium (D1).

## Open questions (remaining)
1. OTP expiry and retry-limit values, and the exact error messages/UI for wrong OTP, expired OTP, too many attempts, invalid number (not in Figma). Cases will assert generic error visibility unless told otherwise.
2. Resend state after the 30s timer ends (button label/copy; any message for +91 saying both WhatsApp and SMS were sent) is not in Figma.
3. Phone-number validation rules (length per country, +91 starting digits).
4. Where the app lands after "Successfully Verified"; new vs. existing user behaviour ("Login or Sign Up").
5. Exactly what "Change" does (back to login with number prefilled?) and back-arrow behaviour.
6. How WhatsApp OTP reading should work technically (D3): real device with WhatsApp logged in, or emulator? Is reading the notification acceptable?
7. SMS on +91 resend and autofill: confirm they stay manual/not automated.
8. A non-+91 test number that receives WhatsApp (for R4) - available?
9. Ticket key / Figma URL for traceability, if available.
10. SMS fallback (R12): does the OTP screen indicate that SMS was also sent (icon/copy)? (Resolved 2026-10-27: the 10s check runs once before resend and is not restarted; typing the OTP within 10s cancels the SMS.)
11. Which request does the app send at 10s (a resend-style API call?) and does it count against the retry limit (R7)?
