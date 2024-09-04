import {expect, test as base} from "@playwright/test";
import {UserInfo} from "./helpers/types";
import {faker} from "@faker-js/faker";
import {RegistrationPage} from "../infra/page-objects/RegisterationPage";
import {RegistrationSucceededPage} from "../infra/page-objects/RegistrationSucceededPage";
import {mockExistingUserAddFail, mockUserAdd, mockUserAddFail} from "./helpers/mocks";

require('dotenv').config();

const apiUrl = process.env.API_URL;
const apiUserUrl = `${apiUrl}/user`

const test = base.extend<{ userInfo: UserInfo }>({
    userInfo: async ({page}, use) => {
        const info = {
            name: faker.internet.userName(),
            password: faker.internet.password(),
            last_name: faker.person.lastName(),
            first_name: faker.person.firstName(),
        }
        await use(info)
    }
})

test.describe.skip("Registration", () => {
    test.beforeAll(() => {
        expect(apiUrl, 'The API address is invalid').toBeDefined()
    })

    test.beforeEach(async ({page}) => {
        const registerPage = await new RegistrationPage(page).open()
        expect(registerPage.isOpen(), `The page ${registerPage.name} is not open`).toBeTruthy()
    })

    test("user should pass registration with valid data", async ({page, userInfo}) => {
        await mockUserAdd(page, userInfo, apiUserUrl)
        const registerPage = new RegistrationPage(page)

        await registerPage.registerUser(userInfo)

        const successPage = new RegistrationSucceededPage(page)
        expect(await successPage.isOpen(), `The page ${successPage.name} is not open`).toBeTruthy()
        expect(await successPage.text(), `Invalid text in the page ${successPage.name}`).toContain(userInfo.name)
    })

    test("user should fail registration with invalid data", async ({page, userInfo}) => {
        await mockUserAddFail(page, userInfo, apiUserUrl)
        const registerPage = new RegistrationPage(page)

        await registerPage.registerUser(userInfo)
        expect(await registerPage.errorShown(), `The page ${registerPage.name} has no error`).toBeTruthy()
    })

    test("an existing user should fail registration", async ({page, userInfo}) => {
        await mockExistingUserAddFail(page, userInfo, apiUserUrl)
        const registerPage = new RegistrationPage(page)

        await registerPage.registerUser(userInfo)

        expect(await registerPage.errorShown(), `The page ${registerPage.name} has no error`).toBeTruthy()
        expect(await registerPage.errorTxt(), `Invalid error in the page ${registerPage.name}`).toEqual('User already exists')
    })
})
