import { expect, Page } from '@playwright/test';

export abstract class PageAbstract {
  get url(): string {
    return this._url && this._url !== '' ? this._url : this.page.url();
  }
  get name(): string {
    return this._name;
  }
  get title(): string {
    return this._title;
  }
  set timeout(value: number) {
    this._timeout = value;
  }
  protected _timeout: number = 30000;

  protected constructor(
    protected readonly _name: string,
    protected readonly _url: string,
    protected readonly _title: string,
    protected readonly page: Page
  ) {}

  public async open(): Promise<this> {
    expect(this._url, `Invalid URL for the ${this._name} page`).toBeDefined();
    await this.page.goto(this._url, { timeout: this._timeout });
    await this.page.waitForURL(this._url, { timeout: this._timeout });
    await this.page.waitForLoadState();

    return this;
  }

  public async isOpen(): Promise<boolean> {
    await expect(this.page).toHaveTitle(this._title, { timeout: this._timeout });
    return true;
  }
}
