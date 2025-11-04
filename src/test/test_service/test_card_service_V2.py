import pytest
from unittest.mock import MagicMock, patch, Mock
import requests

from service.card_service import CardService
from dao.card_dao import CardDao
from business_object.card import Card
from business_object.filters.abstract_filter import AbstractFilter


# ----- Fixtures -----

@pytest.fixture
def card_service():
    """Fixture pour créer une instance de CardService"""
    return CardService()


@pytest.fixture
def mock_card():
    """Fixture pour créer une carte mock"""
    return Card(
        ascii_name="Test Card",
        color_identity=["R", "G"],
        color_indicator=[],
        colors=["R", "G"],
        converted_mana_cost=3.0,
        name="Test Card",
        mana_value=3.0,
        text="Test card text",
        type_line="Creature - Test",
        types=["Creature"],
        subtypes=["Test"],
        supertypes=[],
        power="3",
        toughness="3",
        mana_cost="{2}{R}",
        embedded=[0.1, 0.2, 0.3]
    )


@pytest.fixture
def mock_card_list():
    """Fixture pour créer une liste de cartes mock"""
    cards = []
    for i in range(5):
        card = Card(
            ascii_name=f"Card {i}",
            color_identity=["R"],
            color_indicator=[],
            colors=["R"],
            converted_mana_cost=float(i),
            name=f"Card {i}",
            mana_value=float(i),
            text=f"Card {i} text",
            type_line="Creature",
            types=["Creature"],
            subtypes=[],
            supertypes=[],
            power=str(i),
            toughness=str(i),
            mana_cost=f"{{{i}}}{{R}}",
            embedded=[0.1 * i, 0.2 * i, 0.3 * i]
        )
        cards.append(card)
    return cards


@pytest.fixture
def mock_filter():
    """Fixture pour créer un filtre mock"""
    filter_mock = Mock(spec=AbstractFilter)
    filter_mock.variable_filtered = "type"
    filter_mock.type_of_filtering = "positive"
    filter_mock.filtering_value = "Creature"
    return filter_mock


# ----- Tests id_search -----

def test_id_search_success(card_service, mock_card):
    """Test de recherche par ID réussie"""
    # GIVEN
    card_id = 42
    card_service.card_dao.find_by_id = MagicMock(return_value=mock_card)
    
    # WHEN
    result = card_service.id_search(card_id)
    
    # THEN
    assert result == mock_card
    card_service.card_dao.find_by_id.assert_called_once_with(card_id)



if __name__ == "__main__":
    pytest.main([__file__, "-v"])