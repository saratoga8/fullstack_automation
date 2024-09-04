export const submit = () => {
    const userInfo = {
        name: (document.getElementById('username') as HTMLInputElement).value,
        password: (document.getElementById('password') as HTMLInputElement).value,
        first_name: (document.getElementById('firstName') as HTMLInputElement).value,
        last_name: (document.getElementById('lastName') as HTMLInputElement).value,
    }
}

(window as any).submit = submit;