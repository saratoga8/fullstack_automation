import {defineConfig} from '@playwright/test';


export default defineConfig({
    testDir: './tests',
    fullyParallel: true,
    expect: {timeout: 5000},
    timeout: 8000,
    use: {
        baseURL: `http://localhost:${process.env.WEB_APP_PORT}`,
        trace: 'retain-on-failure',
        screenshot: 'only-on-failure',
    }
});
