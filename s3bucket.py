import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

import urllib.request
import urllib.parse


def makeS3Cred():
    ACCESS_KEY_ID = 'AKIAJRZ5MXQ5RVDBYKYA'
    ACCESS_SECRET_KEY = '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'

    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    return s3


def list_bucket_objects():
    S3Cred = makeS3Cred()
    try:
        response = S3Cred.list_objects_v2(Bucket='aardvarc-test-bucket')
    except ClientError as e:
        return None

    if response['KeyCount'] > 0:
        objects = response['Contents']
        if objects is not None:
            # List the object names
            print('Objects')
            for obj in objects:
                print(f'  {obj["Key"]}')
        else:
            # Didn't get any keys
            print('No objects')


def put(ClassCode):
    ACCESS_KEY_ID = 'AKIAJRZ5MXQ5RVDBYKYA'
    ACCESS_SECRET_KEY = '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'
    S3_BUCKET_NAME = 'aardvarc-test-bucket'

    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    S3Cred = s3.Bucket(S3_BUCKET_NAME)
    link_to_html = urllib.parse.quote(
        'http://127.0.0.1/demo/generate/tasyllabus/html/' + ClassCode)  # django template
    urllib.request.urlretrieve('http://localhost:3000/pdf/url/?url=' + link_to_html, ClassCode + '.pdf')  # NodeJS
    with open(ClassCode + '.pdf', 'rb') as pdf:
        response = pdf.read()
        result = S3Cred.put_object(
            Key='Demo\\University-of-Syllabus-Composition\\Documents\\Syllabi\\Summer-2019\\Generated\\test-SOP-101_12345.pdf',
            Body=response, ACL='public-read')
        print(result)


def put_object():
    dest_bucket_name = 'aardvarc-test-bucket'
    dest_object_name = 'test.txt'
    src_data = 'test.txt'

    # Construct Body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
            # possible FileNotFoundError/IOError exception
        except Exception as e:
            return False
    else:
        print('Type of ' + str(type(src_data)) + ' for the argument \'src_data\' is not supported.')
        return False

    # Put the object

    ACCESS_KEY_ID = 'AKIAJRZ5MXQ5RVDBYKYA'
    ACCESS_SECRET_KEY = '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'

    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    try:
        s3.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data, ACL='public-read')
    except ClientError as e:
        return False
    finally:
        if isinstance(src_data, str):
            object_data.close()
    return True

def get_object_data():
    dest_bucket_name = 'aardvarc-test-bucket'
    dest_object_name = 'Demo/University-of-Syllabus-Composition/Documents/Syllabi/Summer-2019/Generated/test-SOP-101_12345.pdf'

    ACCESS_KEY_ID = 'AKIAJRZ5MXQ5RVDBYKYA'
    ACCESS_SECRET_KEY = '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'

    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    result = s3.get_object(Bucket=dest_bucket_name, Key=dest_object_name)
    print(result)


def main():
    # list_bucket_objects()
    # put('BFStXM0Fuu7Z9D6SOJAr')
    # put_object()
    get_object_data()

if __name__ == '__main__':
    main()
