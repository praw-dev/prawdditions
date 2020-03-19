import mock
import prawdditions.patch
import pytest

from .. import IntegrationTest


class TestPrawdditionWikiPage(IntegrationTest):
    @mock.patch("time.sleep", return_value=None)
    def test_update__no_conflict(self, _):
        prawdditions.patch.patch()
        subreddit = self.reddit.subreddit(pytest.placeholders.test_subreddit)
        page = subreddit.wiki["praw_test_page"]
        self.reddit.read_only = False
        with self.recorder.use_cassette(
            "TestPrawdditionWikiPage.test_update__no_conflict"
        ):
            page.update(lambda x: x + " | a suffix")

    @mock.patch("time.sleep", return_value=None)
    def test_update__conflict(self, _):
        prawdditions.patch.patch()
        subreddit = self.reddit.subreddit(pytest.placeholders.test_subreddit)
        page = subreddit.wiki["praw_test_page"]
        repeat = [True]
        self.reddit.read_only = False

        def update_fn(text):
            if repeat[0]:
                page.edit("A new body")
                repeat[0] = False
            return text + " | a suffix"

        with self.recorder.use_cassette(
            "TestPrawdditionWikiPage.test_update__conflict"
        ):
            page.update(update_fn)
