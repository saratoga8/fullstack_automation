import { Page, Request } from '@playwright/test';

export const mockResponse = async (
  page: Page,
  url: string,
  expectedApiResponse: object | null,
  method: string,
  status = 200
) => {
  await page.route(url, async (route) => {
    if (route.request().method() === method) {
      await route.fulfill({
        status: status,
        contentType: 'application/json',
        body: JSON.stringify(expectedApiResponse),
      });
    } else {
      await route.continue();
    }
  });
};

export const mockAmplitudeResponse = async (page: Page) => {
  await page.route('https://api.amplitude.com/', async (route) => {
    if (route.request().method() === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'text/html',
        body: 'success',
      });
    }
  });
};

export const clearMockedResponses = async (page: Page, url: string, method: string) => {
  await page.route(url, async (route) => {
    if (route.request().method() === method) {
      await route.continue();
    }
  });
};

export type RequestInfo = {
  urlEndPart: string;
  method: 'POST' | 'PUT' | 'DELETE';
  postData?: any;
  timeOutSeconds: number;
};

const convertStrToComparable = (dataStr: string) => [...dataStr].sort().join('');

export const waitForSendingRequest = (requestInfo: RequestInfo, page: Page) => {
  const predicate = (request: Request) => {
    const validUrl = request.url().endsWith(requestInfo.urlEndPart);
    const validMethod = request.method() === requestInfo.method;
    if (validMethod && validUrl && requestInfo.postData) {
      const expectedPostData = JSON.stringify(requestInfo.postData);
      const actualPostData = request.postData() as string;
      const validPostData =
        convertStrToComparable(actualPostData) === convertStrToComparable(expectedPostData);

      return validUrl && validMethod && validPostData;
    }
    return validUrl && validMethod;
  };
  return page.waitForRequest(predicate, { timeout: requestInfo.timeOutSeconds * 1000 });
};
