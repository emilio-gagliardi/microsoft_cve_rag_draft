from services.embedding_service import generate_embeddings
from datetime import datetime, timezone
import uuid


# Simulated database for demonstration purposes
class VectorDatabase:
    def __init__(self):
        self._database = {}

    def add_record(self, data):
        try:
            client = self._client()
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now(timezone.utc)
            data["updated_at"] = datetime.now(timezone.utc)
            data["embeddings"] = generate_embeddings(data)
            response = client.add_record(data)
            return response
        except Exception as e:
            raise RuntimeError(f"Error adding record: {e}")

    def update_record(self, id, data):
        try:
            client = self._client()
            if id in self._database:
                data["updated_at"] = datetime.now(timezone.utc)
                data["embeddings"] = generate_embeddings(data)
                response = client.update_record(id, data)
                return response
            else:
                raise ValueError("Record not found")
        except Exception as e:
            raise RuntimeError(f"Error updating record: {e}")

    def delete_record(self, id):
        try:
            client = self._client()
            if id in self._database:
                response = client.delete_record(id)
                return response
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
            response = client.query_records(query, page, page_size)
            return response
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
                data["embeddings"] = generate_embeddings(data)
                response = client.add_record(data)
                new_records.append(response)
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
                    data["embeddings"] = generate_embeddings(data)
                    response = client.update_record(id, data)
                    updated_records.append(response)
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
                    response = client.delete_record(id)
                else:
                    raise ValueError(f"Record with ID {id} not found")
            return {"message": f"{len(ids)} records deleted"}
        except Exception as e:
            raise RuntimeError(f"Error deleting records: {e}")

    def _client(self):
        # This would return the actual database client in a real-world scenario
        return "DatabaseClient"
