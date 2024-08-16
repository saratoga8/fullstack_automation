import {PageAbstract} from "./PageAbstract";
import {Page} from "@playwright/test";

type UserInfo = { firstName: string, lastName: string };

export class WelcomePage extends PageAbstract {
    constructor(userName: string, page: Page) {
        super('Welcome', `/welcome:${userName}`, 'Welcome Page', page);
    }

    async userInfo(): Promise<UserInfo> {
        return { firstName: '', lastName: ''};
    }
}