import {PageAbstract} from "./PageAbstract";
import {Page} from "@playwright/test";
import {UserInfo} from "../../tests/helpers/types";


export class RegistrationPage extends PageAbstract {
    constructor(page: Page) {
        super('Registration', '/register', 'Registration Form', page);
    }


    async registerUser(userInfo: UserInfo) {

    }

    async errorShown(): Promise<boolean> {
        return false
    }

    async errorTxt(): Promise<string> {
        return ""
    }
}