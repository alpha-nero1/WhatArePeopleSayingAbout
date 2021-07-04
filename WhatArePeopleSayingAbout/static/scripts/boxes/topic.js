Box.topic = (topic, data) => {
    return x('div', { className: 'card post', id: `topic-${topic.id}` },
        x('div', { className: 'flex-row space-between card-title' }, 
            x('a', { href: `/topics/${topic.kebab_name}` }, 
                x('h2', {}, topic.name)
            )
        ),
        x('p', {}, `${topic.total_posts} Post${topic.total_posts === 1 ? '' : 's'}`)
    )
}