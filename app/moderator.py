import json
import ast
import http.client, urllib.request, urllib.parse, urllib.error, base64

# CONTENT_MODERATOR_ENDPOINT = "https://moderatedonation.cognitiveservices.azure.com/"
subscription_key = "2c0482cd5932408680bfc33140a84362"

body = "fuck funk shit"


headers = {
    # Request headers
    'Content-Type': 'text/plain',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    # Request parameters
    'autocorrect': 'true',
    'PII': 'true',
    'listId': '',
    'classify': 'True',
    'language': '',
})

try:
    conn = http.client.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
    conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessText/Screen?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    # print(data)
    decode_data = json.loads(data.decode("utf-8").replace("'",'"'))
    if decode_data["Terms"]:
        haveTerm = True
    else:
        haveTerm = False
    results = {
        "Review":decode_data["Classification"]["ReviewRecommended"],
        "haveTerm": haveTerm,
        "term": decode_data["Terms"]
    }
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

print(results)