from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from services.embedding_service import generate_embeddings


def run_etl():
    data = extract_data()
    transformed_data = transform_data(data)
    embeddings = generate_embeddings(transformed_data)
    load_data(embeddings)


if __name__ == "__main__":
    run_etl()
