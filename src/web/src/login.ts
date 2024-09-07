import {doesUserExist} from "./helpers/api";
import {setElementHidden} from "./helpers/html";


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