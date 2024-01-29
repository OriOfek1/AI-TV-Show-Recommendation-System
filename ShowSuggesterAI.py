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
logging.basicConfig(level=logging.WARNING)
csv_filename = "imdb_tvshows - imdb_tvshows.csv"

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_user_input():
    # Get user input for TV shows
    return input(
        "Which TV shows did you love watching? Separate them by a comma. Make sure to enter more than 1 show: ")


def interpret_input_shows_names(user_input):
    # uses fuzzywuzzy to interpret the user input

    input_show_list_raw = user_input.split(',')

    # list of the names of all the shows in the file
    list_of_show_names = get_list_of_shows()
    most_similar_shows_names = []

    # Find the closest match for each input part
    for requested_show_name in input_show_list_raw:

        # Get the most similar show name and its score and add it to the most similar shows list
        top_match, score = process.extractOne(requested_show_name, list_of_show_names)
        if score >= 65:
            most_similar_shows_names.append(top_match)

    return most_similar_shows_names


def get_list_of_shows():
    # Read the CSV file and get the shows names list
    with open(csv_filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        list_of_show_names = [row['Title'] for row in reader]

    return list_of_show_names


def get_list_of_items_for_shows(list_of_shows, column_name):
    # Read the CSV file and get the list of actors for the specified shows
    with open(csv_filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        items_for_shows = [row[column_name].split(',') for row in reader if row['Title'] in list_of_shows]

    # Flatten the list of lists and convert to a set to remove duplicates, then back to list
    return list(set(item.strip() for sublist in items_for_shows for item in sublist))


def confirm_user_input(shows):
    # Confirm user input with the user
    confirmation = input(f"Just to make sure, do you mean {', '.join(shows)}? (y/n): \n")
    return confirmation.lower() == 'y'


def cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (norm(vec_a) * norm(vec_b))


def generate_real_tv_show_recommendations(user_input_show_list):
    with open("tv_show_descriptions_embeddings.pkl", 'rb') as file:
        all_show_embeddings = pickle.load(file)

    # Get the embeddings for the user input shows
    user_input_show_embeddings = {show: all_show_embeddings[show] for show in user_input_show_list if
                                  show in all_show_embeddings}
    # Calculate the average vector for the user input shows
    user_input_vectors = list(user_input_show_embeddings.values())
    average_vector = np.mean(user_input_vectors, axis=0)
    logging.debug(f"Average Vector for User Input Shows: {average_vector}\n")

    # Calculate the similarity scores for all shows except the user input shows
    similarity_scores = {show: cosine_similarity(average_vector, show_embedding) for show, show_embedding in
                         all_show_embeddings.items()}
    for user_picked_show in user_input_show_list:
        similarity_scores.pop(user_picked_show, None)

    user_liked_actors = get_list_of_items_for_shows(user_input_show_list, 'Actors')
    user_liked_genres = get_list_of_items_for_shows(user_input_show_list, 'Genres')

    # Sort the shows by similarity score
    recommended_shows = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    logging.debug(f"Recommended Shows: {recommended_shows}\n")

    print("\nAwesome! I have found shows you might be interested in.\nTop 5 Recommended Shows for you:\n")
    for show, score in recommended_shows:
        final_score = score * 100
        logging.debug(show)
        # Boost score based on familiar character/genres.
        actors_in_recommended_show = get_list_of_items_for_shows([show], 'Actors')
        if any(actor in actors_in_recommended_show for actor in user_liked_actors):
            final_score = final_score + 5
        else:
            final_score = final_score - 2.3
        logging.debug(actors_in_recommended_show + user_liked_actors)
        genres_in_recommended_show = get_list_of_items_for_shows([show], 'Genres')
        if any(genre in genres_in_recommended_show for genre in user_liked_genres):
            final_score = final_score + 4.2
        else:
            final_score = final_score - 3.6
        if final_score >= 100:
            final_score = 99
        logging.debug(final_score)
        print(f"{show}: {final_score:.1f}%")

    return recommended_shows


def generate_made_up_show(show_list):
    prompt = f"""You're a professional Netflix show creator. My favorite shows are: {show_list}.
                Create a show I would love to watch. Please use an actor from the list of my favorite shows and explain the role and name you gave them.
                They don't have to be the main character, so you can mention them by the way in the description.
                In your answer, do not mention the shows I provided. Use this format:
                Name: Name of the show
                Description: Short description of the show (100 words max)"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}"}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    generated_show = response.choices[0].message.content
    show_name = generated_show.split("Name: ")[1].split("Description: ")[0]
    show_description = generated_show.split("Description: ")[1]

    return show_name.strip(), show_description.strip()


def generate_ad_for_a_shows(show_name, show_description):
    prompt = f"""
                You are a creative Movie poster designer. You have to create a poster for a new TV show called {show_name}.
                The show is about {show_description}.you can display the name of the show on the poster but do not add any additional text."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    ad_url = response.data[0].url  # Get the image URL
    print(f"To view an Ad for the show {show_name}, click Here: {ad_url}")


def generate_made_up_shows_and_ads(input_shows, recommended_real_tv_shows):
    show1_name, show1_description = generate_made_up_show(input_shows)
    show2_name, show2_description = generate_made_up_show(recommended_real_tv_shows)
    print("I have also created just for you two shows which I think you would love.")
    print("\n" + "~" * 20 + " Show 1 " + "~" * 20 + "\n")
    print(
        f"Show #1 is based on the fact that you loved the input shows that you gave me.\n"
        f"Its name is {show1_name}\n"
        f"{show1_description}.\n"
    )
    generate_ad_for_a_shows(show1_name, show1_description)

    print("\n" + "~" * 20 + " Show 2 " + "~" * 20 + "\n")
    print(
        f"Show #2 is based on the shows that I recommended for you.\n"
        f"Its name is {show2_name}.\n"
        f"{show2_description}.\n"
    )

    generate_ad_for_a_shows(show2_name, show2_description)

    print("\nHope you like them!\n")
    return {show1_name: show1_description, show2_name: show2_description}


def main():
    # Main function to run the TV show recommendation program
    while True:
        user_input = get_user_input()
        # Check if the input is not empty
        if user_input:
            # Interprets user input into shows from the list
            interpreted_shows = interpret_input_shows_names(user_input)
            if interpreted_shows and confirm_user_input(interpreted_shows):
                # Generate recommendations and custom shows
                recommendations = generate_real_tv_show_recommendations(interpreted_shows)
                custom_shows = generate_made_up_shows_and_ads(interpreted_shows, recommendations)
                break
            else:
                print(
                    "Sorry about that. Let's try again. Please make sure to write the names of the TV shows correctly.\n")
        else:
            print("Please enter at least one TV show.\n")


if __name__ == "__main__":
    main()
