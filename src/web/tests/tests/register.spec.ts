import {expect, test as base} from "@playwright/test";
import {buildUserInfo, UserInfo} from "./helpers/user_info";

import {RegistrationPage} from "../infra/page-objects/RegisterationPage";
import {RegistrationSucceededPage} from "../infra/page-objects/RegistrationSucceededPage";

const apiUrl = process.env.API_URL;
const apiUserUrl = `${apiUrl}/user`

const test = base.extend<{ userInfo: UserInfo }>({
    userInfo: async ({page}, use) => {
        const info = buildUserInfo()
        await use(info)
    }
})

test.describe("Registration", () => {
    test.beforeAll(() => {
        expect(apiUrl, 'The API address is invalid').toBeDefined()
    })

    test.beforeEach("Open registry page", async ({page}) => {
        const registerPage = await new RegistrationPage(page).open()
        expect(registerPage.isOpen(), `The page ${registerPage.name} is not open`).toBeTruthy()
    })

    test("user should pass registration with valid data", async ({page, userInfo}) => {
        const registerPage = new RegistrationPage(page)

        await registerPage.registerUser(userInfo)

        const successPage = new RegistrationSucceededPage(page)
        expect(await successPage.isOpen(), `The page ${successPage.name} is not open`).toBeTruthy()
    })

    test("user should fail registration with invalid data", async ({page, userInfo}) => {
        userInfo.name = ""
        const responseErrMessage = "Invalid user data"
        const registerPage = new RegistrationPage(page)

        await registerPage.registerUser(userInfo)

        expect(await registerPage.warningShown(), `The page ${registerPage.name} has no warning`).toBeTruthy()
        const errMsg = `Invalid warning in the page ${registerPage.name}`
        expect(await registerPage.warningTxt(), errMsg).toEqual(responseErrMessage)
    })

    test("an existing user should fail registration", async ({page, userInfo}) => {
        userInfo.name = "testuser"
        const registerPage = new RegistrationPage(page)

        await registerPage.registerUser(userInfo)

        expect(await registerPage.warningShown(), `The page ${registerPage.name} has no warning`).toBeTruthy()
        const expectedTxt = `User ${userInfo.name} already exists`
        expect(await registerPage.warningTxt(), `Invalid warning in the page ${registerPage.name}`).toEqual(expectedTxt)
    })

    test("should fail user adding because of a server error", async ({page, userInfo}) => {
        userInfo.name = "testuser_500"
        const registerPage = new RegistrationPage(page)

        await registerPage.registerUser(userInfo)

        expect(await registerPage.errorShown(), `The page ${registerPage.name} has no error`).toBeTruthy()
        expect(await registerPage.errorTxt(), `Invalid error in the page ${registerPage.name}`).toEqual('Server Error')
    })
})
