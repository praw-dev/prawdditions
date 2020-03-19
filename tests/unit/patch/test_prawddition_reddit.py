import mock
from praw import const
import prawdditions.patch

from .. import UnitTest

class TestRedditPrawdditions(UnitTest):

  @mock.patch('praw.Reddit.post')
  def test_reddit_message(self, mock_post):
    prawdditions.patch.patch()
    data = {
      'to':'dummy_user',
      'subject':'dummy_subject',
      'text':'dummy_body'
    }
    self.reddit.message(data['to'],data['subject'],data['text'])
    mock_post.assert_called_with(const.API_PATH['compose'],data=data)
