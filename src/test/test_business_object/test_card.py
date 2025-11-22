import pytest
from business_object.card import Card


# Fixtures 

@pytest.fixture
def card_all_collections_initialized():
    """Card with all list/dict collections properly initialized"""
    return Card(
        id_card=1,
        layout="normal",
        name="Test Card",
        type_line="Instant",
        color_identity=[],
        color_indicator=[],
        colors=[],
        keywords=[],
        printings=[],
        rulings=[],
        subtypes=[],
        supertypes=[],
        types=[],
        leadership_skills={},
        legalities={},
        purchase_urls={},
        foreign_data=[]
    )


@pytest.fixture
def complete_card_for_display():
    """Complete card for show_card testing"""
    return Card(
        id_card=2,
        layout="normal",
        name="Serra Angel",
        type_line="Creature - Angel",
        mana_cost="{3}{W}{W}",
        mana_value=5.0,
        power="4",
        toughness="4",
        text="Flying, vigilance",
        color_identity=["W"],
        color_indicator=[],
        colors=["W"],
        keywords=["Flying", "Vigilance"],
        printings=["LEA", "LEB"],
        rulings=[{"date": "2020-01-01", "text": "Some ruling"}],
        subtypes=["Angel"],
        supertypes=[],
        types=["Creature"],
        leadership_skills={"brawl": True},
        legalities={"standard": "not_legal", "modern": "legal"},
        purchase_urls={"tcgplayer": "https://example.com"},
        foreign_data=[
            {"language": "French", "name": "Ange de Serra"},
            {"language": "German", "name": "Serra-Engel"}
        ],
        edhrec_rank=1000,
        first_printing="1993-08-05"
    )


# Tests show_card

def test_show_card_value(card_all_collections_initialized):
    """Test that show_card returns a dictionary"""
    result = card_all_collections_initialized.show_card()
    assert isinstance(result, dict)


def test_show_card_contains_required_fields(card_all_collections_initialized):
    """Test that show_card always includes required fields"""
    result = card_all_collections_initialized.show_card()
    
    assert "id_card" in result
    assert "layout" in result
    assert "name" in result
    assert "type_line" in result
    
    assert result["id_card"] == 1
    assert result["layout"] == "normal"
    assert result["name"] == "Test Card"
    assert result["type_line"] == "Instant"


def test_show_card_minimal_only_required_fields(card_all_collections_initialized):
    """Test that minimal card only returns required fields"""
    result = card_all_collections_initialized.show_card()
    
    # Should only have the 4 required fields
    assert len(result) == 4
    assert set(result.keys()) == {"id_card", "layout", "name", "type_line"}


def test_show_card_includes_optional_scalar_attributes():
    """Test that show_card includes non-None scalar attributes"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Lightning Bolt",
        type_line="Instant",
        mana_cost="{R}",
        mana_value=1.0,
        text="Deal 3 damage",
        power="3",
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    assert result["mana_cost"] == "{R}"
    assert result["mana_value"] == 1.0
    assert result["text"] == "Deal 3 damage"
    assert result["power"] == "3"


def test_show_card_excludes_none_scalar_attributes():
    """Test that show_card excludes None scalar attributes"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        power=None,
        toughness=None,
        loyalty=None,
        defense=None,
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    assert "power" not in result
    assert "toughness" not in result
    assert "loyalty" not in result
    assert "defense" not in result


def test_show_card_includes_non_empty_lists():
    """Test that show_card includes non-empty list attributes"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Dragon",
        type_line="Creature - Dragon",
        keywords=["Flying", "Haste"],
        subtypes=["Dragon"],
        types=["Creature"],
        printings=["M20", "M21"],
        color_identity=["R"],
        color_indicator=[],
        colors=["R"]
    )
    
    result = card.show_card()
    
    assert result["keywords"] == ["Flying", "Haste"]
    assert result["subtypes"] == ["Dragon"]
    assert result["types"] == ["Creature"]
    assert result["printings"] == ["M20", "M21"]
    assert result["color_identity"] == ["R"]
    assert result["colors"] == ["R"]


def test_show_card_excludes_empty_lists():
    """Test that show_card excludes empty list attributes"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        keywords=[],
        subtypes=[],
        types=[],
        printings=[],
        color_identity=[],
        color_indicator=[],
        colors=[],
        rulings=[],
        supertypes=[]
    )
    
    result = card.show_card()
    
    # Should only have required fields
    assert "keywords" not in result
    assert "subtypes" not in result
    assert "types" not in result
    assert "printings" not in result
    assert "color_identity" not in result
    assert "color_indicator" not in result
    assert "colors" not in result
    assert "rulings" not in result
    assert "supertypes" not in result


def test_show_card_includes_non_empty_dicts():
    """Test that show_card includes non-empty dict attributes"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        legalities={"standard": "legal", "modern": "legal"},
        purchase_urls={"tcgplayer": "https://example.com"},
        leadership_skills={"commander": True},
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    assert "legalities" in result
    assert result["legalities"] == {"standard": "legal", "modern": "legal"}
    assert result["purchase_urls"] == {"tcgplayer": "https://example.com"}
    assert result["leadership_skills"] == {"commander": True}


def test_show_card_excludes_empty_dicts():
    """Test that show_card excludes empty dict attributes"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        legalities={},
        purchase_urls={},
        leadership_skills={},
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    assert "legalities" not in result
    assert "purchase_urls" not in result
    assert "leadership_skills" not in result


def test_show_card_filters_falsy_values_in_dicts():
    """Test that show_card filters out falsy values in dict attributes"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        legalities={"standard": "legal", "vintage": None, "legacy": False, "modern": ""},
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    # Only truthy values should be included
    assert result["legalities"] == {"standard": "legal"}
    assert "vintage" not in result["legalities"]
    assert "legacy" not in result["legalities"]
    assert "modern" not in result["legalities"]


def test_show_card_includes_foreign_data():
    """Test that show_card includes non-empty foreign_data"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        foreign_data=[
            {"language": "French", "name": "Test FR", "text": "Texte"},
            {"language": "German", "name": "Test DE"}
        ],
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    assert "foreignData" in result
    assert len(result["foreignData"]) == 2
    assert result["foreignData"][0]["language"] == "French"
    assert result["foreignData"][1]["language"] == "German"


def test_show_card_filters_none_in_foreign_data():
    """Test that show_card filters None values in foreign_data"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        foreign_data=[
            {"language": "French", "name": "Test FR", "text": None, "multiverseId": 123},
            {"language": "German", "name": None, "text": "Text"}
        ],
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    assert "foreignData" in result
    # First entry should not have 'text' key
    assert "text" not in result["foreignData"][0]
    assert result["foreignData"][0]["language"] == "French"
    assert result["foreignData"][0]["multiverseId"] == 123
    
    # Second entry should not have 'name' key
    assert "name" not in result["foreignData"][1]
    assert result["foreignData"][1]["language"] == "German"


def test_show_card_excludes_empty_foreign_data():
    """Test that show_card excludes empty foreign_data"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        foreign_data=[],
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    assert "foreignData" not in result


def test_show_card_complete_card(complete_card_for_display):
    """Test show_card with a complete card"""
    result = complete_card_for_display.show_card()
    
    # Check required fields
    assert result["id_card"] == 2
    assert result["name"] == "Serra Angel"
    assert result["layout"] == "normal"
    assert result["type_line"] == "Creature - Angel"
    
    # Check optional scalars
    assert result["mana_cost"] == "{3}{W}{W}"
    assert result["mana_value"] == 5.0
    assert result["power"] == "4"
    assert result["toughness"] == "4"
    assert result["text"] == "Flying, vigilance"
    
    # Check lists
    assert result["color_identity"] == ["W"]
    assert result["colors"] == ["W"]
    assert result["keywords"] == ["Flying", "Vigilance"]
    assert result["subtypes"] == ["Angel"]
    assert result["types"] == ["Creature"]
    
    # Check dicts
    assert "legalities" in result
    assert result["legalities"]["modern"] == "legal"
    
    # Check foreign data
    assert "foreignData" in result
    assert len(result["foreignData"]) == 2


def test_show_card_with_zero_mana_value():
    """Test that show_card includes mana_value even if it's 0"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Black Lotus",
        type_line="Artifact",
        mana_cost="{0}",
        mana_value=0.0,
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    # 0.0 is falsy but should still be included
    assert "mana_value" in result
    assert result["mana_value"] == 0.0


def test_show_card_with_false_boolean():
    """Test that show_card includes boolean False values"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        is_funny=False,
        is_reserved=False,
        has_alternative_deck_limit=False,
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    
    # False is not None, so it should be included
    assert "is_funny" in result
    assert result["is_funny"] is False
    assert "is_reserved" in result
    assert result["is_reserved"] is False
    assert "has_alternative_deck_limit" in result
    assert result["has_alternative_deck_limit"] is False


# Tests for __str__

def test_str_basic_card():
    """Test __str__ with a basic card"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Lightning Bolt",
        type_line="Instant"
    )
    
    result = str(card)
    
    assert result == "Card(name=Lightning Bolt, id=1)"


def test_str_complete_card(complete_card_for_display):
    """Test __str__ with a complete card"""
    result = str(complete_card_for_display)
    
    assert result == "Card(name=Serra Angel, id=2)"


def test_str_card_with_special_characters():
    """Test __str__ with special characters in name"""
    card = Card(
        id_card=99,
        layout="normal",
        name="Ætherling",
        type_line="Creature"
    )
    
    result = str(card)
    
    assert result == "Card(name=Ætherling, id=99)"


def test_str_card_with_long_name():
    """Test __str__ with a long card name"""
    card = Card(
        id_card=42,
        layout="normal",
        name="Who // What // When // Where // Why",
        type_line="Instant"
    )
    
    result = str(card)
    
    assert result == "Card(name=Who // What // When // Where // Why, id=42)"


def test_str_card_with_quotes_in_name():
    """Test __str__ with quotes in name"""
    card = Card(
        id_card=10,
        layout="normal",
        name='Card "The Great"',
        type_line="Creature"
    )
    
    result = str(card)
    
    assert result == 'Card(name=Card "The Great", id=10)'


# Tests for __repr__

def test_repr_basic_card():
    """Test __repr__ with a basic card"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Lightning Bolt",
        type_line="Instant"
    )
    
    result = repr(card)
    
    assert result == "Card(name=Lightning Bolt, id=1)"


def test_repr_complete_card(complete_card_for_display):
    """Test __repr__ with a complete card"""
    result = repr(complete_card_for_display)
    
    assert result == "Card(name=Serra Angel, id=2)"


def test_repr_equals_str():
    """Test that __repr__ and __str__ return the same value"""
    card = Card(
        id_card=5,
        layout="normal",
        name="Test Card",
        type_line="Creature"
    )
    
    assert str(card) == repr(card)


def test_repr_equals_str_various_cards():
    """Test __repr__ == __str__ for various cards"""
    cards = [
        Card(id_card=1, layout="normal", name="A", type_line="Instant"),
        Card(id_card=999, layout="transform", name="Long Name Card", type_line="Land"),
        Card(id_card=0, layout="normal", name="Zero", type_line="Artifact"),
    ]
    
    for card in cards:
        assert str(card) == repr(card)


# More tests

def test_show_card_then_str():
    """Test that show_card and str work together"""
    card = Card(
        id_card=100,
        layout="normal",
        name="Black Lotus",
        type_line="Artifact",
        mana_cost="{0}",
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result = card.show_card()
    string_repr = str(card)
    
    assert result["id_card"] == 100
    assert result["name"] == "Black Lotus"
    assert string_repr == "Card(name=Black Lotus, id=100)"


def test_multiple_show_card_calls_consistent():
    """Test that multiple calls to show_card return consistent results"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        keywords=["Flying"],
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    result1 = card.show_card()
    result2 = card.show_card()
    
    assert result1 == result2


def test_show_card_does_not_modify_card():
    """Test that show_card doesn't modify the original card"""
    card = Card(
        id_card=1,
        layout="normal",
        name="Test",
        type_line="Instant",
        mana_value=3.0,
        color_identity=[],
        color_indicator=[],
        colors=[]
    )
    
    original_mana = card.mana_value
    _ = card.show_card()
    
    assert card.mana_value == original_mana


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
