import {PageAbstract} from "./PageAbstract";
import {expect, Page} from "@playwright/test";

type UserInfo = { first_name: string, last_name: string };

export class WelcomePage extends PageAbstract {
    constructor(userName: string, page: Page) {
        super('Welcome', `/welcome:${userName}`, 'Welcome Page', page);
    }

    async userInfo(): Promise<UserInfo> {
        const locator = this.page.locator('#welcome-message')
        const txt = await locator.textContent() ?? ""
        expect(txt, 'The text of user info not found').toBeTruthy()

        const infoTxt = txt.split('Welcome ')[1] ?? ""
        return {
            first_name: infoTxt.split(' ')[0] ?? "",
            last_name: infoTxt.split(' ')[1] ?? ""
        }
    }
}