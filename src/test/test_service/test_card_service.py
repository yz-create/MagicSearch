import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from business_object.card import Card
from business_object.filter import Filter
from service.card_service import CardService


# ========== Fixtures ==========

@pytest.fixture
def card_service():
    """Fixture to create a CardService instance"""
    return CardService()


@pytest.fixture
def sample_card():
    """Fixture to create a sample card"""
    return Card(
        id_card=1,
        layout="normal",
        name="Test Card",
        type_line="Creature - Human",
        mana_cost="{2}{U}",
        colors=["U"],
        mana_value=3,
        power="2",
        toughness="2"
    )


@pytest.fixture
def sample_filter():
    """Fixture to create a sample filter"""
    return Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )


# ========== Tests for create_card ==========

@patch('service.card_service.CardDao')
def test_create_card_success(mock_dao, card_service, sample_card):
    """Test successful card creation"""
    mock_dao_instance = Mock()
    mock_dao_instance.create_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.create_card(sample_card)

    assert result is True
    mock_dao_instance.create_card.assert_called_once_with(sample_card)


def test_create_card_invalid_input(card_service, capsys):
    """Test card creation with invalid input"""
    result = card_service.create_card("not a card")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid input: must be a Card instance" in captured.out


@patch('service.card_service.CardDao')
def test_create_card_db_exception(mock_dao, card_service, sample_card, capsys):
    """Test card creation with database exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.create_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.create_card(sample_card)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to create card in DB" in captured.out


# ========== Tests for update_card ==========

@patch('service.card_service.CardDao')
def test_update_card_success(mock_dao, card_service, sample_card):
    """Test successful card update"""
    mock_dao_instance = Mock()
    mock_dao_instance.update_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.update_card(sample_card)

    assert result is True
    mock_dao_instance.update_card.assert_called_once_with(sample_card)


def test_update_card_invalid_input(card_service, capsys):
    """Test card update with invalid input"""
    result = card_service.update_card(123)
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid input: must be a Card instance" in captured.out


@patch('service.card_service.CardDao')
def test_update_card_db_exception(mock_dao, card_service, sample_card, capsys):
    """Test card update with database exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.update_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.update_card(sample_card)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to update card in DB" in captured.out


# ========== Tests for delete_card ==========

@patch('service.card_service.CardDao')
def test_delete_card_success(mock_dao, card_service):
    """Test successful card deletion"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_card(1)

    assert result is True
    mock_dao_instance.delete_card.assert_called_once_with(1)


def test_delete_card_invalid_input(card_service, capsys):
    """Test card deletion with invalid input"""
    result = card_service.delete_card("not an int")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid input: id_card must be the id" in captured.out


@patch('service.card_service.CardDao')
def test_delete_card_db_exception(mock_dao, card_service, capsys):
    """Test card deletion with database exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_card(1)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to delete card from DB" in captured.out


# ========== Tests for id_search ==========

@patch('service.card_service.CardDao')
def test_id_search_success(mock_dao, card_service, sample_card):
    """Test successful search by ID"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(1)

    assert result == sample_card
    mock_dao_instance.id_search.assert_called_once_with(1)


def test_id_search_invalid_type(card_service, capsys):
    """Test search with invalid ID type"""
    result = card_service.id_search("not an int")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid id type: must be an integer" in captured.out


def test_id_search_negative_id(card_service, capsys):
    """Test search with negative ID"""
    result = card_service.id_search(-1)
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid id: must be non-negative" in captured.out


@patch('service.card_service.CardDao')
def test_id_search_id_too_high(mock_dao, card_service, capsys):
    """Test search with ID too high"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(150)

    assert result is None
    captured = capsys.readouterr()
    assert "Invalid id: must not exceed 100" in captured.out


@patch('service.card_service.CardDao')
def test_id_search_db_exception_get_max_id(mock_dao, card_service, capsys):
    """Test search with exception when retrieving max ID"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(1)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to get maximum id from DB" in captured.out


@patch('service.card_service.CardDao')
def test_id_search_db_exception_fetch(mock_dao, card_service, capsys):
    """Test search with exception when fetching card"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(1)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to fetch card from DB" in captured.out


# ========== Tests for name_search ==========

@patch('service.card_service.CardDao')
def test_name_search_success(mock_dao, card_service, sample_card):
    """Test successful search by name"""
    mock_dao_instance = Mock()
    mock_dao_instance.name_search.return_value = [sample_card]
    mock_dao.return_value = mock_dao_instance

    result = card_service.name_search("Test Card")

    assert result == [sample_card]
    mock_dao_instance.name_search.assert_called_once_with("Test Card")


def test_name_search_invalid_type(card_service, capsys):
    """Test search with invalid name type"""
    result = card_service.name_search(123)
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid name type: must be a string" in captured.out


def test_name_search_empty_string(card_service, capsys):
    """Test search with empty name"""
    result = card_service.name_search("   ")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid name: cannot be empty or whitespace" in captured.out


@patch('service.card_service.CardDao')
def test_name_search_db_exception(mock_dao, card_service, capsys):
    """Test search with database exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.name_search.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.name_search("Test")

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to fetch card from DB" in captured.out


# ========== Tests for semantic_search ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.embedding')
def test_semantic_search_success(mock_embedding, mock_dao, card_service, sample_card):
    """Test successful semantic search"""
    mock_embedding.return_value = [0.1, 0.2, 0.3]
    
    mock_dao_instance = Mock()
    mock_dao_instance.get_similar_entries.return_value = [(1, 0.9), (2, 0.8)]
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.semantic_search("Blue bird")

    assert len(result) == 2
    assert all(isinstance(card, Card) for card in result)
    mock_embedding.assert_called_once_with("Blue bird")


# ========== Tests for semantic_search_shortEmbed ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.embedding')
def test_semantic_search_short_embed_success(mock_embedding, mock_dao, card_service, sample_card):
    """Test successful semantic search with short embedding"""
    mock_embedding.return_value = [0.1, 0.2, 0.3]
    
    mock_dao_instance = Mock()
    mock_dao_instance.get_similar_entries.return_value = [(1, 0.9)]
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.semantic_search_shortEmbed("Red dragon")

    assert len(result) == 1
    assert isinstance(result[0], Card)
    mock_embedding.assert_called_once_with("Red dragon")


# ========== Tests for view_random_card ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.random.randint')
def test_view_random_card_success(mock_randint, mock_dao, card_service, sample_card):
    """Test successful random card display"""
    mock_randint.return_value = 5
    
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.view_random_card()

    assert result == sample_card
    mock_randint.assert_called_once_with(0, 100)


# ========== Tests for filter_search ==========
@patch('service.card_service.CardDao')
def test_filter_search_success_first_page(mock_dao, card_service, sample_card):
    """Test paginated search - first page"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    
    mock_card = Mock()
    mock_card.show_card.return_value = {"idCard": 1, "name": "Test Card"}
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.return_value = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
        42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52
    ]
    mock_dao_instance.id_search.return_value = mock_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1], page=1)

    assert result["count"] == 52
    assert result["page"] == 1
    assert result["total_pages"] == 2
    assert len(result["cards"]) == 50


@patch('service.card_service.CardDao')
def test_filter_search_success_second_page(mock_dao, card_service, sample_card):
    """Test paginated search - second page"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    
    mock_card = Mock()
    mock_card.show_card.return_value = {"idCard": 1, "name": "Test Card"}
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.return_value = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
        42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52
    ]
    mock_dao_instance.id_search.return_value = mock_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1], page=2)

    assert result["count"] == 52
    assert result["page"] == 2
    assert result["total_pages"] == 2
    assert len(result["cards"]) == 2


@patch('service.card_service.CardDao')
def test_filter_search_multiple_filters(mock_dao, card_service, sample_card):
    """Test paginated search with multiple filters"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    filter2 = Filter(
        variable_filtered="color",
        type_of_filtering="positive",
        filtering_value="U"
    )
    
    mock_card = Mock()
    mock_card.show_card.return_value = {"idCard": 1, "name": "Test Card"}
    
    mock_dao_instance = Mock()
    # Intersection: [2, 3, 4, 5, 6]
    mock_dao_instance.filter_dao.side_effect = [
        [1, 2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 8, 9]
    ]
    mock_dao_instance.id_search.return_value = mock_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1, filter2], page=1)

    # Intersection = 5 cards[2,3,4,5,6]
    assert result["count"] == 5
    assert result["page"] == 1
    assert result["total_pages"] == 1
    assert len(result["cards"]) == 5

@patch('service.card_service.CardDao')
def test_filter_search_no_results(mock_dao, card_service):
    """Test paginated search with no results"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.return_value = []
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1], page=1)

    assert result["count"] == 0
    assert result["page"] == 1
    assert result["total_pages"] == 0
    assert result["cards"] == []


@patch('service.card_service.CardDao')
def test_filter_search_no_intersection(mock_dao, card_service):
    """Test paginated search with no common results"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    filter2 = Filter(
        variable_filtered="color",
        type_of_filtering="positive",
        filtering_value="U"
    )
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.side_effect = [[1, 2, 3], [4, 5, 6]]  # No intersection
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1, filter2], page=1, )

    assert result["count"] == 0
    assert result["cards"] == []


def test_filter_search_invalid_filter(card_service):
    """Test paginated search with invalid filter"""
    filter1 = Filter(
        variable_filtered="invalid_var",
        type_of_filtering="positive",
        filtering_value="test"
    )
    
    result = card_service.filter_search([filter1], page=1)

    assert "error" in result or result["count"] == 0


def test_filter_search_empty_filters(card_service):
    """Test paginated search with empty filter list"""
    result = card_service.filter_search([], page=1)

    assert result["count"] == 0
    assert result["cards"] == []


@patch('service.card_service.CardDao')
def test_filter_search_page_beyond_results(mock_dao, card_service, sample_card):
    """Test requesting a page beyond available results"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.return_value = [1, 2, 3]
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1], page=10)

    # Page 10 doesn't exist
    assert result["count"] == 3
    assert result["page"] == 10
    assert result["total_pages"] == 1
    assert result["cards"] == []  # There are no cards on this page

# ========== Tests for add_favourite_card ==========

@patch('service.card_service.CardDao')
def test_add_favourite_card_success_added(mock_dao, card_service, capsys):
    """Test successful addition of card to favorites"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.return_value = "ADDED"
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is True
    captured = capsys.readouterr()
    assert "had been added to your favourites" in captured.out


@patch('service.card_service.CardDao')
def test_add_favourite_card_already_exists(mock_dao, card_service, capsys):
    """Test adding card already in favorites"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.return_value = "EXISTS"
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is True
    captured = capsys.readouterr()
    assert "already in your favourites" in captured.out


@patch('service.card_service.CardDao')
def test_add_favourite_card_error(mock_dao, card_service, capsys):
    """Test adding card with error"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.return_value = "ERROR"
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is False
    captured = capsys.readouterr()
    assert "Error adding the card" in captured.out


def test_add_favourite_card_invalid_user_id_type(card_service):
    """Test adding card with invalid user_id type"""
    result = card_service.add_favourite_card("not an int", 10)

    assert result is False


def test_add_favourite_card_invalid_card_id_type(card_service):
    """Test adding card with invalid idCard type"""
    result = card_service.add_favourite_card(1, "not an int")

    assert result is False


@patch('service.card_service.CardDao')
def test_add_favourite_card_exception(mock_dao, card_service):
    """Test adding card with exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is False


# ========== Tests for list_favourite_cards ==========

@patch('service.card_service.CardDao')
def test_list_favourite_cards_success(mock_dao, card_service, sample_card):
    """Test successful listing of favorite cards"""
    mock_dao_instance = Mock()
    mock_dao_instance.list_favourite_cards.return_value = [sample_card]
    mock_dao.return_value = mock_dao_instance

    result = card_service.list_favourite_cards(1)

    assert result == [sample_card]
    mock_dao_instance.list_favourite_cards.assert_called_once_with(1)


def test_list_favourite_cards_invalid_user_id_type(card_service):
    """Test listing with invalid user_id type"""
    result = card_service.list_favourite_cards("not an int")

    assert result is False


@patch('service.card_service.CardDao')
def test_list_favourite_cards_exception(mock_dao, card_service):
    """Test listing with exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.list_favourite_cards.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.list_favourite_cards(1)

    assert result is False


# ========== Tests for delete_favourite_card ==========

@patch('service.card_service.CardDao')
def test_delete_favourite_card_success(mock_dao, card_service):
    """Test successful removal of card from favorites"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_favourite_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_favourite_card(1, 10)

    assert result is True
    mock_dao_instance.delete_favourite_card.assert_called_once_with(1, 10)


def test_delete_favourite_card_invalid_user_id_type(card_service):
    """Test removal with invalid user_id type"""
    result = card_service.delete_favourite_card("not an int", 10)

    assert result is False


def test_delete_favourite_card_invalid_card_id_type(card_service):
    """Test removal with invalid idCard type"""
    result = card_service.delete_favourite_card(1, "not an int")

    assert result is False


@patch('service.card_service.CardDao')
def test_delete_favourite_card_exception(mock_dao, card_service):
    """Test removal with exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_favourite_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_favourite_card(1, 10)

    assert result is False


# ========== Tests for cardModel_to_Card ==========

def test_card_model_to_card_conversion(card_service):
    """Test conversion from card model to Card object"""
    # Create a mock card_model with all necessary attributes
    card_model = Mock()
    card_model.id_card = 1
    card_model.layout = "normal"
    card_model.name = "Test Card"
    card_model.type_line = "Creature"
    card_model.ascii_name = "Test Card"
    card_model.color_identity = ["U"]
    card_model.color_indicator = None
    card_model.colors = ["U"]
    card_model.converted_mana_cost = 3
    card_model.defense = None
    card_model.edhrec_rank = 100
    card_model.edhrec_saltiness = 0.5
    card_model.face_mana_value = None
    card_model.face_name = None
    card_model.first_printing = "2020"
    card_model.foreign_data = []
    card_model.hand = None
    card_model.has_alternative_deck_limit = False
    card_model.is_funny = False
    card_model.keywords = []
    card_model.leadership_skills = None
    card_model.legalities = {}
    card_model.life = None
    card_model.loyalty = None
    card_model.mana_cost = "{2}{U}"
    card_model.mana_value = 3
    card_model.power = "2"
    card_model.printings = []
    card_model.purchase_urls = {}
    card_model.rulings = []
    card_model.side = None
    card_model.subtypes = ["Human"]
    card_model.supertypes = []
    card_model.text = "Test text"
    card_model.toughness = "2"
    card_model.types = ["Creature"]

    result = card_service.cardModel_to_Card(card_model)

    assert isinstance(result, Card)
    assert result.id_card == 1
    assert result.name == "Test Card"
    assert result.mana_value == 3


# ========== Integration tests ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.random.randint')
def test_integration_random_card_returns_valid_card(mock_randint, mock_dao):
    """Integration test: view_random_card returns a valid card"""
    mock_randint.return_value = 5
    
    sample_card = Card(
        id_card=5,
        layout="normal",
        name="Random Card",
        type_line="Creature"
    )
    
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    service = CardService()
    result = service.view_random_card()

    assert result is not None
    assert result.id_card == 5


@patch('service.card_service.CardDao')
def test_integration_filter_search_with_multiple_filters_returns_intersection(mock_dao):
    """Integration test: filter_search returns the intersection of results"""
    filter1 = Filter("manaValue", "equal_to", 3)
    filter2 = Filter("power", "higher_than", 2)
    
    card1 = Card(
        id_card=2,
        layout="normal",
        name="Card 2",
        type_line="Creature"
    )
    card2 = Card(
        id_card=3,
        layout="normal",
        name="Card 3",
        type_line="Creature"
    )
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.side_effect = [
        [1, 2, 3, 4],  # Results from first filter
        [2, 3, 5, 6]   # Results from second filter
    ]
    mock_dao_instance.id_search.side_effect = [card1, card2]
    mock_dao.return_value = mock_dao_instance

    service = CardService()
    result = service.filter_search([filter1, filter2])

    # Intersection is [2, 3]
    assert len(result) == 2
    assert all(card.id_card in [2, 3] for card in result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])