import base64
import os
import json
import logging
import boto3
from chalice import Chalice

app = Chalice(app_name='april-api')
logger = app.log
logger.setLevel(logging.DEBUG)
# This environment variable is set in config.json
s3_bucket = os.environ['S3_BUCKET_NAME']

logger.info(f'Using S3 bucket: {s3_bucket}')
_S3 = None


# test endpoint
@app.route('/april')
def index():
    return {'april': 'shin'}


# Access s3 bucket
def get_s3_client():
    global _S3
    if _S3 is None:
        _S3 = boto3.client('s3')
    return _S3


# Access cloudfront
def get_cf_client():
    global _CF
    if _CF is None:
        _CF = boto3.client('cloudfront')
    return _CF


# Create a route, GET request. In this function, we will retrieve the item from S3
@app.route('/', methods=['GET'])
def retrieve(file):
    s3 = get_s3_client()
    try:
        s3_response = s3.get_object(Bucket=s3_bucket, Key='index.html')

        print("CONTENT TYPE: " + s3_response['ContentType'])
        logger.info(f'S3 bucket s3_response: {s3_response}')

        if s3_response['ContentType'] == '':
            response = {
                'statusCode': 200,
                'headers': { "Content-Type": f"{s3_response['ContentType']}"},
                'body': s3_response['Body'].read().decode('utf-8')
            }
        else:
            response = {
                'statusCode': 200,
                'headers': { "Content-Type": f"{s3_response['ContentType']}"},
                'body': base64.b64encode(s3_response['Body'].read()),
                'isBase64Encoded': True
            }

        return response

    except Exception as e:
        print(e)
        #print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


# @app.on_s3_event(bucket=s3_bucket,
#                  events=['s3:GetObject:*'])
# def handle_s3_event(event):
#     app.log.debug("Received event for bucket: %s, key: %s",
#                   event.bucket, event.key)


# @app.lambda_function(name='lambda-function')
# def lambda_handler(event, context):
#     print("Received event: " + json.dumps(event))
#     # request = app.current_request
#     s3 = get_s3_client()
#     app.log.debug("Received event for bucket: %s, key: %s", event.bucket, event.key)
#     # Get the object from the event and show its content type
#     # bucket = event['Records'][0]['s3']['bucket']['name']
#     # key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
#     try:
#         if event['rawPath'] == '/':
#             s3_response = s3.get_object(Bucket='gfrizzo-api-files', Key='index.html')
#         else:
#             s3_response = s3.get_object(Bucket='gfrizzo-api-files', Key=event['pathParameters']['proxy'])
#
#         print("CONTENT TYPE: " + s3_response['ContentType'])
#
#         if s3_response['ContentType'] == '':
#             response = {
#                 'statusCode': 200,
#                 'headers': { "Content-Type": f"{s3_response['ContentType']}"},
#                 'body': s3_response['Body'].read().decode('utf-8')
#             }
#         else:
#             response = {
#                 'statusCode': 200,
#                 'headers': { "Content-Type": f"{s3_response['ContentType']}"},
#                 'body': base64.b64encode(s3_response['Body'].read()),
#                 'isBase64Encoded': True
#             }
#
#         return response
#     except Exception as e:
#         print(e)
#         #print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
#         raise e

# Get file from S3
# @app.route('/')
# def get_file():
#     request = app.current_request
#     s3 = get_s3_client()
#
#     try:
#         s3_response = s3.get_object(Bucket=s3_bucket, Key='index.html')
#         print("CONTENT TYPE: " + s3_response['ContentType'])
#
#         if s3_response['ContentType'] == '':
#             response = {
#                 'statusCode': 200,
#                 'headers': { "Content-Type": f"{s3_response['ContentType']}"},
#                 'body': s3_response['Body'].read().decode('utf-8')
#             }
#         else:
#             response = {
#                 'statusCode': 200,
#                 'headers': { "Content-Type": f"{s3_response['ContentType']}"},
#                 'body': base64.b64encode(s3_response['Body'].read()),
#                 'isBase64Encoded': True
#             }
#
#         return response
#     except Exception as e:
#         print(e)
#         #print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
#         raise e

# @app.route('/april', methods=['POST'])
# def job_files_webhook():
#     request = app.current_request
#     s3 = get_s3_client()
#
#     json_body = request.json_body
#     return json_body
#
#
#
#
#
# 4:12
# s3_bucket = os.environ['S3_BUCKET_NAME']
# logger.info(f'Using S3 bucket: {s3_bucket}')
#
# _S3 = None
#
#
# def get_s3_client():
#     global _S3
#     if _S3 is None:
#         _S3 = boto3.client('s3')
#     return _S3
# 4:13
# try:
#     s3obj = s3.get_object(Bucket=s3_bucket, Key=yaml_file)
#     yaml_content = s3obj['Body'].read()

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
