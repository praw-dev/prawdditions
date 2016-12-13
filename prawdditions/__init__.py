from .const import __version__
from praw import Reddit, const

def message(self, to, title, body, from_sr=None):
  data = {'subject': title,
          'text': body,
          'to': to}
  if from_sr:
    data['from_sr'] = str(from_sr)
  return self.post(const.API_PATH['compose'], data=data)

Reddit.message = message
