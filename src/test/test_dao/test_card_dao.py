import unittest
from unittest.mock import Mock, patch, MagicMock
from dao.card_dao import CardDao


class TestFilterDAO(unittest.TestCase):

    def setUp(self):
        """Initialisation before each test"""
        self.card_dao = CardDao()

    def _setup_mocks(self, mock_db_connection_class):
        """Helper to configure the mocks (to avoid repetitions)"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_instance = MagicMock()

        mock_db_connection_class.return_value = mock_db_instance
        mock_db_instance.connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        return mock_cursor

    @patch('dao.card_dao.DBConnection')
    def test_filter_categorical_positive_color(self, mock_db_connection_class):
        """Test of positive categorical filters on color"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'color'
        mock_filter.type_of_filtering = 'positive'
        mock_filter.filtering_value = 'B'

        mock_cursor = self._setup_mocks(mock_db_connection_class)

        fake_result = [{'idCard': 1}, {'idCard': 2}]  # because filter_dao returns ids
        mock_cursor.fetchall.return_value = fake_result

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT
        # 1. check whether the execute has been called (the SQL query was executed)
        self.assertTrue(
            mock_cursor.execute.called,
            "execute() should be called :( ")

        # 2. check that the SQL query has the right parameters :
        # variable_filtered and type_of_filtering
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])  # get the SQL query

        self.assertIn('color', sql_query.lower())  # the right column has been called
        self.assertIn('WHERE', sql_query)  # there is a WHERE

        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(
                    any('B' in str(p) for p in params),
                    "The parameter should contain the filtering_value 'B'"
                )

        # 4. check that fetchall has been called
        mock_cursor.fetchall.assert_called_once()

        # 5. check that the result is a list of ids
        self.assertEqual(result, [1, 2])
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(id, int) for id in result))

    @patch('dao.card_dao.DBConnection')
    def test_filter_categorical_negative_type(self, mock_db_connection_class):
        """Test of a negative filter on type"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'type'
        mock_filter.type_of_filtering = 'negative'
        mock_filter.filtering_value = 'Creature'

        mock_cursor = self._setup_mocks(mock_db_connection_class)

        fake_result = [{'idCard': 10}, {'idCard': 20}]
        mock_cursor.fetchall.return_value = fake_result

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT
        # 1. check whether the execute has been called (the SQL query was executed)
        self.assertTrue(mock_cursor.execute.called, "execute() should be called :( ")

        # 2. check that the SQL query has the right parameters :
        # variable_filtered and type_of_filtering
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])
        self.assertIn('type', sql_query.lower())
        self.assertIn('WHERE', sql_query)

        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(any('Creature' in str(p) for p in params),
                            "the parameter should contain the filtering_value")

        # 4. check the return
        self.assertEqual(result, [10, 20])

        # 5. check that fetchall has been called
        mock_cursor.fetchall.assert_called_once()

    @patch('dao.card_dao.DBConnection')
    def test_filter_numerical_higher_than_power(self, mock_db_connection_class):
        """Test of a numerical filter with 'higher_than' on power"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'power'
        mock_filter.type_of_filtering = 'higher_than'
        mock_filter.filtering_value = 5

        mock_cursor = self._setup_mocks(mock_db_connection_class)

        fake_result = [{'idCard': 100}]
        mock_cursor.fetchall.return_value = fake_result

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT
        # 1. check whether the execute has been called (the SQL query was executed)
        self.assertTrue(mock_cursor.execute.called, "execute() should be called :( ")

        # 2. check that the SQL query has the right parameters :
        # variable_filtered and type_of_filtering
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])
        self.assertIn('power', sql_query.lower())
        self.assertIn('WHERE', sql_query)

        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(any('5' in str(p) for p in params),
                            "the parameter should contain the filtering_value")

        # 4. check the return
        self.assertEqual(result, [100])

        # 5. check that fetchall has been called
        mock_cursor.fetchall.assert_called_once()

    @patch('dao.card_dao.DBConnection')
    def test_filter_numerical_equal_to_manavalue(self, mock_db_connection_class):
        """Test of a numerical filter with "equal_to" on manaValue"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'manaValue'
        mock_filter.type_of_filtering = 'equal_to'
        mock_filter.filtering_value = 3

        mock_cursor = self._setup_mocks(mock_db_connection_class)

        # check the return
        fake_result = [{'idCard': 50}]
        mock_cursor.fetchall.return_value = fake_result

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT
        # 1. check whether the execute has been called (the SQL query was executed)
        self.assertTrue(
            mock_cursor.execute.called,
            "execute() should be called :( ")

        # 2. check that the SQL query has the right parameters :
        # variable_filtered and type_of_filtering
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])

        self.assertIn('manaValue', sql_query)
        self.assertIn('WHERE', sql_query)

        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(any('3' in str(p) for p in params),
                            "the parameter should contain the filtering_value")

        # 4. check the return
        self.assertEqual(result, [50])

        # 5. check that fetchall has been called
        mock_cursor.fetchall.assert_called_once()

    @patch('dao.card_dao.DBConnection')
    def test_filter_exception_handling(self, mock_db_connection_class):
        """Test on the way exceptions are handled"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'color'
        mock_filter.type_of_filtering = 'positive'
        mock_filter.filtering_value = 'B'

        mock_cursor = self._setup_mocks(mock_db_connection_class)

        # fake an exception
        mock_cursor.execute.side_effect = Exception("Database error")

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT - if there is a problem it returns False
        self.assertEqual(result, False)

    @patch('dao.card_dao.DBConnection')
    def test_filter_empty_result(self, mock_db_connection_class):
        """Test with an empty result"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'color'
        mock_filter.type_of_filtering = 'positive'
        mock_filter.filtering_value = 'NonExistentColor'

        mock_cursor = self._setup_mocks(mock_db_connection_class)

        # Test that fetchall returns an empty list
        mock_cursor.fetchall.return_value = []

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT - An empty result should return []
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    @patch('dao.card_dao.DBConnection')
    def test_filter_uses_parameterized_queries(self, mock_db_connection_class):
        """test that the queries use the right parameters (SQL injection)"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'color'
        mock_filter.type_of_filtering = 'positive'
        mock_filter.filtering_value = "'; DROP TABLE cards; --"  # injection input

        mock_cursor = self._setup_mocks(mock_db_connection_class)
        mock_cursor.fetchall.return_value = []

        # ACT
        result = self.card_dao.filter_dao(mock_filter)
        # result is not used but the test doesn't pass if is not there

        # ASSERT
        call_args = mock_cursor.execute.call_args

        # check that the query doesn't contain the dangerous input
        sql_query = str(call_args[0][0])

        self.assertNotIn(
            "DROP TABLE", sql_query,
            "the filtering_value must NOT be in the SQL query (injection risk)")
        # check that the parameters are used separetly
        if len(call_args[0]) > 1:
            params = call_args[0][1]
            self.assertIsNotNone(
                params,
                "The parameters should be used to avoid SQL injections")
            # Vérifier que la valeur dangereuse est dans les paramètres (pas dans la requête)
            self.assertTrue(
                any("DROP TABLE" in str(p) for p in params),
                "The dangerous value should be in parameters, not in the query"
            )

    @patch('dao.card_dao.DBConnection')
    def test_filter_numerical_lower_than_toughness(self, mock_db_connection_class):
        """Test numerical filter with 'lower_than' on toughness"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'toughness'
        mock_filter.type_of_filtering = 'lower_than'
        mock_filter.filtering_value = 2

        mock_cursor = self._setup_mocks(mock_db_connection_class)
        fake_result = [{'idCard': 5}, {'idCard': 6}, {'idCard': 7}]
        mock_cursor.fetchall.return_value = fake_result

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT
        self.assertTrue(mock_cursor.execute.called)
        self.assertEqual(result, [5, 6, 7])
        self.assertEqual(len(result), 3)

    @patch('dao.card_dao.DBConnection')
    def test_filter_returns_list_of_integers(self, mock_db_connection_class):
        """Test that filter_dao always returns a list of integers"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'manaValue'
        mock_filter.type_of_filtering = 'equal_to'
        mock_filter.filtering_value = 1

        mock_cursor = self._setup_mocks(mock_db_connection_class)
        fake_result = [{'idCard': 100}, {'idCard': 200}, {'idCard': 300}]
        mock_cursor.fetchall.return_value = fake_result

        # ACT
        result = self.card_dao.filter_dao(mock_filter)

        # ASSERT
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(id_card, int) for id_card in result))
        self.assertEqual(result, [100, 200, 300])

    @patch('dao.card_dao.DBConnection')
    def test_filter_with_none_fetchall_result(self, mock_db_connection_class):
        """Test behavior when fetchall returns None"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'color'
        mock_filter.type_of_filtering = 'positive'
        mock_filter.filtering_value = 'X'

        mock_cursor = self._setup_mocks(mock_db_connection_class)
        mock_cursor.fetchall.return_value = None

        # ACT & ASSERT
        # If fetchall returns None card["idCard"] isn't going to work
        # the method must handle the exception and return a false
        result = self.card_dao.filter_dao(mock_filter)
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
