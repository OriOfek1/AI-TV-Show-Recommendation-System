import pytest
import ShowSuggesterAI

def test_interpret_shows_names():
    assert ShowSuggesterAI.interpret_shows_names("the office, friends") == ["The Office", "Friends"]

# def test_confirm_user_input():
#     pass

# def test_generate_real_tv_show_recommendations():
#     pass   

# def test_generate_made_up_show_input_based():
#     pass

# def test_generate_made_up_show_based_on_recommendations():
#     pass

# def test_generate_ad_for_a_shows():
#     pass

# def test_generate_made_up_shows():
#     pass

# def test_main():
#     pass