import boto3
import argparse
import os
from botocore.exceptions import ClientError

def create_test_folders_and_files(bucket_name, endpoint_url=None):
    try:
        # Initialize S3 client with provided endpoint URL
        s3_client = boto3.client('s3', endpoint_url=endpoint_url)

        # Test folder and file structure
        test_data = {
            "test_folder_1": {
                "file1.txt": "This is the content of file1. Contains the word error.",
                "file2.txt": "This is the content of file2. No relevant keywords here."
            },
            "test_folder_2": {
                "file3.txt": "Here is file3 with some random content and error keyword.",
                "file4.txt": "File4 is just some sample text."
            },
            "test_folder_3": {
                "file5.txt": "File5 includes the term error somewhere in the text.",
                "file6.txt": "File6 does not have the search term at all."
            },
            "empty_folder": {}  # An empty folder for testing
        }

        # Iterate over folders and files and upload them to the bucket
        for folder, files in test_data.items():
            for filename, content in files.items():
                key = f"{folder}/{filename}"
                s3_client.put_object(Bucket=bucket_name, Key=key, Body=content)
                print(f"Uploaded {key} to {bucket_name}")

    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print(f"Error: The bucket '{bucket_name}' does not exist.")
        else:
            print(f"Error: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Create test folders and upload files to an S3 bucket.")
    parser.add_argument("bucket_name", help="The name of the S3 bucket where the test files will be uploaded.")
    parser.add_argument("--endpoint-url", default=os.getenv("S3_ENDPOINT_URL"), help="The S3 endpoint URL (e.g., for LocalStack). Default is taken from the S3_ENDPOINT_URL environment variable if not provided.")

    # Parse arguments
    args = parser.parse_args()

    # Validate that the endpoint URL is present
    if not args.endpoint_url:
        print("Error: No endpoint URL provided. Please provide --endpoint-url or set S3_ENDPOINT_URL environment variable.")

    # Call the function to create folders and upload files
    create_test_folders_and_files(args.bucket_name, endpoint_url=args.endpoint_url)