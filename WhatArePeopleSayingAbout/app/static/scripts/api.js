const Api = ((urlPrefix = '') => {

    const getDefaultHeaders = () => {
      return {
        'Authorization': `Bearer ${getCookie('auth_token')}`,
        'Content-Type': 'application/json'
      }
    };

    const request  = (url, opts, method) => {
      const headers = {
        ...getDefaultHeaders(),
        ...opts.headers,
      }
      return new Promise((resolve, reject) => {
        const request = new XMLHttpRequest();
        request.open(method, url)
        if (typeof headers === 'object') {
          Object.entries(headers).forEach(header => {
            request.setRequestHeader(header[0], header[1])
          })
        }
        request.onreadystatechange = () => {
          if (request.readyState === XMLHttpRequest.DONE) {
            const { status } = request;
            if (status === 0 || (status >= 200 && status < 400)) {
              resolve(JSON.parse(request.response))
            }
          }
        }
        request.onerror = reject;
        request.send(opts.body ? JSON.stringify(opts.body) : null)
      });
    };

    const post = (url, opts) => request(urlPrefix + url, opts, 'POST');
    const del = (url, opts) => request(urlPrefix + url, opts, 'DELETE');
    const get = (url) => request(urlPrefix + url, {}, 'GET');

    return { post, del, get };
});