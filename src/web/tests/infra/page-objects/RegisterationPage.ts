import {PageAbstract} from "./PageAbstract";
import {Page} from "@playwright/test";
import {UserInfo} from "../../tests/helpers/user_info";
import {TextInput} from "../page-elements/TextInput";
import {Button} from "../page-elements/Button";


export class RegistrationPage extends PageAbstract {
    constructor(page: Page) {
        super('Registration', '/register', 'Registration Form', page);
    }

    async registerUser(userInfo: UserInfo) {
        const dataArr = [
            {locator: this.page.locator('#username'), value: userInfo.name, name: "username"},
            {locator: this.page.locator('#password'), value: userInfo.password, name: "password"},
            {locator: this.page.locator('#firstName'), value: userInfo.first_name, name: "first name"},
            {locator: this.page.locator('#lastName'), value: userInfo.last_name, name: "last name"},
        ]
        for await (const data of dataArr) {
            await new TextInput(data.locator, data.name).typeText(data.value)
        }
        await new Button(this.page.locator('#submit'), 'Submit').click()
    }

    async errorShown(): Promise<boolean> {
        return await this.page.locator('#error').isVisible()
    }

    async errorTxt(): Promise<string> {
        return await this.page.locator('#error').textContent()
    }

    async warningTxt(): Promise<string> {
        return await this.page.locator('#warning').textContent()
    }

    async warningShown(): Promise<boolean> {
        return await this.page.locator('#warning').isVisible()
    }
}