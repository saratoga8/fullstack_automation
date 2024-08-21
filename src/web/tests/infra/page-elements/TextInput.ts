import {PageElement} from './PageElement';
import {expect, Locator} from '@playwright/test';

export class TextInput extends PageElement {
    constructor(locator: Locator, name = '') {
        super(locator, name);
        this.locator = locator;
    }

    async typeText(text: string) {
        const errMsg = `Can't type in the element ${this.name}`
        await expect(this.locator, errMsg).toBeEditable({timeout: 5000});
        await this.locator.click();
        await this.locator.fill(text);
    }
}
