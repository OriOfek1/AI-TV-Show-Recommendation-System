import os
import logging
from openai import OpenAI, Client, embeddings
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.DEBUG)
                    
def get_user_input():
    # Get user input for TV shows
    return input("Which TV shows did you love watching? Separate them by a comma. Make sure to enter more than 1 show: ")

def interpret_shows_names(user_input):
    # TODO: Implement fuzzy string matching for TV show interpretation
    interpreted_shows = [show.strip().title() for show in user_input.split(',')]
    logging.debug("TV show interpretation is pending implementation of fuzzy.\n")
    return interpreted_shows

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
        interpreted_shows = interpret_shows_names(user_input)

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
