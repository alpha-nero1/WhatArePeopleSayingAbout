// Opts contains likeCallback, unlikeCallback, dislikeCallback and undislikeCallback
// that all accept the entity id as the param and execute the actual crud operation.
// The opts also contains a likeTextChangedCallback
Box.like = (entity, opts) => {
    let likeBtn;
    let dislikeBtn;

    const initialOffset = (() => {
        if (entity.is_liked) return 1;
        if (entity.is_disliked) return -1;
        return 0;
    })();

    const numFormatter = new Intl.NumberFormat('en-GB', { notation: "compact", compactDisplay: "short" });

    const getLikeStr = () => {
        let offsetLikes = 0;
        if (entity.is_liked) offsetLikes = 1;
        else if (entity.is_disliked) offsetLikes = -1;
        let likes = entity.total_likes + (offsetLikes - initialOffset);
        let totalLikes = numFormatter.format(likes);
        return `${totalLikes}`
    };

    const likeEntity = ({ target }) => {
        if (!isAuthenticated()) return;
        if (entity.is_liked) {
            // Undo the like.
            opts.unlikeCallback(entity[opts.pk || 'id'])
            .then((res) => {
                entity.is_liked = false;
                entity.is_disliked = false;
                likeBtn.classList.remove('active');
                if (opts.likeTextChangedCallback) opts.likeTextChangedCallback(getLikeStr());
            });
        } else {
            // Like the entity.
            opts.likeCallback(entity[opts.pk || 'id'])
            .then((res) => {
                entity.is_liked = true;
                entity.is_disliked = false;
                likeBtn.classList.add('active');
                dislikeBtn.classList.remove('active');
                if (opts.likeTextChangedCallback) opts.likeTextChangedCallback(getLikeStr());
            });
        }
    }

    const dislikeEntity = ({ target }) => {
        if (!isAuthenticated()) return;
        if (entity.is_disliked) {
            // Undo the dislike.
            opts.undislikeCallback(entity[opts.pk || 'id'])
            .then((res) => {
                entity.is_disliked = false;
                entity.is_liked = false;
                target.classList.remove('active');
                if (opts.likeTextChangedCallback) opts.likeTextChangedCallback(getLikeStr());
            });
        } else {
            // Disike the entity.
            opts.dislikeCallback(entity[opts.pk || 'id'])
            .then((res) => {
                entity.is_disliked = true;
                entity.is_liked = false;
                likeBtn.classList.remove('active');
                dislikeBtn.classList.add('active');
                if (opts.likeTextChangedCallback) opts.likeTextChangedCallback(getLikeStr());
            });
        }
    }

    const disabledClass = isAuthenticated() ? '' : 'disabled'

    return x('div', { className: `flex-row-small align-center ${opts.className || ''}` },
        x('i', {
            className: `far fa-thumbs-up link-btn${entity.is_liked ? ' active': ''} ${disabledClass}`,
            onclick: (ev) => likeEntity(ev),
            oninit: (el) => likeBtn = el
        }),
        x('i', { 
            className: `far fa-thumbs-down link-btn${entity.is_disliked ? ' active': ''} ${disabledClass}`,
            onclick: (ev) => dislikeEntity(ev),
            oninit: (el) => dislikeBtn = el
        })
    );
}
