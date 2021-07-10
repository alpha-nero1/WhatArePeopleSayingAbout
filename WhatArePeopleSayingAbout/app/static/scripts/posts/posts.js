// The JavaScript file for the POST page.
(() => {

    const setCommentsLoading = (loading) => {
        commentLoader = document.getElementById('comments-loader');
        commentLoader.hidden = !loading;
    }

    const addCommentToList = (comment) => {
        const commentList = document.getElementById('post-comments-list');
        const data = document.getElementById('page-data');
        const username = data.dataset.username;
        commentList.appendChild(
            createElement(
                Box.comment(comment, { username })
            )
        );
    }

    const loadPostCommentsDom = (results, next, page) => {
        const commentFooter = document.getElementById('post-comments-footer');
        // Clean any loader that may have been inside.
        setCommentsLoading(false)
        results.forEach(addCommentToList);
        // Configure the load more button!
        for (let i = 0; i < commentFooter.children.length; i++) {
            commentFooter.removeChild(commentFooter.children[i]);
        }
        if (next) {
            commentFooter.appendChild(createElement(x(
                'button',
                {
                    id: 'load-more-button',
                    className: 'btn btn-primary',
                    onclick: () => {
                        loadPostComments(page + 1)
                    }
                },
                'Load more'
            )));
        }
    }

    const loadPostComments = (page = 1) => {
        const data = document.getElementById('page-data');
        setCommentsLoading(true)
        if (!data) return;
        const postUuid = data.dataset.postuuid;
        if (!postUuid) return;
        CommentsService.list(postUuid, page)
        .then(res => {
            const { next, results } = res;
            loadPostCommentsDom(results, next, page);
        })
    }

    const listenAddCommentButton = () => {
        const data = document.getElementById('page-data');
        if (!data) return;
        const postUuid = data.dataset.postuuid;
        const btn = document.getElementById('add-comment-button');
        if (!btn) return;
        if (!isAuthenticated()) return btn.disabled = true;
        const commentTextArea = document.getElementById('add-comment-text-area');
        btn.addEventListener('click', () => {
            btn.disabled = true;
            CommentsService.createComment(postUuid, commentTextArea.value)
            .then(({ comment }) => {
                commentTextArea.value = '';
                btn.disabled = false;
                // If successfull, add the comment to list.
                addCommentToList(comment)
            })
            .catch((err) => {
                btn.disabled = false;
                throw err;
            });
        })
    }

    const addLikeSection = () => {
        const section = document.getElementById('post-like-section');
        const post = document.getElementById('page-data');
        const likesTitle = document.getElementById('post-likes');
        const postFromData = {
            id: post.dataset.id,
            uuid: post.dataset.postuuid,
            text: post.dataset.text,
            is_liked: post.dataset.is_liked === "True" ? true : false,
            is_disliked: post.dataset.is_disliked === "True" ? true : false,
            total_likes: +post.dataset.total_likes,
            user: {
                username: post.dataset.username
            },
            topic: {
                kebab_name: post.dataset.topic_kebab_name
            }
        }
        const likeBox = Box.like(
            postFromData,
            {
                pk: 'uuid',
                likeCallback: PostsService.like,
                dislikeCallback: PostsService.dislike,
                unlikeCallback: PostsService.unlike,
                undislikeCallback: PostsService.undislike,
                likeTextChangedCallback: (text) => {
                    likesTitle.innerText = text;
                },
                className: 'post-likes'
            }
        )
        section.parentElement.replaceChild(createElement(likeBox), section);
    }

    const listenOnPostDelete = () => {
        const btn = document.getElementById('post-delete-btn');
        const post = document.getElementById('page-data');
        if (!btn || !post) return;
        btn.addEventListener('click', () => {
            btn.disabled = true;
            PostsService.deletePost(post.dataset.postuuid)
            .then(res => {
                // Post was deleted, go away.
                window.location.href = `/topics/${post.dataset.topic_kebab_name}`;
            })
            .catch(err => {
                btn.disabled = false;
                throw err;
            })
        })

    }

    const windowOnLoaded = () => {
        loadPostComments();
        listenAddCommentButton();
        addLikeSection();
        listenOnPostDelete();
    }
    
    window.addEventListener('load', windowOnLoaded, false);
})();