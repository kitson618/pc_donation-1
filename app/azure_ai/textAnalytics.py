# use this code if you're using SDK version is 5.0.0
from flask import flash
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from webconfig import AITextAnalytics


def authenticate_client():
    ta_credential = AzureKeyCredential(AITextAnalytics.key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=AITextAnalytics.endpoint,
        credential=ta_credential)
    return text_analytics_client


# client = authenticate_client()


def sentiment_analysis_example(client, words):
    response = client.analyze_sentiment(documents=words)[0]
    print("Document Sentiment: {}".format(response.sentiment))
    # flash("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    # flash("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
    #     response.confidence_scores.positive,
    #     response.confidence_scores.neutral,
    #     response.confidence_scores.negative,
    # ))
    print("Total sentence: {}".format(len(response.sentences)))
    # flash("Total sentence: {}".format(len(response.sentences)))
    for idx, sentence in enumerate(response.sentences):
        print("Sentence: {}".format(sentence.text))
        print("Sentence {} sentiment: {}".format(idx + 1, sentence.sentiment))
        print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))
    # for idx, sentence in enumerate(response.sentences):
    # flash("Sentence: {}".format(sentence.text))
    # flash("Sentence {} sentiment: {}".format(idx + 1, sentence.sentiment))
    # flash("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
    #     sentence.confidence_scores.positive,
    #     sentence.confidence_scores.neutral,
    #     sentence.confidence_scores.negative,
    # ))

    return response.confidence_scores.negative


def save_sentiment_analysis_result(client, words):
    response = client.analyze_sentiment(documents=words)[0]
    return response.sentiment, response.confidence_scores


# sentiment_analysis_example(client)


def key_phrase_extraction_example(client, words):
    try:
        response = client.extract_key_phrases(documents=words)[0]
        print(response)
        # flash(response)

        if not response.is_error:
            return response.key_phrases
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))

# key_phrase_extraction_example(client)
