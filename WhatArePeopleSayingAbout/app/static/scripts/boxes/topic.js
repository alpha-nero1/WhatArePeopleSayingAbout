Box.topic = (topic, data) => {
    const getSubtext = () => {
        const totalPostText = `${topic.total_posts} Post${topic.total_posts === 1 ? '' : 's'}`;
        const timestampText = `First post ${topic.naturaltime}`;
        return `${totalPostText} | ${timestampText} ago`;
    };
    return x('div', { className: 'card post', id: `topic-${topic.id}` },
        x('div', { className: 'flex-row space-between card-title' }, 
            x('a', { href: `/topics/${topic.kebab_name}` }, 
                x('h2', {}, topic.name)
            )
        ),
        x('p', {}, getSubtext())
    );
}
