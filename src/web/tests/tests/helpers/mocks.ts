import {Page} from "@playwright/test";
import {UserInfo} from "./user_info";

enum StatusCodes {
    OK = 200,
    CREATED = 201,
    INTERNAL_SERVER_ERROR = 500,
    NOT_FOUND = 404,
    BAD_REQUEST = 400,
    CONFLICT = 409
}

const mockRequest = async (page: Page,
                           url: string,
                           expectedApiResponse: object,
                           status = StatusCodes.OK,
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
                await route.fulfill({status: StatusCodes.OK})
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
    await mockRequest(page, url, {}, StatusCodes.NOT_FOUND)
}

export const mockServerError = async (page: Page, url: string) => {
    await mockRequest(page, url, {}, StatusCodes.INTERNAL_SERVER_ERROR)
}

export const mockUserAdd = async (page: Page, userInfo: UserInfo, url: string) => {
    await mockRequest(page, url, {}, StatusCodes.CREATED, 'POST')
}

export const mockUserAddFail = async (page: Page, expectedApiResponse: object, url: string) => {
    await mockRequest(page, url, expectedApiResponse, StatusCodes.BAD_REQUEST, 'POST')
}

export const mockExistingUserAddFail = async (page: Page, userInfo: UserInfo, url: string) => {
    await mockRequest(page, url, {}, StatusCodes.CONFLICT, 'POST')
}

export const mockServerErrorUserAddFail = async (page: Page, url: string) => {
    await mockRequest(page, url, {}, StatusCodes.INTERNAL_SERVER_ERROR, 'POST')
}