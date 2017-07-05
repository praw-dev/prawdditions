import json


from praw import Reddit, const
from praw.models.reddit.wikipage import WikiPage
from prawcore.exceptions import Conflict


def message(self, to, title, body, from_sr=None):
    """Abstract function for sending out a message via string.

    :param to: Destination of the message.
    :param title: The subject line of the message.
    :param body: The body of the message.
    :param from_sr: A Subreddit instance of string to send the message from.
        By default the message originates from the user.
    :returns: The json response from the server.

    example:

    .. code-block:: python

    reddit = praw.Reddit(client_id='CLIENT_ID',
                         client_secret="CLIENT_SECRET", password='PASSWORD',
                         user_agent='USERAGENT', username='USERNAME')
    reddit.message('username','title','body')

    """
    data = {'subject': title,
            'text': body,
            'to': to}
    if from_sr:
        data['from_sr'] = str(from_sr)
    return self.post(const.API_PATH['compose'], data=data)


def update(self, transformation, reason=None):
    """Safely update a page based on its current content.

    :param transformation: A function taking the previous content as its
        sole parameter and returning the new content.
    :param reason: (Optional) The reason for the revision.

    """
    current_revision = next(self.revisions(limit=1))
    revision_id = current_revision['id']
    content = current_revision['page'].content_md
    new_content = transformation(content)
    while True:
        try:
            self.edit(new_content, reason=reason, previous=revision_id)
            return
        except Conflict as conflict:
            response_body = json.loads(conflict.response.content.decode())
            new_content = transformation(response_body['newcontent'])
            revision_id = response_body['newrevision']

"""
Attach the message function to the Reddit object.
Instantiations of the reddit object will now contain the message function.
"""
Reddit.message = message
WikiPage.update = update
