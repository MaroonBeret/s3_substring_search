import boto3
import argparse
import os
import time

def search_files_in_s3(s3_bucket_name, substring, endpoint_url=None):
    # Create an S3 client, using the provided endpoint URL (if any)
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)
    
    matching_files = []

    # List objects in the bucket
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
    except s3_client.exceptions.NoSuchBucket:
        print(f"Error: The bucket '{s3_bucket_name}' does not exist.")
        return matching_files

    if 'Contents' not in response:
        print("No files found in the bucket.")
        return matching_files

    # Check all found .txt files for substring match
    for obj in response['Contents']:
        file_key = obj['Key']
        if file_key.endswith('.txt'):
            s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=file_key)
            content = s3_object['Body'].read().decode('utf-8')
            if substring in content:
                matching_files.append(file_key)
    
    return matching_files

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Search for a substring in S3 text files.")
    parser.add_argument("s3_bucket_name", help="The name of the S3 bucket to search in.")
    parser.add_argument("substring", help="The substring to search for in the text files.")
    parser.add_argument("--endpoint-url", default=os.getenv("S3_ENDPOINT_URL"), help="The S3 endpoint URL (e.g., for LocalStack). Default is taken from the S3_ENDPOINT_URL environment variable if not provided.")

    # Parse arguments
    args = parser.parse_args()

    # Validate that the endpoint URL is present
    if not args.endpoint_url:
        print("Error: No endpoint URL provided. Please provide --endpoint-url or set S3_ENDPOINT_URL environment variable.")
        exit(1)

    # Start timer
    start_time = time.time()

    # Call the search function
    matching_files = search_files_in_s3(args.s3_bucket_name, args.substring, endpoint_url=args.endpoint_url)

    # Stop timer
    end_time = time.time()

    # Output the results, if any
    if matching_files:
        print(f"Files containing '{args.substring}':")
        for filename in matching_files:
            print(f"- {filename}")
    else:
        print(f"No files found containing '{args.substring}'.")

    # Calculate the time taken
    total_time = end_time - start_time
    print(f"Time taken to execute the script: {total_time:.2f} seconds")