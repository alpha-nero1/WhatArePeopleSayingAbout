const TITLE_SPAN_ID = 'wapsa-title-span';
const TOPIC_INPUT_ID = 'wapsa-topic-input';
const POST_INPUT_ID = 'wapsa-post-input';

// Keep inside function scope.
(() => {
    let titleAnimationTimeout = null;

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
            clearTimeout(titleAnimationTimeout);
            titleSpan.innerText = srcElement.value;
            if (!srcElement.value.length)
            {
                startTitleAnimation();
            }
            const newPlaceholder = (
                srcElement.value ?
                `What are you saying about ${srcElement.value || '...'}?` :
                `What are you saying about... ?`
            );
            postInput.placeholder = newPlaceholder;
        }
    
        topicInput.addEventListener('keyup', topicOnKeypress, false);
    }

    // Animate the title span to show different topic examples...
    const startTitleAnimation = () => {
        const titles = [
            'Cats', 'Lockdown', 'Dogs', 'Football', 'Coding', 
            'Cooking', 'Sleep', 'Games', 'Gardening', 'Plants',
            'School', 'Australia', 'Sport', 'Language', 'Europe',
            'USA', 'The Postman', 'The Weather', 'Design', 'Food'
        ];
        const titleSpan = document.getElementById(TITLE_SPAN_ID);
        titleSpan.innerText = titles[0]
        let currentIndex = 1;
        const animateTitle = () => {
            titleAnimationTimeout = setTimeout(() => {
                animateTitle();
                titleSpan.classList.remove('fade-in');
                titleSpan.innerText = titles[currentIndex];
                void titleSpan.offsetWidth; 
                titleSpan.classList.add('fade-in');
                
                if (currentIndex >= titles.length - 1) currentIndex = 0;
                else currentIndex++;
            }, 3000);
        }
        animateTitle();
    }

    const windowOnLoaded = () => {
        listenLoadMoreTopicsButton();
        listenTopicChange();
        startTitleAnimation();
    }    
    window.addEventListener('load', windowOnLoaded, false);
})();
