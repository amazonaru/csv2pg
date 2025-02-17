from utils.db import generate_query_string, generate_data_pairs
import pandas as pd

class TestGenerateQueryString:
  def test_generate_query_string(self):
    data = [('column1', "'value1'"), ('column2', "'value2'")]
    table = 'test_table'
    schema = 'test_schema'
    expected_query = "INSERT INTO test_schema.test_table (column1,column2) VALUES ('value1','value2');"
    assert generate_query_string(data, table, schema) == expected_query

  def test_generate_query_string_with_special_characters(self):
    data = [('column1', "'value1'"), ('column2', "'value2'"), ('column3', "'value3, with comma'"), ('column4', "'value4 with \"quotes\"'")]
    table = 'test_table'
    schema = 'test_schema'
    expected_query = "INSERT INTO test_schema.test_table (column1,column2,column3,column4) VALUES ('value1','value2','value3, with comma','value4 with \"quotes\"');"
    assert generate_query_string(data, table, schema) == expected_query
  
  def test_generate_query_string_escape_single_quotes(self):
    data = [('column1', "'value1'"), ('column2', "'What's up?'")]
    table = 'test_table'
    schema = 'test_schema'
    expected_query = "INSERT INTO test_schema.test_table (column1,column2) VALUES ('value1','What''s up?');"
    assert generate_query_string(data, table, schema) == expected_query

  def test_generate_query_string_with_empty_data(self):
    data = []
    table = 'test_table'
    schema = 'test_schema'
    assert generate_query_string(data, table, schema) == None

  def test_generate_query_string_with_null_values(self):
    data = [('column1', "'value1'"), ('column2', 'NULL')]
    table = 'test_table'
    schema = 'test_schema'
    expected_query = "INSERT INTO test_schema.test_table (column1,column2) VALUES ('value1',NULL);"
    assert generate_query_string(data, table, schema) == expected_query

class TestGenerateDataPairs:
  def test_generate_data_pairs(self):
    row = pd.Series({'column1': 'value1', 'column2': 123, 'column3': 45.0, 'column4': None})
    selected_columns = [('column1', 'text'), ('column2', 'integer'), ('column3', 'bigint'), ('column4', 'text')]
    expected_data = [('column1', "'value1'"), ('column2', 123), ('column3', 45)]
    assert generate_data_pairs(row, selected_columns) == expected_data

  def test_generate_data_pairs_with_null_values(self):
    row = pd.Series({'column1': 'value1', 'column2': None, 'column3': 'NULL'})
    selected_columns = [('column1', 'text'), ('column2', 'integer'), ('column3', 'text')]
    expected_data = [('column1', "'value1'")]
    assert generate_data_pairs(row, selected_columns) == expected_data

  def test_generate_data_pairs_with_integer_values(self):
    row = pd.Series({'column1': 'value1', 'column2': 123, 'column3': 456.0})
    selected_columns = [('column1', 'text'), ('column2', 'integer'), ('column3', 'bigint')]
    expected_data = [('column1', "'value1'"), ('column2', 123), ('column3', 456)]
    assert generate_data_pairs(row, selected_columns) == expected_data

  def test_generate_data_pairs_with_mixed_values(self):
    row = pd.Series({'column1': 'value1', 'column2': 123, 'column3': 45.0, 'column4': 'value4'})
    selected_columns = [('column1', 'text'), ('column2', 'integer'), ('column3', 'bigint'), ('column4', 'text')]
    expected_data = [('column1', "'value1'"), ('column2', 123), ('column3', 45), ('column4', "'value4'")]
    assert generate_data_pairs(row, selected_columns) == expected_data

  def test_generate_data_pairs_with_empty_row(self):
    row = pd.Series({})
    selected_columns = [('column1', 'text'), ('column2', 'integer')]
    expected_data = []
    assert generate_data_pairs(row, selected_columns) == expected_data
