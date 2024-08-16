# S3 Search Script

This script searches for a specific substring in all `.txt` files stored in an S3 bucket. It is designed for use with LocalStack (local S3 emulation) or a real AWS S3 bucket.

## Prerequisites
- **Python 3.x**: Ensure you have Python installed.
- **`boto3` library**: A Python SDK for AWS services. It is used to interact with S3 buckets in this script.
- **Docker (for LocalStack)**: Required if using LocalStack to emulate S3 locally.

## Setup
1. Clone or download the repository.
2. In the project folder, create a Python virtual environment:
   - `python3 -m venv myenv`
   - `source myenv/bin/activate`
3. Install the required Python libraries, including `boto3`:
   - `pip install boto3`
4. Ensure that the S3 bucket to search within is set up. You can use either LocalStack (for local testing) or AWS S3. Below are the instructions for setting up LocalStack:

### LocalStack Setup
1. Ensure LocalStack is running:
   - `docker run --rm -it -e SERVICES=s3 -p 4566:4566 localstack/localstack`
2. Create an S3 bucket in LocalStack:
   - `aws --endpoint-url=http://localhost:4566 s3 mb s3://BUCKET_NAME`
3. (Optional) Create a test file and folder structure in the bucket:
   - `python3 create_files_and_folders.py BUCKET_NAME --endpoint-url=http://localhost:4566`
4. Verify the file and folder structure:
   - `aws --endpoint-url=http://localhost:4566 s3 ls BUCKET_NAME --recursive`

## Usage

To execute the script, use the following command:

- `python s3_search.py <s3_bucket_name> <search_string> [--endpoint-url <endpoint_url>]`

- `<s3_bucket_name>`: The name of the S3 bucket to search in.
- `<search_string>`: The substring you want to search for in the `.txt` files.
- `[--endpoint-url <endpoint_url>]`: (Optional) The S3 endpoint URL, such as `http://localhost:4566` for LocalStack. If not provided, it will default to the `S3_ENDPOINT_URL` environment variable.

### Example

For LocalStack:
- `python s3_search.py limehome-bucket "error" --endpoint-url=http://localhost:4566`

For AWS (if the `S3_ENDPOINT_URL` environment variable is set):
- `python s3_search.py limehome-bucket "error"`

### Notes
- The `create_files_and_folders.py` script is available to create a test file structure inside an S3 bucket.
- The script can search any `.txt` file within the bucket and return a list of files containing the specified substring.

## Security Considerations

- **Avoid hardcoding credentials**: Ensure that credentials are securely managed using AWS's default credential mechanisms (e.g., environment variables, AWS config files, or IAM roles).
- **Use HTTPS endpoints**: Always use HTTPS instead of HTTP for communication with AWS services to protect data in transit from man-in-the-middle attacks. This applies to both LocalStack and AWS in production environments.