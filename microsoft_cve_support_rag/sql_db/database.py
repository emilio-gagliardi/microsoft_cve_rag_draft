import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import logging
from datetime import datetime, timezone
from app_utils import get_sql_db_credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLDatabase:
    def __init__(self):
        self._db_config = get_sql_db_credentials()
        self._pool = psycopg2.pool.SimpleConnectionPool(1, 10, **self._db_config)
        if self._pool:
            logger.info("Connection pool created successfully")

    def add_record(self, data):
        try:
            client = self._client()
            cursor = client.cursor(cursor_factory=RealDictCursor)
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now(timezone.utc)
            data["updated_at"] = datetime.now(timezone.utc)
            query = """
                INSERT INTO your_table (id, field1, field2, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["id"],
                    data["field1"],
                    data["field2"],
                    data["created_at"],
                    data["updated_at"],
                ),
            )
            client.commit()
            cursor.close()
            return data
        except Exception as e:
            client.rollback()
            logger.error(f"Error adding record: {e}")
            raise RuntimeError(f"Error adding record: {e}")
        finally:
            self._client_close(client)

    def update_record(self, id, data):
        try:
            client = self._client()
            cursor = client.cursor(cursor_factory=RealDictCursor)
            data["updated_at"] = datetime.now(timezone.utc)
            query = """
                UPDATE your_table
                SET field1 = %s, field2 = %s, updated_at = %s
                WHERE id = %s
            """
            cursor.execute(
                query, (data["field1"], data["field2"], data["updated_at"], id)
            )
            client.commit()
            cursor.close()
            return data
        except Exception as e:
            client.rollback()
            logger.error(f"Error updating record: {e}")
            raise RuntimeError(f"Error updating record: {e}")
        finally:
            self._client_close(client)

    def delete_record(self, id):
        try:
            client = self._client()
            cursor = client.cursor(cursor_factory=RealDictCursor)
            query = """
                DELETE FROM your_table WHERE id = %s
            """
            cursor.execute(query, (id,))
            client.commit()
            cursor.close()
            return {"message": "Record deleted"}
        except Exception as e:
            client.rollback()
            logger.error(f"Error deleting record: {e}")
            raise RuntimeError(f"Error deleting record: {e}")
        finally:
            self._client_close(client)

    def query_records(self, query, page=1, page_size=10):
        try:
            client = self._client()
            cursor = client.cursor(cursor_factory=RealDictCursor)
            offset = (page - 1) * page_size
            sql_query = """
                SELECT * FROM your_table
                WHERE (some_field = %s)
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql_query, (query["some_field"], page_size, offset))
            records = cursor.fetchall()
            total_count = cursor.rowcount
            cursor.close()
            return {"results": records, "total_count": total_count}
        except Exception as e:
            logger.error(f"Error querying records: {e}")
            raise RuntimeError(f"Error querying records: {e}")
        finally:
            self._client_close(client)

    def _client(self):
        try:
            client = self._pool.getconn()
            if client:
                logger.info("Successfully received connection from connection pool")
            return client
        except Exception as e:
            logger.error(f"Error getting connection: {e}")
            raise RuntimeError(f"Error getting connection: {e}")

    def _client_close(self, client):
        try:
            self._pool.putconn(client)
            logger.info("Returned connection to pool")
        except Exception as e:
            logger.error(f"Error returning connection to pool: {e}")
            raise RuntimeError(f"Error returning connection to pool: {e}")
