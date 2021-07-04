const CommentsService = (() => {
    const api = Api(`${getCookie('endpoints_url')}/api/comments/`);

    const deleteComment = (commentId) => {
        return api.del(
            'delete', 
            {
                body: { 
                    comment_id: commentId
                }
            }
        );
    }

    const createComment = (puuid, text) => {
        return api.post(
            'create', 
            {
                body: { 
                    text,
                    post_uuid: puuid
                }
            }
        )
    }

    const list = (puuid, page) => api.get(`list?post_uuid=${puuid}&page=${page}`)
    
    const like = (commentId) => api.post('like', { 
        body: {
            comment_id: commentId
        }
    });

    const unlike = (commentId) => api.post('unlike', { 
        body: {
            comment_id: commentId
        }
    });

    const dislike = (commentId) => api.post('dislike', { 
        body: {
            comment_id: commentId
        }
    });

    const undislike = (commentId) => api.post('undislike', { 
        body: {
            comment_id: commentId
        }
    });

    return {
        createComment,
        deleteComment,
        list,
        like,
        unlike,
        dislike,
        undislike
    }
})();