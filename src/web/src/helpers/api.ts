import axios from 'axios';

const url: string = `${process.env.API_URL}/user`;


export const doesUserExist = async (username: string, password: string) => {
    if (username && password) {
        try {
            const response = await axios.get(url, {
                auth: {username, password},
            });
            if (response.status === axios.HttpStatusCode.Ok) {
                return true
            }
            if (response.status === axios.HttpStatusCode.NotFound) {
                return false;
            }
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error('Error while adding user info: ' + error.message);
            }
        }
    } else {
        throw new Error('Invalid username or password');
    }
}
