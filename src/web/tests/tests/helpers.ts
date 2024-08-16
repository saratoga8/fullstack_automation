import {Page} from "@playwright/test";

export const mockUserNotFound = async () => {

}

export const mockUserInfo = async (
    page: Page,
    url: string,
    method: 'GET',
    expectedApiResponse: object,
    status = 200
)=> {
    await page.route(url, async (route) => {
        if (route.request().method() === method) {
            await route.fulfill({
                status: status,
                contentType: 'application/json',
                body: JSON.stringify(expectedApiResponse),
            });
        } else {
            await route.continue();
        }
    });
}

export const mockUserExistance = async (
    page: Page,
    url: string,
    method: 'GET',
    expectedApiResponse: object,
    status = 200
) => {
    await page.route(url, async (route) => {
        if (route.request().method() === method) {
            await route.fulfill({
                status: status,
                contentType: 'application/json',
                body: JSON.stringify(expectedApiResponse),
            });
        } else {
            await route.continue();
        }
    });
}

