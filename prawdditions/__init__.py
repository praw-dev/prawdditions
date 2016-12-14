from .const import __version__
from praw import Reddit, const

def message(self, to, title, body, from_sr=None):
  """
  Abstract function for sending out a message via string.

  :param to: Destination of the message.
  :param title: The subject line of the message.
  :param body: The body of the message.
  :param from_sr: A Subreddit instance of string to send the message from. By default the message originates from the user.
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


"""
Attach the message function to the Reddit object.
Instantiations of the reddit object will now contain the message function.
"""
Reddit.message = message
