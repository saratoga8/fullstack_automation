import { defineConfig } from '@playwright/test';


export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  expect: { timeout: 5000 },
  timeout: 8000,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },

  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://127.0.0.1:3000',
  //   stdout: 'ignore',
  //   stderr: 'pipe',
  // },
});
