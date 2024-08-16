# S3 Search Script

This script searches for a specific substring in all `.txt` files stored in an S3 bucket. It's designed for use with LocalStack (local S3 emulation) or a real AWS S3 bucket.

## Prerequisites
- Python 3.x
- `boto3` library
- Docker (for LocalStack)

## Usage
1. Clone or download the repository.
2. In the project folder, create a python virtual environment `source myenv/bin/activate`.
3. Install the boto3 library `pip install boto3` (EXPLAIN WHAT IT IS USED FOR)
4. Make sure the bucket to search within is setup and configured. LocalStack or AWS S3 can be used. Instructions for localstack:
   1. Ensure LocalStack is running: `docker run --rm -it -e SERVICES=s3 -p 4566:4566 localstack/localstack`
   2. Create a bucket `aws --endpoint-url=http://localhost:4566 s3 mb s3://BUCKET_NAME`
   3. (optional) create test file/folder structure `python3 create_files_and_folders.py BUCKET_NAME`
   4. Verify file/folder structure `aws --endpoint-url=http://localhost:4566 s3 ls BUCKET_NAME --recursive`
5. Execute the search script in this format: `python s3_search.py <s3_bucket_name> <search_string>`. With the test structure, the word `error` will return results.

## Security considerations
In a production environment, ensure the following advice is followed:
- Do not store credentials within the script but use AWS' default credential handling methods like environment variables or a shared credential file. If this is executed on your local machine, configure this securely with the `aws configure` command.
- Use https instead of http when referencing the bucket endpoint. Without TLS, there's a risk of a man-in-the-middle attack and sensitive information like credentials or sensitive files can be intercepted, changed and/or removed by a malicious actor.