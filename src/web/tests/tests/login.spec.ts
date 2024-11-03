import {expect, test} from "@playwright/test";
import {LoginPage} from "../infra/page-objects/LoginPage";
import {WelcomePage} from "../infra/page-objects/WelcomePage";

const apiUrl = process.env.API_URL;

test.describe("Login", () => {
    const validCredentials = {username: "testuser", password: "password123"};

    test.beforeAll(() => {
        expect(apiUrl, 'The API address is invalid').toBeDefined()
    })

    test.describe("Valid input data", () => {
        test("user should login with valid credentials", async ({page}) => {
            const loginPage = await new LoginPage(page).open()

            await loginPage.login(validCredentials)

            const welcomePage = new WelcomePage(validCredentials.username, page)
            expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
        })

        test("should show a correct user info", async ({page}) => {
            const userInfo = {first_name: 'Test', last_name: 'User'}
            const loginPage = await new LoginPage(page).open()

            await loginPage.login(validCredentials)

            const welcomePage = new WelcomePage(validCredentials.username, page)
            expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
            expect(await welcomePage.userInfo(), 'Invalid user info').toEqual(userInfo)
        })
    })

    test.describe("Invalid input data", () => {
        test("user should NOT login with invalid credentials", async ({page}) => {
            const loginPage = await new LoginPage(page).open()

            const invalidCreds = {username: "bla", password: "bla"}
            await loginPage.login(invalidCreds)

            expect(await loginPage.isOpen(), `User is not on the ${loginPage.name}`).toBeTruthy()
            expect(loginPage.shownWarning(), 'Warning not shown').toBeTruthy()
        })

        test('user should NOT login in the case of an error', async ({page}) => {
            const loginPage = await new LoginPage(page).open()

            const invalidCreds = {username: "testuser_500", password: "bla"}
            await loginPage.login(invalidCreds)

            expect(await loginPage.isOpen(), `User is not on the ${loginPage.name}`).toBeTruthy()
            expect(loginPage.shownError(), 'Error not shown').toBeTruthy()
        })
    })
})