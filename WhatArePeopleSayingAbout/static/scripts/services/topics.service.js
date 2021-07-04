const TopicsService = (() => {
    const api = Api(`${getCookie('endpoints_url')}/api/topics/`);

    const listTrending = (page) => api.get(`trending?page=${page}`)
    const search = (page) => api.get(`search?topic=${topic}&page=${page}`)

    return {
        listTrending,
        search
    };
})();