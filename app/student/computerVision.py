# if you choose global environment to store the subscription key, uncomment line 2-3 & line 7 -15
# import os
# import sys
import requests
from app.support.computerVisionVar import subscription_key, endpoint



if subscription_key is not None and endpoint is not None:

    analyze_url = endpoint + "vision/v3.1/analyze"

    # Set image_path to the local path of an image that you want to analyze.
    # Sample images are here, if needed:
    # https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/ComputerVision/Images
    # Change the image_path to post method path
    image_path = "./photos/asian_student.jpg"
    
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Description,Faces,Adult'}
    # params = {'visualFeatures': 'Faces'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    
    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    
    # Show the detail of the analysis
    print(analysis)
    
    # # Check if the photo have not the adult content and have a face
    # if analysis["adult"]["isAdultContent"] or not len(analysis['faces']) == 1:
    #     # The photo cannot upload since it have wrong condition
    #     print("None")
    # else:
    #     # Do some function in here (e.g.: upload photos)
    #     print("OK")

    # For stdent page, it should check the age of the student
    # Next step is check the picture's age is range 6 to 29 or not, please un comment below code
    
    # Check if the photo have not the adult content and have a face
    if analysis["adult"]["isAdultContent"] or not len(analysis['faces']) == 1:
        # The photo cannot upload since it have wrong condition
        print("None")
    else:
        # Do some function in here (e.g.: upload photos)
        if analysis['faces'][0]['age'] < 6 and  analysis['faces'][0]['age'] >= 30:
            print("None")
        else:
            # Do some function in here (e.g.: upload photos)
            print("Suitable age")
