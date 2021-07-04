(() => {
    const includeScript = (filename) => {
        var head = document.getElementsByTagName('head')[0];
    
        var script = document.createElement('script');
        script.src = `/static/scripts${filename}`;
        script.type = 'text/javascript';
    
        head.appendChild(script)
    }
    
    const scripts = [
        '/utils.js',
        '/dialogs.js',
        '/api.js',
        '/auth.js',
        '/cookies.js',
        '/hyperbox.js',
        '/boxes/index.js',
        '/services/comments.service.js',
        '/services/posts.service.js',
        '/services/topics.service.js',
        '/topics/topics.js'
    ];
    
    scripts.forEach(includeScript);
})();
