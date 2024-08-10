from custom_features import compare_features, extract_features
from database import get_client, save_to_db
from postgres_util import db_handler
from storage_util import storage_handler

_COLLECTION = "images"


def query_image(query_image_path, database):
    query_features = extract_features(query_image_path)
    results = []
    for entry in database:
        filename, db_features = entry
        distance = compare_features(query_features, db_features)
        results.append((filename, distance))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def search_image_milvus(query_image_path):
    client = get_client()
    query_features = extract_features(query_image_path)

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    res = client.search(_COLLECTION, data=[query_features.tolist()], anns_field="feature_vector_l2",
                        search_params=search_params, limit=12)

    # search_params2 = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    # res2 = client.search(_COLLECTION, data=[query_features.tolist()], anns_field="feature_vector_cosine",
    #                 search_params=search_params2, limit=50)
    #
    # common_res = intersect_results(res, res2)
    duplicate = find_duplicate(client, query_features)
    if duplicate is None:
        storage_handler.move_file_to_permanent_storage(query_image_path, extract_filename(query_image_path))
        save_to_db(extract_filename(query_image_path), query_features)
    else:
        print(f"Duplicate found: {duplicate}")
        storage_handler.delete_temporary_file(query_image_path)

    # print(f"L2 ids: {[hit['id'] for hit in res[0]]}")
    # print(f"Cosine ids: {[hit['id'] for hit in res2[0]]}")
    ids = [hit['id'] for hit in res[0]]
    return ids


def intersect_results(results_l2, results_cosine):
    set_l2 = set([result['id'] for result in results_l2[0]])
    set_cosine = set([result['id'] for result in results_cosine[0]])

    common_ids = set_l2.intersection(set_cosine)
    common_results = [result for result in results_l2[0] if result['id'] in common_ids]

    # Sort by combined scores or other criteria
    # common_results.sort(key=lambda x: x.distance)  # Example: sort by L2 distance
    return common_results


def find_duplicate(client, features, threshold=0.01):
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = client.search(_COLLECTION, data=[features.tolist()], anns_field="feature_vector_l2",
                            search_params=search_params, limit=1)
    if len(results) > 0:
        if results[0][0]['distance'] < threshold:
            return results[0][0]['id']
    return None


def get_similar_images(input_image):
    similar_images_ids = search_image_milvus(input_image)
    print(f"Input file: {input_image}")
    print(f"Found ids: {similar_images_ids}")
    similar_images = []
    for image_id in similar_images_ids:
        f_name = db_handler.get_filename(image_id)
        print(f"Filename for {image_id}: {f_name}")
        similar_images.append(storage_handler.build_url_for_ui(f_name))
    return similar_images


def extract_filename(full_path):
    import os
    filename = os.path.basename(full_path)
    return filename

# dataset_folder = "./all_images"
# database = build_database(dataset_folder)
# result = query_image("./query_images/histo.jpg", database)
# print(result)
# display_similar_images(result, dataset_folder)


# query_res = get_similar_images("./query_images/histo.jpg")
# print(query_res)
