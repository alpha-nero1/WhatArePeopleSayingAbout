Box.comment = (comment, data) => {
    const username = { data };
    const ownsComment = comment.user.username === username && !!username;
    let likesSpan;
    const initialOffset = (() => {
        if (comment.is_liked) return 1;
        if (comment.is_disliked) return -1;
        return 0;
    })();
    const numFormatter = new Intl.NumberFormat('en-GB', { notation: "compact", compactDisplay: "short" });

    const getLikeStr = () => {
        let offsetLikes = 0;
        if (comment.is_liked) offsetLikes = 1;
        else if (comment.is_disliked) offsetLikes = -1;
        let likes = comment.total_likes + (offsetLikes - initialOffset);
        let totalLikes = numFormatter.format(likes);
        return `${totalLikes || "0"} Like${likes === 1 ? '' : 's'}`
    };

    const deleteComment = () => {
        CommentsService.deleteComment(comment.id)
        .then(res => {
            if (res) {
                const comm = document.getElementById(`comment-${comment.id}`);
                comm.remove();
            }
        })
    }


    return x('div', { id: `comment-${comment.id}`, className: 'post-comment card' },
        x('p', {},
            // x('li', { className: 'far fa-comment-alt' }, ),
            x('span', {}, `${comment.user.username} - `),
            x('span', {}, comment.text)
        ),
        x('div', { }, 
            x('div', { className: 'flex-row align-center end' },
                (
                    ownsComment ? 
                    x('button', { className: 'btn link-danger', onclick: () => deleteComment(comment) }, 'Delete') 
                    :
                    null
                ),
                Box.like(
                    comment,
                    {
                        pk: 'id',
                        likeCallback: CommentsService.like,
                        dislikeCallback: CommentsService.dislike,
                        unlikeCallback: CommentsService.unlike,
                        undislikeCallback: CommentsService.undislike,
                        likeTextChangedCallback: (text) => {
                            likesSpan.innerText = text;
                        }
                    }
                ),
                x('span', { oninit: (el) => likesSpan = el }, `${comment.total_likes || "0"} Like${comment.total_likes === 1 ? '' : 's'}`)
            )
        )
    );
};