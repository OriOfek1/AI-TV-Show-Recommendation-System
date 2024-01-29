import pytest
import ShowSuggesterAI

def test_interpret_input_shows_names():
    assert ShowSuggesterAI.interpret_input_shows_names("the office, frng") == ["The Office", "Fringe"]
    assert ShowSuggesterAI.interpret_input_shows_names("Game of Thrones") == ["Game of Thrones"]
    assert ShowSuggesterAI.interpret_input_shows_names("gem of thrones, lupin, breaking") == ["Game of Thrones", "Lupin", "Breaking Bad"]
    assert ShowSuggesterAI.interpret_input_shows_names("xyz, abc, 123") == []

def test_get_list_of_items_for_shows():
    genres = set(ShowSuggesterAI.get_list_of_items_for_shows(["The Office", "Fringe"], "Genres"))
    assert genres == set(['Comedy', 'Drama', 'Mystery', 'Sci-Fi'])
    actors = set(ShowSuggesterAI.get_list_of_items_for_shows(["Game of Thrones", "Breaking Bad"], "Actors"))
    assert actors == set(['Bryan Cranston', 'Aaron Paul', 'Peter Dinklage', 'Lena Headey', 'Emilia Clarke', 'Kit Harington','Anna Gunn', 'Betsy Brandt'])

