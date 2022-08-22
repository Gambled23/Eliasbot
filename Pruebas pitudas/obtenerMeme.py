from requests import get
import json

print(get('https://meme-api.herokuapp.com/gimme').text)

