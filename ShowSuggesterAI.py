import logging
import pickle
import csv
from fuzzywuzzy import process
import numpy as np
from numpy.linalg import norm
from dotenv import load_dotenv
import os
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.DEBUG)
csv_filename = "imdb_tvshows - imdb_tvshows.csv"

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
                    
def get_user_input():
    # Get user input for TV shows
    return input("Which TV shows did you love watching? Separate them by a comma. Make sure to enter more than 1 show: ")

def interpret_input_shows_names(user_input):
    # uses fuzzywuzzy to interpret the user input

    input_show_list_raw = user_input.split(',')

    # Read the CSV file and get the shows names list
    with open(csv_filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        list_of_show_names = [row['Title'] for row in reader]

    most_similar_shows_names = []

    # Find the closest match for each input part
    for requested_show_name in input_show_list_raw:
        
        # Get the most similar show name and its score and add it to the most similar shows list
        top_match, score = process.extractOne(requested_show_name, list_of_show_names)
        if score >= 65:
            most_similar_shows_names.append(top_match)

    return most_similar_shows_names


def confirm_user_input(shows):
    # Confirm user input with the user
    confirmation = input(f"Just to make sure, do you mean {', '.join(shows)}? (y/n): ")
    return confirmation.lower() == 'y'

def cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (norm(vec_a) * norm(vec_b))

def generate_real_tv_show_recommendations(user_input_show_list):
    #TODO:add boost for similar actors, genres, etc


    with open("tv_show_descriptions_embeddings.pkl", 'rb') as file:
        all_show_embeddings = pickle.load(file)
    
    # Get the embeddings for the user input shows
    user_input_show_embeddings = {show: all_show_embeddings[show] for show in user_input_show_list if show in all_show_embeddings}

    # Calculate the average vector for the user input shows
    user_input_vectors = list(user_input_show_embeddings.values())
    average_vector = np.mean(user_input_vectors, axis=0)
    logging.debug(f"Average Vector for User Input Shows: {average_vector}\n")

    # Calculate the similarity scores for all shows except the user input shows
    similarity_scores = {show: cosine_similarity(average_vector, show_embedding) for show, show_embedding in all_show_embeddings.items()}
    for user_picked_show in user_input_show_list:
        similarity_scores.pop(user_picked_show, None)

    # Sort the shows by similarity score
    recommended_shows = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    logging.debug(f"Recommended Shows: {recommended_shows}\n")
    print("Top 5 Recommended Shows:\n")
    for show, score in recommended_shows:
        print(f"{show}: {score * 100:.0f}%")
    
    return recommended_shows
    
def generate_made_up_show(show_list):
        promt = f"""You're a professional Netflix show creator. My favorite shows are: {show_list}.
                Create a show I would love to watch. Please use an actor from the list of my favorite shows and explain the role and name you gave them.
                They don't have to be the main character, so you can mention them by the way in the description.
                In your answer, do not mention the shows I provided. Use this format:
                Name: Name of the show
                Description: Short description of the show (100 words max)"""
        messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":f"{promt}"}
    ]
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
        generated_show = response.choices[0].message.content
        show_name = generated_show.split("Name: ")[1].split("Description: ")[0]
        show_description = generated_show.split("Description: ")[1]
        
        return show_name, show_description


def generate_ad_for_a_shows(show_name, show_description):
    #TODO: Generate an ad for a show using dale-e
    logging.debug("Generating an ad image for a show is pending implementation.\n")
    pass

def generate_made_up_shows_and_ads(input_shows, recommended_real_tv_shows):
    
    show1_name, show1_description = generate_made_up_show(input_shows)
    show2_name, show2_description = generate_made_up_show(recommended_real_tv_shows)

    print(
        f"I have also created just for you two shows which I think you would love.\n"
        f"Show #1 is based on the fact that you loved the input shows that you gave me.\n"
        f"Its name is {show1_name} and it is about {show1_description}.\n"
        f"Show #2 is based on the shows that I recommended for you.\n"
        f"Its name is {show2_name} and it is about {show2_description}.\n"
        f"Here are also the 2 TV show ads. Hope you like them!"
    )

    generate_ad_for_a_shows(show1_name, show1_description)
    generate_ad_for_a_shows(show2_name, show2_description)
    return {show1_name: show1_description, show2_name: show2_description}


def main():
    # Main function to run the TV show recommendation program
    while True:
        user_input = get_user_input()
        # Interprets user input into shows from the list
        interpreted_shows = interpret_input_shows_names(user_input)

        if confirm_user_input(interpreted_shows):
            # Generate recommendations and custom shows
            recommendations = generate_real_tv_show_recommendations(interpreted_shows)

            custom_shows = generate_made_up_shows_and_ads(interpreted_shows, recommendations)
            break
        else:
            print("Sorry about that. Let's try again. Please make sure to write the names of the TV shows correctly.")

if __name__ == "__main__":
    main()
