import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from unittest.mock import Mock, patch, MagicMock
from psycopg2 import sql
from dao.card_dao import CardDao
from db_connection import DBConnection


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
        
        # associate a fake result with the mock
        fake_result = [('card1',), ('card2',)]
        mock_cursor.fetchall.return_value = fake_result
        
        # ACT
        result = self.card_dao.filter_dao(mock_filter)
        
        # ASSERT (doesn't depend on the real values returned by the database)
        # 1. check wether the execute has been called (the SQL query was executed)
        self.assertTrue(mock_cursor.execute.called, 
                    "execute() should be called :( ")
    
        # 2. check that the SQL query has the right parameters : variable_filtered and type_of_filtering
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])  # get the SQL query
        
        self.assertIn('color', sql_query.lower())  # the right column has been called
        self.assertIn('WHERE', sql_query)  #  there is a WHERE
        
        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(
                    any('B' in str(p) for p in params),
                    "The parameter should contain the filtering_value 'B'"
                )
        
        # 4. check that fetchall has been called
        mock_cursor.fetchall.assert_called_once()   

        # 5. check that the mock returns the right false result
        self.assertEqual(result, mock_cursor.fetchall.return_value)
        

    @patch('dao.card_dao.DBConnection')
    def test_filter_categorical_negative_type(self, mock_db_connection_class):
        """Test of a negative filter on type"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'type'
        mock_filter.type_of_filtering = 'negative'
        mock_filter.filtering_value = 'Creature'
        
        mock_cursor = self._setup_mocks(mock_db_connection_class)
        fake_result = [('card1'), ('card2')]
        mock_cursor.fetchall.return_value = fake_result
        
        # ACT
        result = self.card_dao.filter_dao(mock_filter)
        
        # ASSERT
        # 1. check whether the execute has been called (the SQL query was executed)
        self.assertTrue(mock_cursor.execute.called, "execute() should be called :( ")
        
        # 2. check that the SQL query has the right parameters : variable_filtered and type_of_filtering
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])
        self.assertIn('type', sql_query.lower())
        self.assertIn('WHERE', sql_query)
        
        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(any('Creature' in str(p) for p in params),
                            "the parameter should contain the filtering_value")
        
        # 4. check that the mock returns the right false result
        self.assertEqual(result, fake_result)
        
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
        fake_result = [('card')]
        mock_cursor.fetchall.return_value = fake_result
        
        # ACT
        result = self.card_dao.filter_dao(mock_filter)
        
        # ASSERT
        # 1. check wether the execute has been called (the SQL query was executed)
        self.assertTrue(mock_cursor.execute.called, "execute() should be called :( ")
        
        # 2. check that the SQL query has the right parameters : variable_filtered and type_of_filtering
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])
        self.assertIn('power', sql_query.lower())
        self.assertIn('WHERE', sql_query)
        
        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(any('5' in str(p) for p in params),
                            "the parameter should contain the filtering_value")
        
        # 4. check that the mock returns the right false result
        self.assertEqual(result, fake_result)
        
        # 5.  check that fetchall has been called
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
        fake_result = [('card1')]
        mock_cursor.fetchall.return_value = fake_result
        
        # ACT
        result = self.card_dao.filter_dao(mock_filter)
        
        # ASSERT
        # 1. check wether the execute has been called (the SQL query was executed)
        self.assertTrue(mock_cursor.execute.called, 
                    "execute() should be called :( ")

        # 2. check that the SQL query has the right parameters : variable_filtered and type_of_filtering            
        call_args = mock_cursor.execute.call_args
        sql_query = str(call_args[0][0])
        
        self.assertIn('manaValue', sql_query)
        self.assertIn('WHERE', sql_query)
        
        # 3. check that the SQL query has the right parameters : filtered_value
        params = call_args[0][1] if len(call_args[0]) > 1 else None
        if params:
            self.assertTrue(any('3' in str(p) for p in params),
                            "the parameter should contain the filtering_value")
        
        # 4. check that fetchall has been called
        self.assertEqual(result, fake_result)
        mock_cursor.fetchall.assert_called_once()

        # 5. check that the mock returns the right false result
        self.assertEqual(result, mock_cursor.fetchall.return_value)
        
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
        
        # ACT & ASSERT
        
        result = self.card_dao.filter_dao(mock_filter)
        self.assertEqual(result, False)
        
        
    @patch('dao.card_dao.DBConnection')
    def test_filter_empty_result(self, mock_db_connection_class):
        """Test with a null result (None vs [])"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'color'
        mock_filter.type_of_filtering = 'positive'
        mock_filter.filtering_value = 'NonExistentColor'
        
        mock_cursor = self._setup_mocks(mock_db_connection_class)
        
        # Tester when fetchall returns None
        mock_cursor.fetchall.return_value = None
        
        # ACT
        result = self.card_dao.filter_dao(mock_filter)
        
        # ASSERT 
        self.assertEqual(result, [], 
                        "a none result should be turned to a []")
    
    @patch('dao.card_dao.DBConnection')
    def test_filter_uses_parameterized_queries(self, mock_db_connection_class):
        """test that the querys use the right parameters (SQL injection)"""
        # GIVEN
        mock_filter = Mock()
        mock_filter.variable_filtered = 'name'
        mock_filter.type_of_filtering = 'positive'
        mock_filter.filtering_value = "'; DROP TABLE cards; --"  # injection tentative
        
        mock_cursor = self._setup_mocks(mock_db_connection_class)
        mock_cursor.fetchall.return_value = []
        
        # ACT
        result = self.card_dao.filter_dao(mock_filter)
        
        # ASSERT - 
        sql_query = str(call_args[0])
        
        self.assertNotIn("DROP TABLE", sql_query, 
                        "the filtering_value must NOT be in the SQL query (injection risk)")
        
    
        if len(call_args) > 1:
            params = call_args[1]
            self.assertIsNotNone(params, 
                               "The parameters should be used to avoid SQL injections")
        

if __name__ == '__main__':
    unittest.main()