import psycopg

def clear_tables(pg_conn: psycopg.Connection,
                 TABLES: list[str]) -> None:
    print("Clearing all tables in PostgreSQL...")
    with pg_conn.cursor() as cursor:
        for table in TABLES:
            cursor.execute(f"TRUNCATE TABLE content.{table} CASCADE")
            cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM information_schema.sequences "
                "WHERE sequence_schema = 'content' AND sequence_name = %s)",
                (f"{table}_id_seq",)
            )
            result = cursor.fetchone()
            print(result)
            if result.get('exists') == True and result[0]:
                cursor.execute(f"ALTER SEQUENCE content.{table}_id_seq RESTART WITH 1")
            else:
                print(f"Warning: Sequence 'content.{table}_id_seq' does not exist.")
    print("All tables cleared successfully")