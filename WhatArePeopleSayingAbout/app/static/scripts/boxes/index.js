const Box = { };

(() => {
    const includeScript = (filename) => {
        var head = document.getElementsByTagName('head')[0];
    
        var script = document.createElement('script');
        script.src = `/static/scripts${filename}`;
        script.type = 'text/javascript';
    
        head.appendChild(script)
    }
    
    const scripts = [
        './boxes/like.js',
        '/boxes/comment.js',
        '/boxes/post.js',
        '/boxes/topic.js'
    ];
    
    scripts.forEach(includeScript);
})();