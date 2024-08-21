import {Page} from "@playwright/test";

const mockRequest = async (page: Page,
                           url: string,
                           expectedApiResponse: object,
                           status = 200,
                           method = 'GET'
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

export const mockUserExistance = async (page: Page, url: string) => {
    await mockRequest(page, url, {})
}

export const mockUserInfo = async (page: Page, url: string, expectedApiResponse: object) => {
    await mockRequest(page, url, expectedApiResponse)
}

export const mockUserNotFound = async (page: Page, url: string) => {
    await mockRequest(page, url, {}, 404)
}

export const mockServerError = async (page: Page, url: string) => {
    await mockRequest(page, url, {}, 500)
}