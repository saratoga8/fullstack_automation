import {Page} from "@playwright/test";
import {UserInfo} from "./types";


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

const mockAuthRequest = async (page: Page, url: string) => {
    await page.route(url, async (route) => {
        if (route.request().method() === 'GET') {
            if (await route.request().headerValue('Authorization')) {
                await route.fulfill({status: 200})
            }
        }
    })
}

export const mockUserExistance = async (page: Page, url: string) => {
    await mockAuthRequest(page, url)
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

export const mockUserAdd = async (page: Page, userInfo: UserInfo, url: string) => {
    await mockRequest(page, url, {}, 200, 'POST')
}

export const mockUserAddFail = async (page: Page, userInfo: UserInfo, url: string) => {
    await mockRequest(page, url, {}, 400, 'POST')
}

export const mockExistingUserAddFail = async (page: Page, userInfo: UserInfo, url: string) => {
    await mockRequest(page, url, {}, 409, 'POST')
}