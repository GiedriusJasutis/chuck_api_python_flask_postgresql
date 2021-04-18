import requests

# Initial Joke
def get_jokes():
  return requests.get('https://api.chucknorris.io/jokes/random')