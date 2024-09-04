import {expect, test} from "@playwright/test";
import axios from 'axios';
import {LoginPage} from "../infra/page-objects/LoginPage";
import {fail} from 'assert'
import {faker} from "@faker-js/faker";
import {WelcomePage} from "../infra/page-objects/WelcomePage";
import {UserInfo} from "./helpers/types";


require('dotenv').config();

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

test.describe('E2E', () => {
    test.beforeAll(() => {
        expect(apiUrl, 'The API address is invalid').toBeDefined()
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

    test('user should get to the Welcome Page', async ({page}) => {
        const userInfo = await createUser()

        const loginPage = await new LoginPage(page).open()

        const credentials = {username: userInfo.name, password: userInfo.password};
        await loginPage.login(credentials)
        const welcomePage = new WelcomePage(credentials.username, page)
        expect(await welcomePage.isOpen(), `User is not on the ${welcomePage.name}`).toBeTruthy()
        const expected = {first_name: userInfo.first_name, last_name: userInfo.last_name}
        expect(await welcomePage.userInfo(), 'Invalid user info').toEqual(expected)
    })
});