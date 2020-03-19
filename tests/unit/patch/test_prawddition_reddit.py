import mock
from praw import const
import prawdditions.patch

from .. import UnitTest


class TestRedditPrawdditions(UnitTest):
    @mock.patch("praw.Reddit.post")
    def test_reddit_message(self, mock_post):
        prawdditions.patch.patch()
        data = {
            "to": "dummy_user",
            "subject": "dummy_subject",
            "text": "dummy_body",
        }
        self.reddit.message(data["to"], data["subject"], data["text"])
        mock_post.assert_called_with(const.API_PATH["compose"], data=data)

    @mock.patch("praw.Reddit.post")
    def test_reddit_message_with_sr_and_subreddit(self, mock_post):
        prawdditions.patch.patch()
        data = {
            "to": self.reddit.subreddit("testing"),
            "subject": "dummy_subject",
            "text": "dummy_body",
            "from_sr": self.reddit.subreddit("test"),
        }
        self.reddit.message(
            data["to"], data["subject"], data["text"], from_sr=data["from_sr"]
        )
        mock_post.assert_called_with(
            const.API_PATH["compose"],
            data={
                k: str(v) if k != "to" else "/r/" + str(v)
                for k, v in data.items()
            },
        )
