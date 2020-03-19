"""Store :func:`.update`."""
import json
from typing import Callable, Optional

from prawcore.exceptions import Conflict


def update(
    self, transformation: Callable[[str], str], reason: Optional[str] = None
) -> None:
    """Safely update a page based on its current content.

    .. note:: Adds attribute ``update`` to :class:`praw.models.WikiPage`.

    :param transformation: A function taking the previous content as its
        sole parameter and returning the new content.
    :param reason: (Optional) The reason for the revision.

    Example code:

    .. code-block:: python

        import prawdditions.patch
        reddit = praw.Reddit(client_id='CLIENT_ID',
                             client_secret="CLIENT_SECRET",
                             password='PASSWORD',
                             user_agent='USERAGENT', username='USERNAME')
        prawdditions.patch.patch()
        def transform(content: str) -> str:
            return content + " test"
        page = next(iter(reddit.subreddit('test').wiki))
        page.update(transform)
    """
    current_revision = next(self.revisions(limit=1))
    revision_id = current_revision["id"]
    content = current_revision["page"].content_md
    new_content = transformation(content)
    while True:
        try:
            self.edit(new_content, reason=reason, previous=revision_id)
            return
        except Conflict as conflict:
            response_body = json.loads(
                conflict.response.content.decode("utf-8")
            )
            new_content = transformation(response_body["newcontent"])
            revision_id = response_body["newrevision"]
