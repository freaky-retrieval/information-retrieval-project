def insert_records(client, collection_name, records):
    """
    Insert records into the Milvus Lite collection.
    Args:
        client: Milvus Lite client object.
        collection_name: Name of the collection.
        records: List of records to insert.
    """
    try:
        res = client.insert(collection_name=collection_name, data=records)
        print(f"Inserted {len(records)} records.")
        return res
    except Exception as e:
        print(f"Failed to insert records: {str(e)}")