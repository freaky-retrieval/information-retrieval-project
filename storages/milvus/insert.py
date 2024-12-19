def insert_records(collection, records):
    """
    Insert records into the Milvus collection.
    Args:
        collection: Milvus collection object.
        records: List of records to insert.
    """
    try:
        collection.insert(records)
        print(f"Inserted {len(records)} records.")
    except Exception as e:
        print(f"Failed to insert records: {str(e)}")
