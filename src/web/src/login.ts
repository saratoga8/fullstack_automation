import axios from 'axios';

const url: string = `${process.env.API_URL}/user`;

type elementId = 'warning' | 'error'

const doesUserExist = async (username: string, password: string) => {
    if (username && password) {
        const response = await axios.get(url, {params: {username, password}});
        if (response.status === axios.HttpStatusCode.Ok) {
            return true
        }
        if (response.status === axios.HttpStatusCode.NotFound) {
            return false;
        }
        throw new Error('Invalid status code: ' + response.status);
    }
}

const setElementHidden = (element: elementId, hidden: boolean) => {
    (document.getElementById(element) as HTMLElement).hidden = hidden
}

const submitLogin = async () => {
    const username = (document.getElementById('username') as HTMLInputElement).value;
    const password = (document.getElementById('password') as HTMLInputElement).value;

    setElementHidden('warning', true)
    setElementHidden('error', true)

    try {
        if (await doesUserExist(username, password)) {
            window.localStorage.setItem('userName', username);
            window.location.href = `/welcome`;
        } else {
            setElementHidden('warning', false)
        }
    } catch (error) {
        setElementHidden('error', false)
        console.error(`Error while trying to login with username ${username}: ${error}`);
    }
};

(window as any).submitLogin = submitLogin;