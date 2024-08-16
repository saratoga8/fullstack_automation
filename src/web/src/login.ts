import axios from 'axios';

const submitLogin = async () => {
    const username = (document.getElementById('username') as HTMLInputElement).value;
    const password = (document.getElementById('password') as HTMLInputElement).value;

    if (username === '' || password === '') {
        (document.getElementById('warning') as HTMLElement).hidden = false
        return;
    }

    try {
        const response = await axios.get('http://localhost:3000/user', {
            params: {
                username: username,
                password: password,
            },
        });

        if (response.status === axios.HttpStatusCode.Ok) {
            (document.getElementById('warning') as HTMLElement).hidden = true
            window.location.href = `http://localhost:3000/welcome/${username}`;
        }
        else {
            (document.getElementById('warning') as HTMLElement).hidden = false
            console.debug(`Request failed with status ${response.status}`);
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            const status = error.response && error.response.status;
            if (status === axios.HttpStatusCode.NotFound) {
                (document.getElementById('warning') as HTMLElement).hidden = false
            }
        }
        else {
            console.error(`Error while trying to login with username ${username}: ${error}`);
        }
    }
};

// Expose the function to the global scope so it can be called from the HTML
(window as any).submitLogin = submitLogin;