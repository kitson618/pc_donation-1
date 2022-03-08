from flask import flash
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from webconfig import FormRecognize
import requests


def authenticate_client():
    recognizer_credential = AzureKeyCredential(FormRecognize.KEY)
    form_recognizer_client = FormRecognizerClient(
        endpoint=FormRecognize.ENDPOINT,
        credential=recognizer_credential)
    return form_recognizer_client


def form_recognizer_example(path):
    # with open(path, "rb") as data:
    #     business_card = data.read()

    # poller = authenticate_client().begin_recognize_business_cards(business_card)
    # result = poller.result()

    # analyze_url = FormRecognize.ENDPOINT + "formrecognizer/v2.1-preview.3/prebuilt/businessCard/analyze"
    # image_data = path
    # headers = {'Ocp-Apim-Subscription-Key': FormRecognize.KEY,
    #            'Content-Type': 'application/json'}
    # data = {"source": image_data}
    # params = {'locale': 'en-US'}
    #
    # response = requests.post(analyze_url, headers=headers, params=params, json=data)
    # response.raise_for_status()
    # print(response)
    # test = response.json()
    # print("abc: XD")
    # print(test)

    # if you want to recognize photo from url, please use this function
    firstname = None
    lastname = None
    school_name = None
    poller = authenticate_client().begin_recognize_business_cards_from_url(path)
    result = poller.result()
    print(result)

        # for name, field in business_card.fields.items():
            # if name == "CompanyNames":
            #     flash(name)
            #     for items in field.value:
            #         for item_name, item in items.value.items():
            #             flash("...{}: {} has confidence {}".format(item_name, item.value, item.confidence))
            # else:
            #     for item in field.value:
            #         print("{}: {} has confidence {}".format(item.name, item.value, item.confidence))

    for idx, business_card in enumerate(result):
        print("--------Recognizing business card #{}--------".format(idx + 1))
        contact_names = business_card.fields.get("ContactNames")
        if contact_names:
            for contact_name in contact_names.value:
                print("Contact First Name: {} has confidence: {}".format(
                    contact_name.value["FirstName"].value, contact_name.value["FirstName"].confidence
                ))
                firstname = contact_name.value["FirstName"].value
                print("Contact Last Name: {} has confidence: {}".format(
                    contact_name.value["LastName"].value, contact_name.value["LastName"].confidence
                ))
                lastname = contact_name.value["LastName"].value
        company_names = business_card.fields.get("CompanyNames")
        if company_names:
            for company_name in company_names.value:
                print("School Name: {} has confidence: {}".format(company_name.value, company_name.confidence))
                school_name = company_name.value
        departments = business_card.fields.get("Departments")

    return firstname, lastname, school_name
