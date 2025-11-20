import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from business_object.card import Card
from business_object.filter import Filter
from service.card_service import CardService


# ========== Fixtures ==========

@pytest.fixture
def card_service():
    """Fixture pour créer une instance de CardService"""
    return CardService()


@pytest.fixture
def sample_card():
    """Fixture pour créer une carte exemple"""
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
    """Fixture pour créer un filtre exemple"""
    return Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )


# ========== Tests pour create_card ==========

@patch('service.card_service.CardDao')
def test_create_card_success(mock_dao, card_service, sample_card):
    """Test de création réussie d'une carte"""
    mock_dao_instance = Mock()
    mock_dao_instance.create_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.create_card(sample_card)

    assert result is True
    mock_dao_instance.create_card.assert_called_once_with(sample_card)


def test_create_card_invalid_input(card_service, capsys):
    """Test de création avec une entrée invalide"""
    result = card_service.create_card("not a card")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid input: must be a Card instance" in captured.out


@patch('service.card_service.CardDao')
def test_create_card_db_exception(mock_dao, card_service, sample_card, capsys):
    """Test de création avec une exception de base de données"""
    mock_dao_instance = Mock()
    mock_dao_instance.create_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.create_card(sample_card)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to create card in DB" in captured.out


# ========== Tests pour update_card ==========

@patch('service.card_service.CardDao')
def test_update_card_success(mock_dao, card_service, sample_card):
    """Test de mise à jour réussie d'une carte"""
    mock_dao_instance = Mock()
    mock_dao_instance.update_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.update_card(sample_card)

    assert result is True
    mock_dao_instance.update_card.assert_called_once_with(sample_card)


def test_update_card_invalid_input(card_service, capsys):
    """Test de mise à jour avec une entrée invalide"""
    result = card_service.update_card(123)
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid input: must be a Card instance" in captured.out


@patch('service.card_service.CardDao')
def test_update_card_db_exception(mock_dao, card_service, sample_card, capsys):
    """Test de mise à jour avec une exception de base de données"""
    mock_dao_instance = Mock()
    mock_dao_instance.update_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.update_card(sample_card)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to update card in DB" in captured.out


# ========== Tests pour delete_card ==========

@patch('service.card_service.CardDao')
def test_delete_card_success(mock_dao, card_service):
    """Test de suppression réussie d'une carte"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_card(1)

    assert result is True
    mock_dao_instance.delete_card.assert_called_once_with(1)


def test_delete_card_invalid_input(card_service, capsys):
    """Test de suppression avec une entrée invalide"""
    result = card_service.delete_card("not an int")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid input: id_card must be the id" in captured.out


@patch('service.card_service.CardDao')
def test_delete_card_db_exception(mock_dao, card_service, capsys):
    """Test de suppression avec une exception de base de données"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_card(1)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to delete card from DB" in captured.out


# ========== Tests pour id_search ==========

@patch('service.card_service.CardDao')
def test_id_search_success(mock_dao, card_service, sample_card):
    """Test de recherche par ID réussie"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(1)

    assert result == sample_card
    mock_dao_instance.id_search.assert_called_once_with(1)


def test_id_search_invalid_type(card_service, capsys):
    """Test de recherche avec un type d'ID invalide"""
    result = card_service.id_search("not an int")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid id type: must be an integer" in captured.out


def test_id_search_negative_id(card_service, capsys):
    """Test de recherche avec un ID négatif"""
    result = card_service.id_search(-1)
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid id: must be non-negative" in captured.out


@patch('service.card_service.CardDao')
def test_id_search_id_too_high(mock_dao, card_service, capsys):
    """Test de recherche avec un ID trop élevé"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(150)

    assert result is None
    captured = capsys.readouterr()
    assert "Invalid id: must not exceed 100" in captured.out


@patch('service.card_service.CardDao')
def test_id_search_db_exception_get_max_id(mock_dao, card_service, capsys):
    """Test de recherche avec exception lors de la récupération de l'ID max"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(1)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to get maximum id from DB" in captured.out


@patch('service.card_service.CardDao')
def test_id_search_db_exception_fetch(mock_dao, card_service, capsys):
    """Test de recherche avec exception lors de la récupération de la carte"""
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.id_search(1)

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to fetch card from DB" in captured.out


# ========== Tests pour name_search ==========

@patch('service.card_service.CardDao')
def test_name_search_success(mock_dao, card_service, sample_card):
    """Test de recherche par nom réussie"""
    mock_dao_instance = Mock()
    mock_dao_instance.name_search.return_value = [sample_card]
    mock_dao.return_value = mock_dao_instance

    result = card_service.name_search("Test Card")

    assert result == [sample_card]
    mock_dao_instance.name_search.assert_called_once_with("Test Card")


def test_name_search_invalid_type(card_service, capsys):
    """Test de recherche avec un type de nom invalide"""
    result = card_service.name_search(123)
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid name type: must be a string" in captured.out


def test_name_search_empty_string(card_service, capsys):
    """Test de recherche avec un nom vide"""
    result = card_service.name_search("   ")
    
    assert result is None
    captured = capsys.readouterr()
    assert "Invalid name: cannot be empty or whitespace" in captured.out


@patch('service.card_service.CardDao')
def test_name_search_db_exception(mock_dao, card_service, capsys):
    """Test de recherche avec exception de base de données"""
    mock_dao_instance = Mock()
    mock_dao_instance.name_search.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.name_search("Test")

    assert result is None
    captured = capsys.readouterr()
    assert "Failed to fetch card from DB" in captured.out


# ========== Tests pour semantic_search ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.embedding')
def test_semantic_search_success(mock_embedding, mock_dao, card_service, sample_card):
    """Test de recherche sémantique réussie"""
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


# ========== Tests pour semantic_search_shortEmbed ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.embedding')
def test_semantic_search_short_embed_success(mock_embedding, mock_dao, card_service, sample_card):
    """Test de recherche sémantique avec embedding court réussie"""
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


# ========== Tests pour view_random_card ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.random.randint')
def test_view_random_card_success(mock_randint, mock_dao, card_service, sample_card):
    """Test d'affichage d'une carte aléatoire réussie"""
    mock_randint.return_value = 5
    
    mock_dao_instance = Mock()
    mock_dao_instance.get_highest_id.return_value = 100
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.view_random_card()

    assert result == sample_card
    mock_randint.assert_called_once_with(0, 100)


# ========== Tests pour filter_search ==========

@patch('service.card_service.CardDao')
def test_filter_search_success_single_filter(mock_dao, card_service, sample_card):
    """Test de recherche avec un seul filtre réussie"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.return_value = [1, 2, 3]
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1])

    assert len(result) == 3
    assert all(isinstance(card, Card) for card in result)


@patch('service.card_service.CardDao')
def test_filter_search_success_multiple_filters(mock_dao, card_service, sample_card):
    """Test de recherche avec plusieurs filtres réussie"""
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
    mock_dao_instance.filter_dao.side_effect = [[1, 2, 3], [2, 3, 4]]
    mock_dao_instance.id_search.return_value = sample_card
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1, filter2])

    # L'intersection de [1,2,3] et [2,3,4] est [2,3]
    assert len(result) == 2


def test_filter_search_invalid_categorical_variable(card_service):
    """Test de recherche avec une variable catégorielle invalide"""
    filter1 = Filter(
        variable_filtered="invalid_var",
        type_of_filtering="positive",
        filtering_value="test"
    )
    
    result = card_service.filter_search([filter1])

    assert result == []


def test_filter_search_invalid_numerical_variable(card_service):
    """Test de recherche avec une variable numérique invalide"""
    filter1 = Filter(
        variable_filtered="invalid_var",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    
    result = card_service.filter_search([filter1])

    assert result == []


def test_filter_search_invalid_filter_type(card_service):
    """Test de recherche avec un type de filtre invalide"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="invalid_type",
        filtering_value=3
    )
    
    result = card_service.filter_search([filter1])

    assert result == []


def test_filter_search_invalid_filtering_value_type(card_service):
    """Test avec une valeur de filtrage de type invalide pour un filtre catégoriel"""
    filter1 = Filter(
        variable_filtered="color",
        type_of_filtering="positive",
        filtering_value=123  # Devrait être un string
    )
    
    result = card_service.filter_search([filter1])

    assert result == []


@patch('service.card_service.CardDao')
def test_filter_search_no_common_results(mock_dao, card_service):
    """Test de recherche sans résultats communs"""
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
    mock_dao_instance.filter_dao.side_effect = [[1, 2], [3, 4]]  # Pas d'intersection
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1, filter2])

    assert result == []


@patch('service.card_service.CardDao')
def test_filter_search_one_filter_returns_empty(mock_dao, card_service):
    """Test de recherche où un filtre ne retourne rien"""
    filter1 = Filter(
        variable_filtered="manaValue",
        type_of_filtering="equal_to",
        filtering_value=3
    )
    
    mock_dao_instance = Mock()
    mock_dao_instance.filter_dao.return_value = []
    mock_dao.return_value = mock_dao_instance

    result = card_service.filter_search([filter1])

    assert result == []


# ========== Tests pour add_favourite_card ==========

@patch('service.card_service.CardDao')
def test_add_favourite_card_success_added(mock_dao, card_service, capsys):
    """Test d'ajout réussi d'une carte aux favoris"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.return_value = "ADDED"
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is True
    captured = capsys.readouterr()
    assert "had been added to your favourites" in captured.out


@patch('service.card_service.CardDao')
def test_add_favourite_card_already_exists(mock_dao, card_service, capsys):
    """Test d'ajout d'une carte déjà dans les favoris"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.return_value = "EXISTS"
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is True
    captured = capsys.readouterr()
    assert "already in your favourites" in captured.out


@patch('service.card_service.CardDao')
def test_add_favourite_card_error(mock_dao, card_service, capsys):
    """Test d'ajout avec erreur"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.return_value = "ERROR"
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is False
    captured = capsys.readouterr()
    assert "Error adding the card" in captured.out


def test_add_favourite_card_invalid_user_id_type(card_service):
    """Test d'ajout avec un type d'user_id invalide"""
    result = card_service.add_favourite_card("not an int", 10)

    assert result is False


def test_add_favourite_card_invalid_card_id_type(card_service):
    """Test d'ajout avec un type d'idCard invalide"""
    result = card_service.add_favourite_card(1, "not an int")

    assert result is False


@patch('service.card_service.CardDao')
def test_add_favourite_card_exception(mock_dao, card_service):
    """Test d'ajout avec exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.add_favourite_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.add_favourite_card(1, 10)

    assert result is False


# ========== Tests pour list_favourite_cards ==========

@patch('service.card_service.CardDao')
def test_list_favourite_cards_success(mock_dao, card_service, sample_card):
    """Test de listage des cartes favorites réussi"""
    mock_dao_instance = Mock()
    mock_dao_instance.list_favourite_cards.return_value = [sample_card]
    mock_dao.return_value = mock_dao_instance

    result = card_service.list_favourite_cards(1)

    assert result == [sample_card]
    mock_dao_instance.list_favourite_cards.assert_called_once_with(1)


def test_list_favourite_cards_invalid_user_id_type(card_service):
    """Test de listage avec un type d'user_id invalide"""
    result = card_service.list_favourite_cards("not an int")

    assert result is False


@patch('service.card_service.CardDao')
def test_list_favourite_cards_exception(mock_dao, card_service):
    """Test de listage avec exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.list_favourite_cards.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.list_favourite_cards(1)

    assert result is False


# ========== Tests pour delete_favourite_card ==========

@patch('service.card_service.CardDao')
def test_delete_favourite_card_success(mock_dao, card_service):
    """Test de suppression d'une carte des favoris réussie"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_favourite_card.return_value = True
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_favourite_card(1, 10)

    assert result is True
    mock_dao_instance.delete_favourite_card.assert_called_once_with(1, 10)


def test_delete_favourite_card_invalid_user_id_type(card_service):
    """Test de suppression avec un type d'user_id invalide"""
    result = card_service.delete_favourite_card("not an int", 10)

    assert result is False


def test_delete_favourite_card_invalid_card_id_type(card_service):
    """Test de suppression avec un type d'idCard invalide"""
    result = card_service.delete_favourite_card(1, "not an int")

    assert result is False


@patch('service.card_service.CardDao')
def test_delete_favourite_card_exception(mock_dao, card_service):
    """Test de suppression avec exception"""
    mock_dao_instance = Mock()
    mock_dao_instance.delete_favourite_card.side_effect = Exception("DB Error")
    mock_dao.return_value = mock_dao_instance

    result = card_service.delete_favourite_card(1, 10)

    assert result is False


# ========== Tests pour cardModel_to_Card ==========

def test_card_model_to_card_conversion(card_service):
    """Test de conversion d'un modèle de carte en objet Card"""
    # Créer un mock de card_model avec tous les attributs nécessaires
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


# ========== Tests d'intégration ==========

@patch('service.card_service.CardDao')
@patch('service.card_service.random.randint')
def test_integration_random_card_returns_valid_card(mock_randint, mock_dao):
    """Test d'intégration : view_random_card retourne une carte valide"""
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
    """Test d'intégration : filter_search retourne bien l'intersection des résultats"""
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
        [1, 2, 3, 4],  # Résultats du premier filtre
        [2, 3, 5, 6]   # Résultats du deuxième filtre
    ]
    mock_dao_instance.id_search.side_effect = [card1, card2]
    mock_dao.return_value = mock_dao_instance

    service = CardService()
    result = service.filter_search([filter1, filter2])

    # L'intersection est [2, 3]
    assert len(result) == 2
    assert all(card.id_card in [2, 3] for card in result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])