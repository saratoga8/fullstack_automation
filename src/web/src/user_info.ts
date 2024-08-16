import axios from 'axios';

async function fetchUserInfo(userName: string): Promise<any> {
    try {
        const response = await axios.get('http://localhost:4000/user_info', {
            params: {
                username: userName
            },
        });

        if (response.status === axios.HttpStatusCode.Ok) {
            const userInfo = await response.data.json();
            const { first_name, last_name } = userInfo;

            return `Welcome ${first_name} ${last_name}`;
        }
        else {
            throw new Error('Network response was not ok');
        }
    } catch (error) {
        console.error('Error fetching user information:', error);
    }
}

// Call the function to fetch and display user information
(window as any).fetchUserInfo = fetchUserInfo
