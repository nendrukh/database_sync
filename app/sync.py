import pymysql
from typing import List, Dict, Any

from config import (
    SOURCE_DB,
    SOURCE_DB_PASS,
    SOURCE_DB_USER,
    SOURCE_DB_HOST,
    TARGET_DB,
    TARGET_DB_PASS,
    TARGET_DB_USER,
    TARGET_DB_HOST
)


class DbCorrector:
    source_conn = pymysql.connect(host=SOURCE_DB_HOST, user=SOURCE_DB_USER, password=SOURCE_DB_PASS, database=SOURCE_DB)
    target_conn = pymysql.connect(host=TARGET_DB_HOST, user=TARGET_DB_USER, password=TARGET_DB_PASS, database=TARGET_DB)

    @classmethod
    def _get_tables(cls, conn) -> List[str]:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def _get_table_schema(conn, table: str) -> Dict[str, Dict[str, Any]]:
        with conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table}")
            return {row[0]: row[1:] for row in cursor.fetchall()}

    @classmethod
    def sync_structure(cls):
        source_tables = cls._get_tables(cls.source_conn)
        target_tables = cls._get_tables(cls.target_conn)

        for table in source_tables:
            if table not in target_tables:
                cls._create_table(table)

        for table in source_tables:
            if table in target_tables:
                cls._sync_table_schema(table)

    @classmethod
    def _create_table(cls, table: str):
        with cls.source_conn.cursor() as source_cursor, cls.target_conn.cursor() as target_cursor:
            source_cursor.execute(f"SHOW CREATE TABLE {table}")
            create_table_query = source_cursor.fetchone()[1]
            target_cursor.execute(create_table_query)
            cls.target_conn.commit()

    @classmethod
    def _sync_table_schema(cls, table: str):
        source_schema = cls._get_table_schema(cls.source_conn, table)
        target_schema = cls._get_table_schema(cls.target_conn, table)

        with cls.target_conn.cursor() as cursor:
            for column, attributes in source_schema.items():
                if column not in target_schema:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {attributes[0]}")
            cls.target_conn.commit()

    @classmethod
    def sync_data(cls):
        source_tables = cls._get_tables(cls.source_conn)

        for table in source_tables:
            cls._sync_table_data(table)

    @classmethod
    def _sync_table_data(cls, table: str):
        with cls.source_conn.cursor() as source_cursor:
            source_cursor.execute(f"SELECT * FROM {table}")
            source_rows = source_cursor.fetchall()

            source_cursor.execute(f"SHOW COLUMNS FROM {table}")
            columns = [row[0] for row in source_cursor.fetchall()]

        with cls.target_conn.cursor() as target_cursor:
            for row in source_rows:
                placeholders = ", ".join(["%s"] * len(row))
                update_clause = ", ".join([f"{col}=VALUES({col})" for col in columns])
                sql = f"""INSERT INTO {table} ({', '.join(columns)}) 
                VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {update_clause}"""
                target_cursor.execute(sql, row)

            cls.target_conn.commit()

    @classmethod
    def close(cls):
        cls.source_conn.close()
        cls.target_conn.close()


if __name__ == "__main__":
    print("python_sync started")
    try:
        DbCorrector.sync_structure()
        DbCorrector.sync_data()
    finally:
        DbCorrector.close()
    print("python_sync completed")
