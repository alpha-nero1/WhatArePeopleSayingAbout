const PostsService = (() => {
    const api = Api(`${getCookie('endpoints_url')}/api/posts/`);

    const deletePost = (postUuid) => {
        return api.del(
            'delete', 
            {
                body: { 
                    uuid: postUuid
                }
            }
        );
    }

    const createPost = (topic, text) => {
        return api.post(
            'create', 
            {
                body: { 
                    topic,
                    text
                }
            }
        )
    }

    const list = (topic, page) => api.get(`list?topic=${topic}&page=${page}`)
    
    const like = (postUuid) => api.post('like', { 
        body: {
            post_uuid: postUuid
        }
    });

    const unlike = (postUuid) => api.post('unlike', { 
        body: {
            post_uuid: postUuid
        }
    });

    const dislike = (postUuid) => api.post('dislike', { 
        body: {
            post_uuid: postUuid
        }
    });

    const undislike = (postUuid) => api.post('undislike', { 
        body: {
            post_uuid: postUuid
        }
    });

    return {
        createPost,
        deletePost,
        list,
        like,
        unlike,
        dislike,
        undislike
    }
})();