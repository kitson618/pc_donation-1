import json
from uuid import uuid4

from requests import post

from webconfig import AITranslate


def ai_translate(words, to='zh-Hant'):
    params = {
        'api-version': '3.0',
        # 'to': ['en'],
        'to': [to],
        'includeSentenceLength': True
    }

    headers = {
        'Ocp-Apim-Subscription-Key': AITranslate.subscription_key,
        'Ocp-Apim-Subscription-Region': AITranslate.location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': words
    }]

    request = post(AITranslate.constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    # flash(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

    translated_text = json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
    translated_text = json.loads(translated_text)
    print(translated_text)
    translated_content = translated_text[0]["translations"][0]["text"]
    source_length = translated_text[0]["translations"][0]["sentLen"]["srcSentLen"]
    source_length = sum(source_length)
    translated_length = translated_text[0]["translations"][0]["sentLen"]["transSentLen"]
    translated_length = sum(translated_length)
    print("Source content length: " + str(source_length))
    # flash("Source content length: " + str(source_length))
    print("Translated Text Length: " + str(translated_length))
    # flash("Translated Text Length: " + str(translated_length))

    translated_text_array = [translated_content]
    print("Translated Text: " + "\"" + translated_content + "\"")
    # flash("Translated Text: " + "\"" + translated_content + "\"")

    # result = [
    #     source_length,
    #     translated_length,
    #     translated_text_array
    # ]

    return source_length, translated_length, translated_text_array
