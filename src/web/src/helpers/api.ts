import axios from 'axios';

const url: string = `${process.env.API_URL}/user`;


export const doesUserExist = async (username: string, password: string) => {
    if (username && password) {
        const response = await axios.get(url, {
            auth: {username, password},
        });
        if (response.status === axios.HttpStatusCode.Ok) {
            return true
        }
        if (response.status === axios.HttpStatusCode.NotFound) {
            return false;
        }
        throw new Error('Invalid status code: ' + response.status);
    }
}
