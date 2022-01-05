import json
#import sagemaker
import base64
#from sagemaker.serializers import IdentitySerializer
import boto3
runtime = boto3.client('runtime.sagemaker')

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2022-01-05-07-13-45-219'

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])
    
    response = runtime.invoke_endpoint(
        EndpointName = ENDPOINT,
        ContentType = 'image/png',
        Body = image)

    # # Instantiate a Predictor
    # predictor = sagemaker.Predictor(ENDPOINT)

    # # For this model the IdentitySerializer needs to be "image/png"
    # predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    inferences = json.loads(response['Body'].read())

    # We return the data back to the Step Function    
    event["inferences"] = inferences
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
