import {expect, test} from "@playwright/test";
import axios from 'axios';
import {fail} from 'assert'
import {faker} from "@faker-js/faker";
import {buildUserInfo, UserInfo} from "./helpers/user_info";
import {RegistrationPage} from "../infra/page-objects/RegisterationPage";
import {RegistrationSucceededPage} from "../infra/page-objects/RegistrationSucceededPage";
import {LoginPage} from "../infra/page-objects/LoginPage";
import {WelcomePage} from "../infra/page-objects/WelcomePage";


const apiUrl = process.env.API_URL;
const apiUserUrl = `${apiUrl}/user`

async function createUser(): Promise<UserInfo> {
    const userInfo = {
        name: faker.internet.userName(),
        password: faker.internet.password(),
        last_name: faker.person.lastName(),
        first_name: faker.person.firstName(),
    }
    try {
        const response = await axios.post(apiUserUrl, userInfo)
        expect(response.status, "Invalid status of creating user").toBe(axios.HttpStatusCode.Created)
    } catch (e) {
        fail(`Error while creating user info: ${e}`)
    }
    return userInfo
}

test.describe('E2E', {tag: '@e2e'}, () => {
    let userInfo = null
    test.describe.configure({mode: 'serial'});

    test.beforeAll(() => {
        expect(apiUrl, 'The API address is invalid').toBeDefined()
        userInfo = buildUserInfo()
    })

    test.beforeEach(async ({baseURL}) => {
        try {
            const response = await axios.get(`${apiUrl}/health`)
            expect(response.status, 'Incorrect health status of the API service').toBe(axios.HttpStatusCode.Ok)
        } catch (error) {
            fail('API service is unreachable')
        }
        try {
            const response = await axios.get(`${baseURL}/health`)
            expect(response.status, 'The Web App service is not reachable').toBe(axios.HttpStatusCode.Ok)
        } catch (error) {
            fail('Web App service is unreachable')
        }
    })

    test("user should pass registration", async ({page}) => {
        const registerPage = await new RegistrationPage(page).open()

        await registerPage.registerUser(userInfo)

        const successPage = new RegistrationSucceededPage(page)
        expect(await successPage.isOpen(), `The page ${successPage.name} is not open`).toBeTruthy()
    })

    test("user should login", async ({page}) => {
        const loginPage = await new LoginPage(page).open()

        await loginPage.login({username: userInfo.name, password: userInfo.password})

        const welcomePage = new WelcomePage(userInfo.name, page)
        expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
    })
});