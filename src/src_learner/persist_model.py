import json
import boto3
from botocore.exceptions import ClientError

def persist_model(filename):
    """

    @param filename: name of the .pt file that should be saved (e.g. python3_base_model.pt)
    @return: ok if file was saved, error otherwise
    """
    # credentials are saved in a separate file so that they are not shared by accident
    with open('credentials.txt') as f:
        data = f.read()
    credentials = json.loads(data)

    AWS_ACCESS_KEY_ID = credentials['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = credentials['AWS_SECRET_ACCESS_KEY']
    bucket_name = 'bucket-e979ig'

    # create s3 client with credentials
    s3_client = boto3.client('s3', region_name='eu-central-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        response = s3_client.upload_file(filename, bucket_name, filename)
    except ClientError as e:
        return {'ok': -1, 'error_message':e}
    except FileNotFoundError as e:
        print(e)
        return {'ok': -1, 'error_message':e}
    return {'ok': 1}

