from webconfig import ai_analyze
import requests
from flask_babel import _


def vision_analyze(photo_path, check_age_range=False):
    if ai_analyze.subscription_key is not None and ai_analyze.endpoint is not None:
        analyze_url = ai_analyze.endpoint + "vision/v3.1/analyze"
        headers = {
            'Ocp-Apim-Subscription-Key': ai_analyze.subscription_key,
            'Content-Type': 'application/json'
        }
        params = {'visualFeatures': 'Description,Faces,Adult'}
        data = {"url": photo_path}
        response = requests.post(analyze_url,
                                 headers=headers,
                                 params=params,
                                 json=data)
        response.raise_for_status()
        analysis = response.json()
        print(analysis)
        if len(analysis['faces']) == 0:
            print("No face")
            return _('Invalid Photo: Unable to recognize any faces!')
        elif analysis["adult"]["isAdultContent"]:
            print("Adult Content")
            return _('Invalid Photo: Adult Content!')
        elif analysis["adult"]["isGoryContent"]:
            print("Gory Content")
            return _('Invalid Photo: Gory Content!')
        elif analysis["adult"]["isRacyContent"]:
            print("Racy Content")
            return _('Invalid Photo: Racy Content!')
        elif check_age_range:
            # Do some function in here (e.g.: upload photos)
            if analysis['faces'][0]['age'] < 6 or analysis['faces'][0]['age'] >= 30:
                return _(
                    'Invalid Photo: our AI infers you are under age 6 or over 30!'
                )
    return None


