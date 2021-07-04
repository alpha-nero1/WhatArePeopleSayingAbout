const isAuthenticated = () => {
    return (getCookie('auth_token'));
}