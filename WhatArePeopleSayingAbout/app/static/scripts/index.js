(() => {
    const includeScript = (filename) => {
        var head = document.getElementsByTagName('head')[0];
    
        var script = document.createElement('script');
        script.src = `/static/static/scripts${filename}`;
        script.type = 'text/javascript';
    
        head.appendChild(script)
    }
    
    const scripts = [
        '/utils.js',
        '/api.js',
        '/auth.js',
        '/cookies.js',
        '/hyperbox.js',
        '/recaptcha-utils.js',
        '/boxes/index.js',
        '/services/comments.service.js',
        '/services/posts.service.js',
        '/services/topics.service.js',
        '/topics/topics.js'
    ];
    
    scripts.forEach(includeScript);
})();
