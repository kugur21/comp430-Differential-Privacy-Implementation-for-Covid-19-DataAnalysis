def initialize_database(db_connection):
    """
    Initializes the database by creating necessary tables if they don't exist.
    :param db_connection: The database connection instance.
    """
    from database.schema import CREATE_TABLES_QUERIES

    for table_name, query in CREATE_TABLES_QUERIES.items():
        try:
            db_connection.execute_query(query)
            print(f"Table {table_name} created or already exists.")
        except Exception as e:
            print(f"Error creating table {table_name}: {e}")
