const TITLE_SPAN_ID = 'wapsa-title-span';
const TOPIC_INPUT_ID = 'wapsa-topic-input';
const POST_INPUT_ID = 'wapsa-post-input';

// Keep inside function scope.
(() => {
    const addTopicToList = (topic) => {
        const topicList = document.getElementById('topic-list');
        const data = document.getElementById('page-data');
        const username = data.dataset.username;
        topicList.appendChild(
            createElement(
                Box.topic(topic, { username })
            )
        );
    }

    const removeLoadMoreBtn = () => {
        const loadMoreBtn = document.getElementById('next-page-load-more');
        if (!loadMoreBtn) return;
        loadMoreBtn.removeEventListener('click', this);
        loadMoreBtn.parentElement.removeChild(loadMoreBtn);
    }

    const listenLoadMoreTopicsButton = () => {
        const loadMoreBtn = document.getElementById('next-page-load-more');
        const data = document.getElementById('page-data');
        if (!loadMoreBtn || !data) return;
        let page = 1;
        loadMoreBtn.addEventListener('click', () => {
            page += 1;
            TopicsService.listTrending(page)
            .then((topics) => {
                if (topics.results) topics.results.forEach(addTopicToList);
                // If no more posts, remove btn.
                if (!topics.next) removeLoadMoreBtn();         
            });
        })
    }

    const listenTopicChange = () => {
        const titleSpan = document.getElementById(TITLE_SPAN_ID);
        const topicInput = document.getElementById(TOPIC_INPUT_ID);
        const postInput = document.getElementById(POST_INPUT_ID);
        if (!topicInput) return;
    
        const topicOnKeypress = ({ srcElement }) => {
            titleSpan.innerText = srcElement.value;
            const newPlaceholder = (
                srcElement.value ?
                `What are you saying about ${srcElement.value || '...'}?` :
                `What are you saying about... ?`
            );
            postInput.placeholder = newPlaceholder;
        }
    
        topicInput.addEventListener('keyup', topicOnKeypress, false);
    }

    const windowOnLoaded = () => {
        listenLoadMoreTopicsButton();
        listenTopicChange();
    }    
    window.addEventListener('load', windowOnLoaded, false);
})();
