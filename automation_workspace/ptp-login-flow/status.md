# Status - ptp-login-flow
- Stage 1 collect-docs: done (Jira pasted, PRD skipped, Figma screenshot, extras skipped) - 2026-10-23
- Stage 2 generate-context: done, confirmed by user (2026-10-27)
- Stage 3 generate-testcases: done, all 24 approved by user (2026-10-27). Automate now: TC-001..TC-017 except TC-011 (16 cases)
- Stage 4 generate-testscript: done (2026-10-27). tests/test_login_flow.py: 8 live (TC-001..005, 007..009) pass; 8 OTP-screen cases (TC-006, 010, 012..017) skipped with TODO selectors; TC-011 deferred (OTP source)
- R12/D5 SMS fallback after 10s: app requests SMS only if OTP not auto-read in 10s, backend then sends (all countries); TC-025..TC-030 manual; fires once before resend, typing the OTP within 10s cancels it - 2026-10-27
