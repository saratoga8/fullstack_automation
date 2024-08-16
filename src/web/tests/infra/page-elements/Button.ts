import { Clickable } from './Clickable';
import { PageElement } from './PageElement';
import { expect, Locator } from '@playwright/test';

export class Button extends PageElement implements Clickable {
  constructor(locator: Locator, name: string) {
    super(locator, name);
  }

  async click(): Promise<void> {
    await expect(this.locator, `The button ${this.name} not exist`).toBeAttached();
    await this.locator.click();
  }
}
