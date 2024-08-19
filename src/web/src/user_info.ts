import axios from 'axios';

const buildElementTxt = async () => {
    const userName = window.localStorage.getItem('userName')
    if (userName) {
        const params = {username: userName}
        const url = 'http://localhost:4000/user_info'
        const response = await axios.get(url, {params});
        if (response.status === axios.HttpStatusCode.Ok) {
            return `Welcome ${response.data.first_name} ${response.data.last_name}`;
        } else {
            return `Can not get information about the user '${userName}'`;
        }
    }
    return 'Can not get information about the user: User not defined';
}

export const fetchUserInfo = async (): Promise<void> => {
    try {
        (document.getElementById('welcome-message') as HTMLElement).innerText = await buildElementTxt();
    } catch (error) {
        console.error('Error fetching user information:', error);
    }
}

(window as any).onload = fetchUserInfo;