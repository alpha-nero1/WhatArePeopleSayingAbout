Box.post = (post, data) => {
    const { username } = data;
    const ownsPost = post?.user?.username === username && !!username;
    const postUsername = post?.user?.username ? post.user.username : 'Anonymous';
    let likesTitle;

    const initialOffset = (() => {
        if (post.is_liked) return 1;
        if (post.is_disliked) return -1;
        return 0;
    })();
    const numFormatter = new Intl.NumberFormat('en-GB', { notation: "compact", compactDisplay: "short" });

    const getLikeStr = () => {
        let offsetLikes = 0;
        if (post.is_liked) offsetLikes = 1;
        else if (post.is_disliked) offsetLikes = -1;
        let likes = post.total_likes + (offsetLikes - initialOffset);
        let totalLikes = numFormatter.format(likes);
        return `${totalLikes}`
    };

    const deletePost = () => {
        PostsService.deletePost(post.uuid)
        .then(res => {
            if (res) {
                const postEl = document.getElementById(`post-${post.id}`);
                if (!postEl) return;
                postEl.remove();
            }
        })
    }

    return x('div', { className: 'card post', id: `post-${post.id}` },
        x('div', { className: 'flex-row space-between card-title' }, 
            x('a', { href: `/topics/${post.topic.kebab_name}/${post.uuid}` }, 
                x('h2', {}, post.text)
            ),
            x('h2', { oninit: (el) => likesTitle = el }, getLikeStr())
        ),
        x('div', { className: 'flex-row-end align-center' },
            (
                ownsPost ? 
                x('button', { className: 'btn link-danger', onclick: deletePost }, 'Delete') 
                :
                null
            ),
            Box.like(
                post,
                {
                    pk: 'uuid',
                    likeCallback: PostsService.like,
                    dislikeCallback: PostsService.dislike,
                    unlikeCallback: PostsService.unlike,
                    undislikeCallback: PostsService.undislike,
                    likeTextChangedCallback: (text) => {
                        likesTitle.innerText = text;
                    }
                }
            ),
            x('span', {}, `- ${postUsername}`)
        )
    )
}