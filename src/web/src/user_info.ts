import axios from 'axios';

type UserInfo = { firstName: string; lastName: string };

const url: string = `${process.env.API_URL}/user_info`;

const getUserInfo = async (userName: string): Promise<UserInfo | null> => {
    const params = {username: userName}
    const response = await axios.get(url, {params});
    try {
        if (response.status === axios.HttpStatusCode.Ok) {
            return {firstName: response.data.first_name, lastName: response.data.last_name};
        } else {
            console.error(`Error while requesting user info: Status ${response.status}: ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Error while trying to login with username ${userName}: ${error}`);
    }
    return null;
}

const buildElementTxt = async () => {
    const userName = window.localStorage.getItem('userName')
    if (userName) {
        const userInfo = await getUserInfo(userName)
        const errTxt = `Can not get information about the user '${userName}'`
        return (userInfo) ? `Welcome ${userInfo.firstName} ${userInfo.lastName}` : errTxt
    }
    return 'Cannot get information about the user: User not defined';
}

export const fetchUserInfo = async (): Promise<void> => {
    try {
        (document.getElementById('welcome-message') as HTMLElement).innerText = await buildElementTxt();
    } catch (error) {
        console.error('Error fetching user information:', error);
    }
}

(window as any).onload = fetchUserInfo;