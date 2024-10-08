import {PageAbstract} from "./PageAbstract";
import {Page} from "@playwright/test";

export class RegistrationSucceededPage extends PageAbstract {
    constructor(page: Page) {
        super('Registration Succeeded', '/success', 'Registration succeeded', page);
    }

    async text(): Promise<string> {
        return "";
    }
}