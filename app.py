from flask import Flask
import requests
import stanza
from quantulum3 import parser

app = Flask(__name__)


@app.route("/<seed>/<lang>")
def index(seed, lang):
    if ',' in seed:
        seed = seed.replace(',', ' , ')
    nlp = stanza.Pipeline(str(lang), use_gpu=False,
                          processors='tokenize,pos,lemma')
    doc = nlp(seed)
    res = {'data': []}
    translated_text = ""
    for sent in doc.sentences:
        if lang != 'en':
            temp = sent.text.replace(',', 'and')
            url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

            querystring = {"q": temp, "langpair": lang + "|en", "de": "a@b.c", "onlyprivate": "0", "mt": "1"}

            headers = {
                'x-rapidapi-key': "fedcecb517msh4b38401fd4b1c46p102514jsnf278bf4c4523",
                'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            translated_text = response.json()['responseData']['translatedText']
            print(translated_text)

        else:
            translated_text = sent.text

        quants = parser.parse(translated_text)
        for q in quants:
            if q.unit.entity.name == 'length':
                res['data'].append([float(q.surface.split()[0]), q.surface.split()[1]])
    if len(res['data']) > 0:
        print(res)
        print(len(res))
        del doc
    else:
        res['type'] = 'entity'

    nlp = stanza.Pipeline(str('en'), use_gpu=False,
                          processors='tokenize,pos,lemma')
    doc = nlp(translated_text)
    for sent in doc.sentences:
        for word in sent.words:
            res['data'].append([word.lemma, word.upos, word.text])
    i = 0
    for w in res['data']:
        w.append(i)
        i = 0
        if w[1] == 'NUM':
            i = int(w[0])
    for w in res['data']:
        if w[1] == 'NOUN':
            translated_word = w[0]

            url = "https://bing-image-search1.p.rapidapi.com/images/search/"

            querystring = {"q": str(translated_word) + " Cartoon Clip Art transparent "}

            headers = {
                'x-rapidapi-key': "fedcecb517msh4b38401fd4b1c46p102514jsnf278bf4c4523",
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            if response.json()['value']:
                w[0] = response.json()['value'][1]['contentUrl']
                print(w[0])
            else:
                w[1] = 'NOUN_'
        if w[1] == 'PROPN':
            r2 = requests.get("https://api.genderize.io?name=" + w[0])
            gender = r2.json()['gender']
            if gender == 'female':

                url = "https://bing-image-search1.p.rapidapi.com/images/search/"

                querystring = {"q": "Girl Cartoon Clip Art transparent"}

                headers = {
                    'x-rapidapi-key': "fedcecb517msh4b38401fd4b1c46p102514jsnf278bf4c4523",
                    'x-rapidapi-host': "bing-image-search1.p.rapidapi.com"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                if response.json()['value']:
                    w[0] = response.json()['value'][0]['contentUrl']
                    print(w[0])

            else:
                translated_word = w[0]
                print(translated_text)

                url = "https://bing-image-search1.p.rapidapi.com/images/search/"

                querystring = {"q": "Boy Cartoon Clip Art transparent"}

                headers = {
                    'x-rapidapi-key': "fedcecb517msh4b38401fd4b1c46p102514jsnf278bf4c4523",
                    'x-rapidapi-host': "bing-image-search1.p.rapidapi.com"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                if response.json()['value']:
                    w[0] = response.json()['value'][0]['contentUrl']
                    print(w[0])
    print(res)
    del doc
    return res


if __name__ == '__main__':
    app.run()
