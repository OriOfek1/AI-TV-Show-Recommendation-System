import os
import pickle
import csv
from openai import OpenAI
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Given a string input, generates an embedding vector using the OpenAI API
def generate_embedding(description):
    response = client.embeddings.create(
        input=description,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Function to process the CSV file and generate embeddings
def generate_embeddings_dict_from_csv_file(csv_filename):
    embeddings_dict = {}

    with open(csv_filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['Title']
            description = row['Description']
            embedding = generate_embedding(description)
            embeddings_dict[title] = embedding

    return embeddings_dict

#process the CSV file and generate embeddings dictionary
def generate_embeddings_dict_from_csv_file(csv_filename):
    embeddings_dict = {}

    with open(csv_filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['Title']
            description = row['Description']
            embedding = generate_embedding(description)
            embeddings_dict[title] = embedding

    return embeddings_dict

# Save the embeddings dictionary to a pickle file
def save_embeddings_dict_to_pickle(embeddings_dict, filename):
    with open(filename, 'wb') as file:
        pickle.dump(embeddings_dict, file)


def main():
    csv_ShowsFile = "imdb_tvshows - imdb_tvshows.csv"
    embeddings_pickle_filename = 'tv_show_descriptions_embeddings.pkl'
    embeddings_dict = generate_embeddings_dict_from_csv_file(csv_ShowsFile)
    save_embeddings_dict_to_pickle(embeddings_dict, embeddings_pickle_filename)
    
if __name__ == "__main__":
    main()