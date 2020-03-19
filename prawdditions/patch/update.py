import json

from prawcore.exceptions import Conflict

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

