import logging
import csv
from fuzzywuzzy import process
import numpy as np


# Configure logging
logging.basicConfig(level=logging.DEBUG)
csv_filename = "imdb_tvshows - imdb_tvshows.csv"

                    
def get_user_input():
    # Get user input for TV shows
    return input("Which TV shows did you love watching? Separate them by a comma. Make sure to enter more than 1 show: ")

def interpret_input_shows_names(user_input):
    # using fuzzywuzzy to interpret the user input

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

def generate_real_tv_show_recommendations():
    #TODO: Generate TV show recommendations using the embeddings api
    logging.debug("TV show recommendations generation is pending implementation.\n")
    return []

def generate_made_up_show_input_based(input_shows):
        # TODO: Generate a made-up show based on the input shows
        logging.debug("Generating a made-up show based on input shows is pending implementation.\n")
        show1_name = "Show1_name"
        show1_description = "Show1_description"
        return show1_name, show1_description

def generate_made_up_show_based_on_recommendations(recommended_shows):
    # TODO: Generate a made-up show based on the recommended shows
    logging.debug("Generating a made-up show based on recommended shows is pending implementation.\n")
    show2_name = "Show2_name"
    show2_description = "Show2_description"
    return show2_name, show2_description

def generate_ad_for_a_shows(show_name, show_description):
    #TODO: Generate an ad for a show using dale-e
    logging.debug("Generating an ad image for a show is pending implementation.\n")
    pass

def generate_made_up_shows(input_shows, recommended_real_tv_shows):
    
    show1_name, show1_description = generate_made_up_show_input_based(input_shows)
    show2_name, show2_description = generate_made_up_show_based_on_recommendations(recommended_real_tv_shows)

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
        interpreted_shows = interpret_input_shows_names(user_input)

        if confirm_user_input(interpreted_shows):
            # Generate recommendations and custom shows
            recommendations = generate_real_tv_show_recommendations()

            # Display recommendations
            for recommendation in recommendations:
                print(f"{recommendation['name']} ({recommendation['score']}%)")

            custom_shows = generate_made_up_shows(interpreted_shows, recommendations)
            break
        else:
            print("Sorry about that. Let's try again. Please make sure to write the names of the TV shows correctly.")

if __name__ == "__main__":
    main()
