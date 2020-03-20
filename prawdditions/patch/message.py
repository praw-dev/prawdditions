"""Store :func:`.message`."""
from typing import Optional, Union
from praw import const
from praw.models import Message, Redditor, Subreddit


def message(
    self,
    to: Union[Redditor, Subreddit, str],
    title: str,
    body: str,
    from_sr: Optional[Union[Subreddit, str]] = None,
) -> Message:
    """Abstract function for sending out a message via string.

    .. note:: Adds attribute ``message`` to :class:`praw.Reddit`.

    :param to: Destination of the message.
    :param title: The subject line of the message.
    :param body: The body of the message.
    :param from_sr: A Subreddit instance of string to send the message from.
        By default the message originates from the user.
    :returns: An instance of :class:`praw.models.Message`.

    Example code:

    .. code-block:: python

        import prawdditions.patch
        reddit = praw.Reddit(client_id='CLIENT_ID',
                             client_secret="CLIENT_SECRET",
                             password='PASSWORD',
                             user_agent='USERAGENT', username='USERNAME')
        prawdditions.patch.patch()
        reddit.message('username','title','body')
    """
    dest = str(to)
    if isinstance(to, Subreddit):  # Subreddits need to be prefixed with `/r/`
        dest = "/r/" + dest
    data = {"subject": title, "text": body, "to": dest}
    if from_sr:
        data["from_sr"] = str(from_sr)
    return self.post(const.API_PATH["compose"], data=data)
