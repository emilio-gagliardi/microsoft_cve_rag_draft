# python -m pip install "pymongo[srv]"==3.11
# from pymongo.mongo_client import MongoClient


# from app_utils import get
# client = MongoClient(uri)
# Send a ping to confirm a successful connection
# try:
#     client.admin.command("ping")
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
from datetime import datetime, timezone
import uuid


class DocumentsDatabase:
    def __init__(self):
        self._database = {}

    def add_record(self, data):
        try:
            client = self._client()
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now(timezone.utc)
            data["updated_at"] = datetime.now(timezone.utc)
            self._database[data["id"]] = data
            return data
        except Exception as e:
            raise RuntimeError(f"Error adding record: {e}")

    def update_record(self, id, data):
        try:
            client = self._client()
            if id in self._database:
                data["updated_at"] = datetime.now(timezone.utc)
                self._database[id].update(data)
                return self._database[id]
            else:
                raise ValueError("Record not found")
        except Exception as e:
            raise RuntimeError(f"Error updating record: {e}")

    def delete_record(self, id):
        try:
            client = self._client()
            if id in self._database:
                del self._database[id]
            else:
                raise ValueError("Record not found")
        except Exception as e:
            raise RuntimeError(f"Error deleting record: {e}")

    def query_records(self, query, page=1, page_size=10):
        try:
            client = self._client()
            filtered_records = [
                record
                for record in self._database.values()
                if all(item in record.items() for item in query.items())
            ]
            total_count = len(filtered_records)
            start = (page - 1) * page_size
            end = start + page_size
            paginated_records = filtered_records[start:end]
            return paginated_records, total_count
        except Exception as e:
            raise RuntimeError(f"Error querying records: {e}")

    def bulk_add_records(self, data_list):
        try:
            client = self._client()
            new_records = []
            for data in data_list:
                data["id"] = str(uuid.uuid4())
                data["created_at"] = datetime.now(timezone.utc)
                data["updated_at"] = datetime.now(timezone.utc)
                self._database[data["id"]] = data
                new_records.append(data)
            return new_records
        except Exception as e:
            raise RuntimeError(f"Error adding records: {e}")

    def bulk_update_records(self, data_list):
        try:
            client = self._client()
            updated_records = []
            for data in data_list:
                id = data["id"]
                if id in self._database:
                    data["updated_at"] = datetime.now(timezone.utc)
                    self._database[id].update(data)
                    updated_records.append(self._database[id])
                else:
                    raise ValueError(f"Record with ID {id} not found")
            return updated_records
        except Exception as e:
            raise RuntimeError(f"Error updating records: {e}")

    def bulk_delete_records(self, ids):
        try:
            client = self._client()
            for id in ids:
                if id in self._database:
                    del self._database[id]
                else:
                    raise ValueError(f"Record with ID {id} not found")
        except Exception as e:
            raise RuntimeError(f"Error deleting records: {e}")

    def _client(self):
        # This would return the actual database client in a real-world scenario
        return "DatabaseClient"
