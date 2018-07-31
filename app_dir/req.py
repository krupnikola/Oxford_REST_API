import requests
import json
from flask import current_app


def find_sentences(word, language):
    url = 'https://od-api.oxforddictionaries.com/api/v1/entries/' + language + '/' + word.lower() + '/sentences'
    auth = {'app_key': current_app.config['API_KEY'], 'app_id': current_app.config['API_ID']}

    r = requests.get(url, headers=auth)
    try:
        prefix = r.json()['results'][0]['lexicalEntries'][0]['sentences']
        results = []
        if len(prefix) < 5:
            for i in range(len(prefix)):
                results.append(prefix[i]['text'])
        else:
            for i in range(5):
                results.append(prefix[i]['text'])
        return results
    except json.JSONDecodeError:
        return 'Not found.'
