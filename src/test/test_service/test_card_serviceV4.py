import sys
import os
import pytest
from unittest.mock import MagicMock, patch, Mock
import re

# Imports des classes nécessaires
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from business_object.card import Card
from business_object.filters.abstract_filter import AbstractFilter
from service.card_service import CardService
from dao.card_dao import CardDao


# ========== FIXTURES ==========

@pytest.fixture
def mock_card():
    """Fixture pour créer une carte de test"""
    return Card(
        ascii_name="Test Card",
        color_identity=["R", "U"],
        color_indicator=[],
        colors=["R", "U"],
        converted_mana_cost=3.0,
        edhrec_rank=100,
        name="Test Card",
        mana_cost="{2}{R}",
        mana_value=3.0,
        power="3",
        toughness="3",
        text="Test card text",
        type_line="Creature - Test"
    )


@pytest.fixture
def mock_filter_cat():
    """Fixture pour un filtre catégoriel"""
    filter_mock = Mock(spec=AbstractFilter)
    filter_mock.variable_filtered = "type"
    filter_mock.type_of_filtering = "positive"
    filter_mock.filtering_value = "Creature"
    return filter_mock


@pytest.fixture
def mock_filter_num():
    """Fixture pour un filtre numérique"""
    filter_mock = Mock(spec=AbstractFilter)
    filter_mock.variable_filtered = "manaValue"
    filter_mock.type_of_filtering = "higher_than"
    filter_mock.filtering_value = 5
    return filter_mock


# ========== TESTS ID_SEARCH ==========

class TestIdSearch:
    """Tests pour la méthode id_search"""

    def test_id_search_success(self, mock_card):
        """Test de recherche par ID avec succès"""
        # GIVEN
        card_id = 42
        with patch.object(CardDao, 'id_search', return_value=mock_card) as mock_dao:
            # WHEN
            service = CardService()
            result = service.id_search(card_id)
            
            # THEN
            mock_dao.assert_called_once_with(card_id)
            assert result == mock_card
            assert result.name == "Test Card"

    def test_id_search_not_found(self):
        """Test de recherche par ID non trouvé"""
        # GIVEN
        card_id = 999999
        with patch.object(CardDao, 'id_search', return_value=None) as mock_dao:
            # WHEN
            service = CardService()
            result = service.id_search(card_id)
            
            # THEN
            mock_dao.assert_called_once_with(card_id)
            assert result is None

    def test_id_search_invalid_type(self):
        """Test de recherche avec un type invalide"""
        # GIVEN
        invalid_id = "not_an_int"
        
        # WHEN / THEN
        with pytest.raises(TypeError):
            card_service = CardService()
            card_service.id_search(invalid_id)


# ========== TESTS NAME_SEARCH ==========

class TestNameSearch:
    """Tests pour la méthode name_search"""

    def test_name_search_success(self, mock_card):
        """Test de recherche par nom avec succès"""
        # GIVEN
        card_name = "Test Card"
        with patch.object(CardDao, 'name_search', return_value=mock_card) as mock_dao:
            # WHEN
            service = CardService()
            result = service.id_search(card_name)
            
            # THEN
            mock_dao.assert_called_once_with(card_name)
            assert result == mock_card
            assert result.name == card_name

    def test_name_search_not_found(self):
        """Test de recherche par nom non trouvé"""
        # GIVEN
        card_name = "Nonexistent Card"
        with patch.object(CardDao, 'name_search', return_value=None) as mock_dao:
            # WHEN
            service = CardService()
            result = service.name_search(card_name)
            
            # THEN
            mock_dao.assert_called_once_with(card_name)
            assert result is None

    def test_name_search_partial_match(self, mock_card):
        """Test de recherche avec correspondance partielle"""
        # GIVEN
        partial_name = "Test"
        with patch.object(CardDao, 'name_search', return_value=mock_card) as mock_dao:
            # WHEN
            service = CardService()
            result = service.name_search(partial_name)
            
            # THEN
            mock_dao.assert_called_once_with(partial_name)
            assert result is not None


# ========== TESTS SEMANTIC_SEARCH ==========

class TestSemanticSearch:
    """Tests pour la méthode semantic_search"""

    @patch('service.card_service.requests.post')
    @patch('service.card_service.conn')
    def test_semantic_search_success(self, mock_conn, mock_post):
        """Test de recherche sémantique avec succès"""
        # GIVEN
        search_query = "red flying creature"
        mock_embedding_response = {
            "embeddings": [[0.1, 0.2, 0.3]]
        }
        mock_post.return_value.json.return_value = mock_embedding_response
        
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("embed1", 0.1),
            ("embed2", 0.2),
            ("embed3", 0.3)
        ]
        mock_conn.execute.return_value = mock_cursor
        
        # WHEN
        service = CardService()
        result = service.semantic_search(search_query)
        
        # THEN
        mock_post.assert_called_once()
        assert len(result) == 3
        assert result[0][1] == 0.1  # distance la plus faible

    @patch('service.card_service.requests.post')
    def test_semantic_search_api_error(self, mock_post):
        """Test avec erreur API lors de l'embedding"""
        # GIVEN
        search_query = "test query"
        mock_post.side_effect = Exception("API Error")
        
        # WHEN / THEN
        with pytest.raises(Exception):
            card_service = CardService()
            card_service.semantic_search(search_query)

    @patch('service.card_service.requests.post')
    @patch('service.card_service.conn')
    def test_semantic_search_empty_results(self, mock_conn, mock_post):
        """Test avec aucun résultat"""
        # GIVEN
        search_query = "very specific nonexistent card"
        mock_embedding_response = {
            "embeddings": [[0.1, 0.2, 0.3]]
        }
        mock_post.return_value.json.return_value = mock_embedding_response
        
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.execute.return_value = mock_cursor
        
        # WHEN
        service = CardService()
        result = service.semantic_search(search_query)
        
        # THEN
        assert result == []


# ========== TESTS VIEW_RANDOM_CARD ==========

class TestViewRandomCard:
    """Tests pour la méthode view_random_card"""

    @patch('service.card_service.random.randint')
    @patch.object(CardDao, 'get_highest_id')
    @patch.object(CardService, 'id_search')
    def test_view_random_card_success(self, mock_id_search, mock_highest_id, mock_randint, mock_card):
        """Test d'affichage d'une carte aléatoire"""
        # GIVEN
        mock_highest_id.return_value = 1000
        mock_randint.return_value = 42
        mock_id_search.return_value = mock_card
        
        # WHEN
        service = CardService()
        result = service.view_random_card()
        
        # THEN
        mock_highest_id.assert_called_once()
        mock_randint.assert_called_once_with(0, 1000)
        mock_id_search.assert_called_once_with(42)

    @patch('service.card_service.random.randint')
    @patch.object(CardDao, 'get_highest_id')
    def test_view_random_card_no_cards(self, mock_highest_id, mock_randint):
        """Test quand il n'y a pas de cartes"""
        # GIVEN
        mock_highest_id.return_value = 0
        
        # WHEN
        card_service = CardService()
        card_service.view_random_card()
        
        # THEN
        mock_randint.assert_called_once_with(0, 0)


# ========== TESTS FILTER_CAT_SERVICE ==========

class TestFilterCatService:
    """Tests pour la méthode filter_cat_service"""

    def test_filter_cat_service_valid_positive(self, mock_filter_cat):
        """Test de filtre catégoriel positif valide"""
        # GIVEN
        card_service = CardService()
        with patch.object(CardDao, 'filter_cat_dao', return_value=[]) as mock_dao:
            # WHEN
            result = card_service.filter_cat_service(mock_filter_cat)
            
            # THEN
            mock_dao.assert_called_once_with(mock_filter_cat)

    def test_filter_cat_service_invalid_variable(self):
        """Test avec variable invalide"""
        # GIVEN
        card_service = CardService()
        filter_mock = Mock(spec=AbstractFilter)
        filter_mock.variable_filtered = "invalid_variable"
        filter_mock.type_of_filtering = "positive"
        filter_mock.filtering_value = "test"
        
        # WHEN / THEN
        with pytest.raises(ValueError, match="variable_filtered must be in the following list : type"):
            card_service.filter_cat_service(filter_mock)

    def test_filter_cat_service_invalid_filtering_type(self):
        """Test avec type de filtrage invalide"""
        # GIVEN
        card_service = CardService()
        filter_mock = Mock(spec=AbstractFilter)
        filter_mock.variable_filtered = "type"
        filter_mock.type_of_filtering = "invalid_type"
        filter_mock.filtering_value = "test"
        
        # WHEN / THEN
        with pytest.raises(ValueError, match="type_of_filtering can only take 'positive' or 'negative' as input"):
            card_service.filter_cat_service(filter_mock)

    def test_filter_cat_service_invalid_value_type(self):
        """Test avec type de valeur invalide"""
        # GIVEN
        card_service = CardService()
        filter_mock = Mock(spec=AbstractFilter)
        filter_mock.variable_filtered = "type"
        filter_mock.type_of_filtering = "positive"
        filter_mock.filtering_value = 123  # Should be string
        
        # WHEN / THEN
        with pytest.raises(ValueError, match="filtering_value must be a string"):
            card_service.filter_cat_service(filter_mock)

    def test_filter_cat_service_negative_filter(self):
        """Test de filtre négatif"""
        # GIVEN
        card_service = CardService()
        filter_mock = Mock(spec=AbstractFilter)
        filter_mock.variable_filtered = "type"
        filter_mock.type_of_filtering = "negative"
        filter_mock.filtering_value = "Creature"
        
        with patch.object(CardDao, 'filter_cat_dao', return_value=[]) as mock_dao:
            # WHEN
            result = card_service.filter_cat_service(filter_mock)
            
            # THEN
            mock_dao.assert_called_once()


# ========== TESTS FILTER_NUM_SERVICE ==========

class TestFilterNumService:
    """Tests pour la méthode filter_num_service"""

    def test_filter_num_service_valid_higher_than(self, mock_filter_num):
        """Test de filtre numérique 'higher_than' valide"""
        # GIVEN
        card_service = CardService()
        with patch.object(CardDao, 'filter_num_dao', return_value=[]) as mock_dao:
            # WHEN
            result = card_service.filter_num_service(mock_filter_num)
            
            # THEN
            mock_dao.assert_called_once_with(mock_filter_num)

    def test_filter_num_service_invalid_variable(self):
        """Test avec variable invalide"""
        # GIVEN
        card_service = CardService()
        filter_mock = Mock(spec=AbstractFilter)
        filter_mock.variable_filtered = "invalid_variable"
        filter_mock.type_of_filtering = "higher_than"
        filter_mock.filtering_value = 5
        
        # WHEN / THEN
        with pytest.raises(ValueError, match="variable_filtered must be in the following list"):
            card_service.filter_num_service(filter_mock)

    def test_filter_num_service_invalid_type(self):
        """Test avec type de filtrage invalide"""
        # GIVEN
        card_service = CardService()
        filter_mock = Mock(spec=AbstractFilter)
        filter_mock.variable_filtered = "manaValue"
        filter_mock.type_of_filtering = "invalid_type"
        filter_mock.filtering_value = 5
        
        # WHEN / THEN
        with pytest.raises(ValueError, match="type_of_filtering can only take"):
            card_service.filter_num_service(filter_mock)

    @pytest.mark.parametrize(
        "variable,type_filter,value",
        [
            ("manaValue", "higher_than", 5),
            ("defense", "lower_than", 3),
            ("edhrecRank", "equal_to", 100),
            ("toughness", "higher_than", 2),
            ("power", "lower_than", 10),
        ]
    )
    def test_filter_num_service_all_valid_combinations(self, variable, type_filter, value):
        """Test de toutes les combinaisons valides"""
        # GIVEN
        card_service = CardService()
        filter_mock = Mock(spec=AbstractFilter)
        filter_mock.variable_filtered = variable
        filter_mock.type_of_filtering = type_filter
        filter_mock.filtering_value = value
        
        with patch.object(CardDao, 'filter_num_dao', return_value=[]) as mock_dao:
            # WHEN
            result = card_service.filter_num_service(filter_mock)
            
            # THEN
            mock_dao.assert_called_once()


# ========== TESTS D'INTÉGRATION ==========

class TestIntegration:
    """Tests d'intégration pour vérifier l'interaction entre les méthodes"""

    @patch.object(CardDao, 'id_search')
    @patch.object(CardDao, 'name_search')
    def test_search_consistency(self, mock_name_search, mock_id_search, mock_card):
        """Test de cohérence entre recherche par ID et par nom"""
        # GIVEN
        mock_id_search.return_value = mock_card
        mock_name_search.return_value = mock_card
        
        # WHEN
        card_service = CardService()
        result_by_id = card_service.id_search(1)
        result_by_name = card_service.name_search("Test Card")
        
        # THEN
        assert result_by_id.name == result_by_name.name

    @patch.object(CardDao, 'filter_cat_dao')
    @patch.object(CardDao, 'filter_num_dao')
    def test_combined_filters(self, mock_num_dao, mock_cat_dao):
        """Test de combinaison de filtres"""
        # GIVEN
        card_service = CardService()
        cat_filter = Mock(spec=AbstractFilter)
        cat_filter.variable_filtered = "type"
        cat_filter.type_of_filtering = "positive"
        cat_filter.filtering_value = "Creature"
        
        num_filter = Mock(spec=AbstractFilter)
        num_filter.variable_filtered = "manaValue"
        num_filter.type_of_filtering = "lower_than"
        num_filter.filtering_value = 4
        
        mock_cat_dao.return_value = []
        mock_num_dao.return_value = []
        
        # WHEN
        cat_result = card_service.filter_cat_service(cat_filter)
        num_result = card_service.filter_num_service(num_filter)
        
        # THEN
        mock_cat_dao.assert_called_once()
        mock_num_dao.assert_called_once()


# ========== TESTS DE PERFORMANCE ==========

class TestPerformance:
    """Tests de performance (optionnels mais recommandés)"""

    @patch('service.card_service.requests.post')
    @patch('service.card_service.conn')
    def test_semantic_search_response_time(self, mock_conn, mock_post):
        """Test que la recherche sémantique répond en temps raisonnable"""
        import time
        
        # GIVEN
        mock_embedding_response = {"embeddings": [[0.1] * 1024]}
        mock_post.return_value.json.return_value = mock_embedding_response
        
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(f"embed{i}", i*0.1) for i in range(5)]
        mock_conn.execute.return_value = mock_cursor
        
        # WHEN
        start = time.time()
        card_service = CardService()
        card_service.semantic_search("test query")
        elapsed = time.time() - start
        
        # THEN
        assert elapsed < 1.0  # Should complete in less than 1 second


# ========== TESTS PARAMÉTRÉS ==========

@pytest.mark.parametrize(
    "params,error,error_message",
    [
        (
            {"variable_filtered": "toughness", "type_of_filtering": "positive", "filtering_value": "Creature"},
            ValueError,
            "variable_filtered must be in the following list : type"
        ),
        (
            {"variable_filtered": "type", "type_of_filtering": "random", "filtering_value": "Creature"},
            ValueError,
            "type_of_filtering can only take 'positive' or 'negative' as input"
        ),
        (
            {"variable_filtered": "type", "type_of_filtering": "positive", "filtering_value": 9},
            ValueError,
            "filtering_value must be a string"
        )
    ]
)
def test_filter_cat_service_parametrized(params, error, error_message):
    """Tests paramétrés pour filter_cat_service"""
    card_service = CardService()
    filter_mock = Mock(spec=AbstractFilter)
    filter_mock.variable_filtered = params["variable_filtered"]
    filter_mock.type_of_filtering = params["type_of_filtering"]
    filter_mock.filtering_value = params["filtering_value"]
    
    with pytest.raises(error, match=re.escape(error_message)):
        card_service.filter_cat_service(filter_mock)


@pytest.mark.parametrize(
    "params,error,error_message",
    [
        (
            {"variable_filtered": "type", "type_of_filtering": "equal_to", "filtering_value": 9},
            ValueError,
            "variable_filtered must be in the following list : manaValue, defense, edhrecRank, toughness, power"
        ),
        (
            {"variable_filtered": "power", "type_of_filtering": "positive", "filtering_value": 9},
            ValueError,
            "type_of_filtering can only take 'higher_than', 'lower_than' or 'equal_to' as input"
        )
    ]
)
def test_filter_num_service_parametrized(params, error, error_message):
    """Tests paramétrés pour filter_num_service"""
    card_service = CardService()
    filter_mock = Mock(spec=AbstractFilter)
    filter_mock.variable_filtered = params["variable_filtered"]
    filter_mock.type_of_filtering = params["type_of_filtering"]
    filter_mock.filtering_value = params["filtering_value"]
    
    with pytest.raises(error, match=re.escape(error_message)):
        card_service.filter_num_service(filter_mock)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])