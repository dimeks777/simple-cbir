import os
import shutil

from dotenv import load_dotenv

load_dotenv()
STORAGE_TYPE = os.getenv('STORAGE')
BASE_SERVER_URL = os.getenv('BASE_SERVER_URL')


# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")


class StorageHandler:
    # def __init__(self):

    # if _STORAGE == "s3":
    #     self.s3_client = boto3.client(
    #         's3',
    #         aws_access_key_id=AWS_ACCESS_KEY_ID,
    #         aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    #     )

    def build_filename(self, original_filename):
        # Example: builds a URI based on storage type
        if STORAGE_TYPE == "local":
            return f"local:///{original_filename}"
        # elif STORAGE_TYPE == "s3":
        #     return f"s3://{AWS_S3_BUCKET_NAME}/{original_filename}"
        else:
            raise ValueError("Unsupported storage type")

    # def retrieve_file(self, filename_uri):
    # if filename_uri.startswith('local:///'):
    #     file_path = filename_uri.replace('local:///', '')
    #     with open(file_path, 'rb') as file:
    #         return file
    # # elif filename_uri.startswith('s3://'):
    # #     bucket_name, object_path = filename_uri.replace('s3://', '').split('/', 1)
    # #     response = self.s3_client.get_object(Bucket=bucket_name, Key=object_path)
    # #     return response['Body'].read()
    # else:
    #     raise ValueError("Unsupported storage type or URI format.")

    def build_url_for_ui(self, filename_uri):
        if filename_uri.startswith('local:///'):
            # Assuming '/images/' is the route in your backend that serves local images
            relative_path = filename_uri.replace('local:///', '')
            return f'{BASE_SERVER_URL}/images/{relative_path}'
        # elif filename_uri.startswith('s3://'):
        #     # Generate a signed URL for S3 objects (if using boto3)
        #     object_path = filename_uri.replace(f's3://{AWS_S3_BUCKET_NAME}/', '')
        #     return self.s3_client.generate_presigned_url('get_object',
        #                                                  Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': object_path},
        #                                                  ExpiresIn=3600) # URL expires in 1 hour
        else:
            raise ValueError("Unsupported storage type")

    # def save_file(self, file, temp=False):
    #     if STORAGE_TYPE == "local":
    #         # folder = None
    #         if temp is True:
    #             folder = os.getenv('TMP_IMAGE_FOLDER')
    #         else:
    #             folder = os.getenv('IMAGE_FOLDER')
    #         # Ensure the directory exists
    #         file_path = f"{folder}/{file.filename}"
    #         os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #         with open(file_path, "wb") as f:
    #             f.write(file.file.read())  # Assuming 'file' is a FastAPI UploadFile
    #
    #         print(f'File path to save: {file_path}')
    #         return file_path
    #     # elif STORAGE_TYPE == "s3":
    #     #     self.s3_client.upload_fileobj(
    #     #         file.file,  # Assuming 'file' is a FastAPI UploadFile
    #     #         AWS_S3_BUCKET_NAME,
    #     #         file_path
    #     #     )
    #     else:
    #         raise ValueError("Unsupported storage type")

    def move_file_to_permanent_storage(self, temp_filepath, new_filename):

        if STORAGE_TYPE == "local":

            folder = os.getenv('IMAGE_FOLDER')
            permanent_filepath = os.path.join(folder, new_filename)
            shutil.move(temp_filepath, permanent_filepath)
            print(f'File moved to: {permanent_filepath}')
            return permanent_filepath

        else:
            raise ValueError("Unsupported storage type")

    def save_temporary_file(self, file):
        folder = os.getenv('TMP_IMAGE_FOLDER')
        file_path = f"{folder}/{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        print(f'File path to save: {file_path}')
        return file_path

    def delete_temporary_file(self, temp_filepath):
        # Delete a temporary file
        os.remove(temp_filepath)


# import boto3
# bucket_name, path = uri.replace('s3://', '').split('/', 1)
# s3 = boto3.client('s3')
# # Implement logic to retrieve file from S3
# return s3.get_object(Bucket=bucket_name, Key=path)['Body'].read()

storage_handler = StorageHandler()

# file_content = storage_handler.get_file('s3://bucket-name/images/filename.jpg')
