import {expect, test} from "@playwright/test";
import {LoginPage} from "../infra/page-objects/LoginPage";
import {WelcomePage} from "../infra/page-objects/WelcomePage";
import {mockServerError, mockUserExistance, mockUserInfo, mockUserNotFound} from "./helpers";

require('dotenv').config();

const apiUrl = process.env.API_URL;


test.describe("Login", () => {
    const credentials = {username: "test", password: "test"};

    test.beforeAll(() => {
        expect(apiUrl, 'The API address is invalid').toBeDefined()
    })

    test.describe("Valid input data", () => {
        test("user should login with valid credentials", async ({page}) => {
            const apiRequestUrl = `${apiUrl}/user?username=${credentials.username}&password=${credentials.password}`
            await mockUserExistance(page, apiRequestUrl)
            const loginPage = await new LoginPage(page).open()

            await loginPage.login(credentials)

            const welcomePage = new WelcomePage(credentials.username, page)
            expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
        })

        test("should show a correct user info", async ({page}) => {
            let apiRequestUrl = `${apiUrl}/user?username=${credentials.username}&password=${credentials.password}`
            await mockUserExistance(page, apiRequestUrl)

            apiRequestUrl = `${apiUrl}/user_info?username=${credentials.username}`
            const userInfo = {first_name: 'John', last_name: 'Smith'}
            await mockUserInfo(page, apiRequestUrl, userInfo)
            const loginPage = await new LoginPage(page).open()

            await loginPage.login(credentials)

            const welcomePage = new WelcomePage(credentials.username, page)
            expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
            expect(await welcomePage.userInfo(), 'Invalid user info').toEqual(userInfo)
        })
    })

    test.describe("Invalid input data", () => {
        test("user should NOT login with invalid credentials", async ({page}) => {
            const apiRequestUrl = `${apiUrl}/user?username=${credentials.username}&password=${credentials.password}`
            await mockUserNotFound(page, apiRequestUrl)
            const loginPage = await new LoginPage(page).open()

            await loginPage.login(credentials)

            expect(await loginPage.isOpen(), `User is not on the ${loginPage.name}`).toBeTruthy()
            expect(loginPage.shownWarning(), 'Warning not shown').toBeTruthy()
        })

        test('user should NOT login in the case of an error', async ({page}) => {
            const apiRequestUrl = `${apiUrl}/user?username=${credentials.username}&password=${credentials.password}`
            await mockServerError(page, apiRequestUrl)
            const loginPage = await new LoginPage(page).open()

            await loginPage.login(credentials)

            expect(await loginPage.isOpen(), `User is not on the ${loginPage.name}`).toBeTruthy()
            expect(loginPage.shownError(), 'Error not shown').toBeTruthy()
        })
    })
})