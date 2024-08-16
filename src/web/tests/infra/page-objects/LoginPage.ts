import {PageAbstract} from "./PageAbstract";
import {Page} from "@playwright/test";
import {TextInput} from "../page-elements/TextInput";
import {Button} from "../page-elements/Button";

export class LoginPage extends PageAbstract {
    constructor(page: Page) {
        super('Login', '/login', 'Login Page', page);
    }

    async login(credentials: { password: string; username: string }) {
        const locatorUsr = this.page.locator('#username')
        await new TextInput(locatorUsr, 'User Name').typeText(credentials.username)

        const locatorPwd = this.page.locator('#password')
        await new TextInput(locatorPwd, 'Password').typeText(credentials.password)

        const locatorBtn = this.page.locator('#submit');
        await new Button(locatorBtn, 'Login').click()
    }

    async shownWarning(): Promise<boolean> {
        const locator = this.page.locator('#warning')
        return await locator.isVisible()
    }
}