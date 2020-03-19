"""PRAWdditions Unit Test Suite."""

from praw import Reddit


class UnitTest(object):
    def setup(self):
        self.reddit = Reddit(
            client_id="dummy", client_secret="dummy", user_agent="dummy"
        )

        self.reddit._core._requestor._http = None
