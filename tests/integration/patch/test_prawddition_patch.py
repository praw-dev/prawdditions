from praw import Reddit
from praw.models import WikiPage
import prawdditions.patch

class TestPatch:
    def test_patch(self):
        prawdditions.patch.patch()
        assert hasattr(Reddit, "message")
        assert hasattr(WikiPage, "update")

    def test_unpatch(self):
        prawdditions.patch.unpatch()
        assert not hasattr(Reddit, "message")
        assert not hasattr(WikiPage, "update")