import os
import shutil

from custom_features import extract_features
from milvus_util import get_client, _COLLECTION
from postgres_util import db_handler
from storage_util import storage_handler


# def build_database(image_folder):
#     database = []
#     for filename in os.listdir(image_folder):
#         if filename.endswith(('.png', '.jpg', '.jpeg')):
#             features = extract_features(os.path.join(image_folder, filename))
#             # print((filename, features))
#             database.append((filename, features))
#     return database


#     try:
#         pg_conn = get_postgres_connection()
#         cursor = pg_conn.cursor()
#         cursor.execute("YOUR SQL QUERY HERE")
#         pg_conn.commit()
#
#     except (Exception, psycopg2.Error) as error:
#         # Rolling back the transaction in case of error
#         pg_conn.rollback()
#
#     finally:
#         # Closing the cursor and connection
#         if pg_conn:
#             cursor.close()
#              pg_conn.close()

# def build_milvus_database(image_folder):
#     count = 0
#     for filename in os.listdir(image_folder):
#         if filename.endswith(('.png', '.jpg', '.jpeg')):
#             features = extract_features(os.path.join(image_folder, filename))
#             inserted_count = save_to_db(filename, features)
#             count += inserted_count
#     return count

def build_milvus_database(image_folder):
    count = 0
    for dirpath, dirnames, filenames in os.walk(image_folder):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(dirpath, filename)
                features = extract_features(full_path)
                inserted_count = save_to_db(filename, features)
                count += inserted_count
    return count


def copy_images_to_flat_directory(source_folder, destination_folder):
    image_extensions = ('.png', '.jpg', '.jpeg')
    copied_count = 0


    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for dirpath, _, filenames in os.walk(source_folder):
        for filename in filenames:
            if filename.lower().endswith(image_extensions):
                source_path = os.path.join(dirpath, filename)
                destination_path = os.path.join(destination_folder, filename)

                if os.path.exists(destination_path):
                    base, extension = os.path.splitext(filename)
                    i = 1
                    new_filename = f"{base}_{i}{extension}"
                    destination_path = os.path.join(destination_folder, new_filename)
                    while os.path.exists(destination_path):
                        i += 1
                        new_filename = f"{base}_{i}{extension}"
                        destination_path = os.path.join(destination_folder, new_filename)

                shutil.copy(source_path, destination_path)
                copied_count += 1

    print(f"Copied {copied_count} images to {destination_folder}")
    return copied_count


def save_to_db(filename, features):
    milvus_client = get_client()
    data = {"feature_vector_l2": features, "feature_vector_cosine": features}
    ret = milvus_client.insert(_COLLECTION, data=data)
    ret_id = ret['ids'][0]
    db_handler.insert_mapping(ret_id, storage_handler.build_filename(filename))
    return ret['insert_count']


# IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "/all_images")
# print(IMAGE_FOLDER)
# copy_images_to_flat_directory("animals", IMAGE_FOLDER)
# rows = build_milvus_database(IMAGE_FOLDER)
# print(rows)
