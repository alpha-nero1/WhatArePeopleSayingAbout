// The JavaScript file for the TOPIC page.
(() => {

    const postOnLike = (postIndex, postUuid) => {
        const totalLikes = document.getElementById(`post-${postIndex}-total-likes`);
        totalLikes.innerText = (+totalLikes.innerText + 1)
    }

    const postOnDislike = (postIndex, postUuid) => {
        const totalLikes = document.getElementById(`post-${postIndex}-total-likes`);
        totalLikes.innerText = (+totalLikes.innerText - 1)
    }

    const loadAllPostButtonListeners = () => {
        let nextPost = true;
        let i = 0;
        while (nextPost) {
            const currentIndex = i
            const post = document.getElementById(`post-${currentIndex}`)
            if (!post) {
                // End of the line.
                nextPost = false;
                return;
            }
            const likeButton = document.getElementById(`post-${currentIndex}-like`)
            const dislikeButton = document.getElementById(`post-${currentIndex}-dislike`)
            if (!likeButton || !dislikeButton) return;
            likeButton.addEventListener('click', () => postOnLike(currentIndex, post.dataset.postuuid))
            dislikeButton.addEventListener('click', () => postOnDislike(currentIndex, post.dataset.postuuid))
            i += 1;
        }
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
                if (!posts.next && loadMoreBtn) {
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