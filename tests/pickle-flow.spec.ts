import { test, expect } from '@playwright/test';

test.describe('Pickle app flow', () => {
  test('login, OTP, template selection and image generation flow', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('textbox', { name: /phone|mobile/i })).toBeVisible();
    await page.getByRole('textbox', { name: /phone|mobile/i }).fill('+919876543210');
    await page.getByRole('button', { name: /continue|send otp|get otp/i }).click();

    await expect(page.getByRole('textbox', { name: /otp|code/i })).toBeVisible();
    await page.getByRole('textbox', { name: /otp|code/i }).fill('123456');
    await page.getByRole('button', { name: /verify|continue/i }).click();

    await expect(page.getByRole('button', { name: /template|explore/i })).toBeVisible();
    await page.getByRole('button', { name: /template|explore/i }).click();

    await page.getByText(/portrait|popular|new/i).first().click();
    await page.getByText(/classic portrait|portrait/i).first().click();

    await page.getByRole('button', { name: /upload|add photo/i }).click();
    await page.setInputFiles('input[type="file"]', 'tests/fixtures/sample-image.png');

    await page.getByRole('button', { name: /generate/i }).click();
    await expect(page.getByText(/generating|processing|complete/i)).toBeVisible({ timeout: 120000 });
  });
});
