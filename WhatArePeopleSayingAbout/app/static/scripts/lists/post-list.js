(() => {

    const loadAllPostButtonListeners = () => {
        let nextPost = true;
        const data = document.getElementById('page-data');
        const postList = document.getElementById('post-list');
        const username = data.dataset.username;
        let i = 0;
        boxes = [];
        while (nextPost) {
            const currentIndex = i;
            const post = document.getElementById(`post-${currentIndex}`);
            if (!post) {
                // End of the line.
                nextPost = false;
                continue;
            }
            const postFromData = {
                id: post.dataset.id,
                uuid: post.dataset.postuuid,
                text: post.dataset.text,
                is_liked: post.dataset.is_liked === "True" ? true : false,
                is_disliked: post.dataset.is_disliked === "True" ? true : false,
                total_likes: +post.dataset.total_likes,
                naturaltime: post.dataset.naturaltime,
                user: {
                    username: post.dataset.username
                },
                topic: {
                    kebab_name: post.dataset.topic_kebab_name
                }
            }
            // Add to post list.
            boxes.push(Box.post(postFromData, { username }))
            i += 1;
        }
        // Replace current with the JS objects.
        postList.parentElement.replaceChild(
            createElement(x('div', { id: 'post-list' }, ...boxes)),
            postList
        );
    }

    const addPostToList = (post) => {
        const postList = document.getElementById('post-list');
        const data = document.getElementById('page-data');
        const username = data.dataset.username;
        postList.appendChild(
            createElement(
                Box.post(post, { username })
            )
        );
    }

    const listenLoadMorePostsButton = () => {
        const loadMoreBtn = document.getElementById('next-page-load-more');
        const data = document.getElementById('page-data');
        if (!loadMoreBtn || !data) return;
        let page = 1;
        loadMoreBtn.addEventListener('click', () => {
            page += 1;
            PostsService.list(data.dataset.topic, page)
            .then(posts => {
                if (posts.results) posts.results.forEach(addPostToList);
                // If no more posts, remove btn.
                if (!posts.next) {
                    loadMoreBtn.removeEventListener('click', this);
                    loadMoreBtn.parentElement.removeChild(loadMoreBtn);
                    return;
                }                
            });
        })
    }

    const windowOnLoaded = () => {
        listenLoadMorePostsButton();
        loadAllPostButtonListeners();
    }
    
    window.addEventListener('load', windowOnLoaded, false);
})();