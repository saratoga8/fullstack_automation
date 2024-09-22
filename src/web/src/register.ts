import {getElementValue, setElementHidden} from "./helpers/html";
import axios, {AxiosResponse} from "axios";

type UserInfo = {
    name: string,
    password: string,
    first_name: string,
    last_name: string,
}

const getUserInfo = (): UserInfo => {
    return {
        name: getElementValue('username'),
        password: getElementValue('password'),
        first_name: getElementValue('firstName'),
        last_name: getElementValue('lastName'),
    }
}

enum RequestResult {
    OK, SERVER_ERROR, USER_EXISTS, INVALID_VALUES
}

type RequestResultInfo = { result: RequestResult, errTxt?: string }

const url: string = process.env.API_URL ?? 'http://localhost:8000'

const errorID = 'error'
const warningID = 'warning'

const buildResultInfo = (response: AxiosResponse): RequestResultInfo => {
    switch (response.status) {
        case axios.HttpStatusCode.Created:
            return {result: RequestResult.OK};
        case axios.HttpStatusCode.Conflict:
            return {result: RequestResult.USER_EXISTS}
        case axios.HttpStatusCode.BadRequest:
            return {result: RequestResult.INVALID_VALUES, errTxt: response.data.error}
        default:
            console.error(`Error while adding user info: Status ${response.status}: ${response.statusText}`);
            return {result: RequestResult.SERVER_ERROR}
    }
}

const sendAddUserRequest = async (userInfo: UserInfo): Promise<RequestResultInfo> => {
    try {
        const nonExceptionalStatuses = (status: RequestResult) => status < axios.HttpStatusCode.InternalServerError
        const response = await axios.post(`${url}/user`, userInfo, {validateStatus: nonExceptionalStatuses});
        return buildResultInfo(response)
    } catch (error) {
        console.error(`Error while adding user info: ${error}`);
    }
    return {result: RequestResult.SERVER_ERROR}
}

const showErrors = (resultInfo: RequestResultInfo, userName: string) => {
    if (resultInfo.result === RequestResult.USER_EXISTS) {
        (document.getElementById(warningID) as HTMLElement).innerText = `User ${userName} already exists`;
        setElementHidden(warningID, false)
    } else if (resultInfo.result === RequestResult.INVALID_VALUES) {
        (document.getElementById(warningID) as HTMLElement).innerText = resultInfo.errTxt ?? "Invalid values";
        setElementHidden(warningID, false)
    } else if (resultInfo.result === RequestResult.SERVER_ERROR) {
        setElementHidden(errorID, false)
    } else {
        (document.getElementById(errorID) as HTMLElement).innerText = "Unknown error";
        setElementHidden(errorID, false)
    }
}

const addNewUser = async (userInfo: UserInfo): Promise<void> => {
    const resultInfo = await sendAddUserRequest(userInfo)
    if (resultInfo.result === RequestResult.OK) {
        window.localStorage.setItem('userName', userInfo.name);
        window.location.href = `/success`;
    } else {
        showErrors(resultInfo, userInfo.name)
    }
}

const sendForm = async () => {
    const userInfo = getUserInfo()

    setElementHidden(errorID, true)
    setElementHidden(warningID, true)
    try {
        await addNewUser(userInfo)
    } catch (error) {
        setElementHidden(errorID, false)
        console.error(`Error while trying to add a user: ${error}`);
    }
}

(window as any).sendForm = sendForm;