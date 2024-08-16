import {expect, test} from "@playwright/test";
import {LoginPage} from "../infra/page-objects/LoginPage";
import {WelcomePage} from "../infra/page-objects/WelcomePage";
import {mockUserExistance, mockUserInfo, mockUserNotFound} from "./helpers";

test.describe("Login", () => {
    const credentials = { username: "test", password: "test" };

    test("user should login with valid credentials", async ({page}) => {
        const apiRequestUrl = `http://localhost:3000/user?username=${credentials.username}&password=${credentials.password}`
        await mockUserExistance(page, apiRequestUrl, 'GET', {})
        const loginPage = await new LoginPage(page).open()

        await loginPage.login(credentials)

        const welcomePage = new WelcomePage(credentials.username, page)
        expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
    })

    test("user should NOT login with invalid credentials", async ({page}) => {
        await mockUserNotFound()
        const loginPage = await new LoginPage(page).open()

        await loginPage.login(credentials)

        expect(await loginPage.isOpen(), `User is not on the ${loginPage.name}`).toBeTruthy()
        expect(loginPage.shownWarning(), 'Warning not shown').toBeTruthy()
    })

    test("should show a correct user info", async ({page}) => {
        let apiRequestUrl = `http://localhost:3000/user?username=${credentials.username}&password=${credentials.password}`
        await mockUserExistance(page, apiRequestUrl, 'GET', {})

        apiRequestUrl = `http://localhost:3000/user_info?username=${credentials.username}`
        const userInfo = { firstName: 'John', lastName: 'Smith' }
        await mockUserInfo(page, apiRequestUrl, 'GET', userInfo)
        const loginPage = await new LoginPage(page).open()

        await loginPage.login(credentials)

        const welcomePage = new WelcomePage(credentials.username, page)
        expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
        expect(await welcomePage.userInfo(), 'Invalid user info').toEqual(userInfo)
    })
})