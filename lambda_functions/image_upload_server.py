import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    email_content = ''
    
    # Retrieve bucket name and file_key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    # Labling the image using Rekognition
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.detect_labels(Image= {"S3Object":{"Bucket":bucket_name, "Name":file_name}})
    s3.put_object(Bucket='analyzed-widget-images-bucket', Key="d.txt",Body=str(response))
    
    # Now, sending notifications to quality control group members via SNS
    sns_client = boto3.client('sns')
    response_sns= sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:090121384790:WidgetInspectionReport',
        Message=str(response),
        Subject='Widget Inspection Report : '+str(file_name))
    
