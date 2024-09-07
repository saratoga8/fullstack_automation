import {faker} from "@faker-js/faker";

export type UserInfo = {
    name: string,
    password: string,
    last_name: string,
    first_name: string,
}

export const buildUserInfo = (): UserInfo => {
    return {
        name: faker.internet.userName(),
        password: faker.internet.password(),
        last_name: faker.person.lastName(),
        first_name: faker.person.firstName(),
    }
}