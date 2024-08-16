import { Locator } from '@playwright/test';

export abstract class PageElement {
  protected constructor(public locator: Locator, public readonly name = '') {}
}
