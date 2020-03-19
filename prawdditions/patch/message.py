from typing import Optional, Union
from praw import const
from praw.models import Redditor, Subreddit

def message(self, to: Union[Redditor, Subreddit, str], title: str, body: str,
            from_sr: Optional[Union[Subreddit, str]]=None):
    """Abstract function for sending out a message via string.

    :param to: Destination of the message.
    :param title: The subject line of the message.
    :param body: The body of the message.
    :param from_sr: A Subreddit instance of string to send the message from.
        By default the message originates from the user.
    :returns: An instance of :class:`praw.models.Message`.

    example:

    .. code-block:: python

    reddit = praw.Reddit(client_id='CLIENT_ID',
                         client_secret="CLIENT_SECRET", password='PASSWORD',
                         user_agent='USERAGENT', username='USERNAME')
    reddit.message('username','title','body')

    """
    dest = str(to)
    if isinstance(to, Subreddit): # Subreddits need to be prefixed with `/r/`
        dest = "/r/" + dest
    data = {'subject': title,
            'text': body,
            'to': dest}
    if from_sr:
        data['from_sr'] = str(from_sr)
    return self.post(const.API_PATH['compose'], data=data)
