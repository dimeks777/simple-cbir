from pymilvus import connections, db, DataType

from milvus_util import _COLLECTION, _DATABASE, _HOST, _PORT, get_client

conn = connections.connect(host=_HOST, port=_PORT)

try:
    db.create_database(_DATABASE)
    print(f"Database '{_DATABASE}' created.")
except Exception as e:
    print(f"Could not create database '{_DATABASE}'. It might already exist. Error: {e}")

print(f"All databases: {db.list_database()}")

client = get_client()

try:

    schema = client.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )

    schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="feature_vector_l2", datatype=DataType.FLOAT_VECTOR, dim=512)
    # schema.add_field(field_name="feature_vector_cosine", datatype=DataType.FLOAT_VECTOR, dim=512)

    index_params = client.prepare_index_params()

    index_params.add_index(
        field_name="feature_vector_l2",
        index_type="IVF_FLAT",
        metric_type="L2",
        index_name="idx_l2",
        params={"nlist": 1024}
    )

    # index_params.add_index(
    #     field_name="feature_vector_cosine",
    #     index_type="IVF_FLAT",
    #     metric_type="COSINE",
    #     index_name="idx_cosine",
    #     params={"nlist": 1024}
    # )

    client.create_collection(_COLLECTION, shards_num=3, schema=schema)
    print(f"Collection '{_COLLECTION}' created.")

    client.create_index(collection_name=_COLLECTION, index_params=index_params)

    indexes = client.list_indexes(_COLLECTION)
    print(f"Indexes: {indexes}")

    for index in indexes:
        idx_info = client.describe_index(_COLLECTION, index)
        print(f"Index info: {idx_info}")


except Exception as e:
    print(f"Could not create collection '{_COLLECTION}'. It might already exist. Error: {e}")

try:
    load_state = client.get_load_state(
        collection_name=_COLLECTION
    )

    print(f"Load state of {_COLLECTION}: {load_state}")

    all_collections = client.list_collections()
    print(f"All collections: {all_collections}")

    client.load_collection(_COLLECTION)
    print(f"Loaded collection: {_COLLECTION}")

    description = client.describe_collection(_COLLECTION)
    print(f"Description of {_COLLECTION}: {description}")
except Exception as e:
    print(f" Error: {e}")
