# Html meta configurations
META_CONFIG = {
    'LoginView': {
        'keywords': 'login, log in, log in to whatarepeoplesayingabout.com',
        'description': 'Log in to whatarepeoplesayingabout.com'
    },
    'SignupView': {
        'keywords': 'signup, sign up, sign up to whatarepeoplesayingabout.com',
        'description': 'Sign up to whatarepeoplesayingabout.com'
    },
    'HomeView': {
        'keywords': 'home, feed, home page, main',
        'description': 'whatarepeoplesayingabout.com home page'
    }
}

# Utility function to get the correct meta data for our html pages.
def get_meta(view_name):
    return META_CONFIG[view_name];


def get_topic_meta(topic):
    return {
        'keywords': 'What are people saying about ' + topic.name + '? Find out and have your say!, ' + topic.name,
        'description': 'What are people saying about ' + topic.name
    }


def get_post_meta(post):
    return {
        'keywords': post.topic.name + ', ' + post.text,
        'description': post.topic.name + ' | ' + post.text
    }