CREATE TABLE IF NOT EXISTS file_mappings
(
    milvus_id BIGINT PRIMARY KEY,
    filename  TEXT NOT NULL
);