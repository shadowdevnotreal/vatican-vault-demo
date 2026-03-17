"""
Sample test suite for demonstrating HTML report generation
This test suite includes various test scenarios to showcase reporting capabilities
"""

import pytest
import time
from datetime import datetime


class TestBasicFunctionality:
    """Basic functionality tests"""

    def test_addition(self):
        """Test basic addition"""
        assert 1 + 1 == 2

    def test_subtraction(self):
        """Test basic subtraction"""
        assert 5 - 3 == 2

    def test_multiplication(self):
        """Test basic multiplication"""
        assert 3 * 4 == 12

    def test_division(self):
        """Test basic division"""
        assert 10 / 2 == 5

    def test_string_operations(self):
        """Test string operations"""
        assert "hello".upper() == "HELLO"
        assert "WORLD".lower() == "world"
        assert "test".replace("t", "b") == "besb"


class TestDataStructures:
    """Data structure tests"""

    def test_list_operations(self):
        """Test list operations"""
        lst = [1, 2, 3]
        lst.append(4)
        assert len(lst) == 4
        assert lst[-1] == 4

    def test_dict_operations(self):
        """Test dictionary operations"""
        d = {"a": 1, "b": 2}
        d["c"] = 3
        assert len(d) == 3
        assert d["c"] == 3

    def test_set_operations(self):
        """Test set operations"""
        s = {1, 2, 3}
        s.add(4)
        assert 4 in s
        assert len(s) == 4


class TestTimestampGeneration:
    """Timestamp and datetime tests"""

    def test_current_timestamp(self):
        """Test current timestamp generation"""
        ts = datetime.now()
        assert isinstance(ts, datetime)
        assert ts.year >= 2024

    def test_timestamp_formatting(self):
        """Test timestamp formatting"""
        ts = datetime(2024, 1, 1, 12, 0, 0)
        formatted = ts.strftime("%Y-%m-%d %H:%M:%S")
        assert formatted == "2024-01-01 12:00:00"


class TestFileOperations:
    """File and path tests"""

    def test_path_operations(self):
        """Test path operations"""
        import os
        assert os.path.exists("/")
        assert os.path.isdir("/")

    def test_temp_directory(self):
        """Test temp directory access"""
        import tempfile
        temp_dir = tempfile.gettempdir()
        assert temp_dir is not None
        assert len(temp_dir) > 0


class TestMathOperations:
    """Mathematical operations tests"""

    def test_power(self):
        """Test power operations"""
        assert 2 ** 3 == 8
        assert 5 ** 2 == 25

    def test_modulo(self):
        """Test modulo operations"""
        assert 10 % 3 == 1
        assert 15 % 4 == 3

    def test_floor_division(self):
        """Test floor division"""
        assert 17 // 5 == 3
        assert 20 // 3 == 6


class TestBooleanLogic:
    """Boolean logic tests"""

    def test_and_operator(self):
        """Test AND operator"""
        assert True and True
        assert not (True and False)

    def test_or_operator(self):
        """Test OR operator"""
        assert True or False
        assert not (False or False)

    def test_not_operator(self):
        """Test NOT operator"""
        assert not False
        assert not (not True)


class TestExceptionHandling:
    """Exception handling tests"""

    def test_value_error_handling(self):
        """Test ValueError handling"""
        with pytest.raises(ValueError):
            int("not a number")

    def test_key_error_handling(self):
        """Test KeyError handling"""
        with pytest.raises(KeyError):
            d = {"a": 1}
            _ = d["b"]

    def test_zero_division_error(self):
        """Test ZeroDivisionError handling"""
        with pytest.raises(ZeroDivisionError):
            _ = 1 / 0


class TestPerformance:
    """Performance and timing tests"""

    def test_list_comprehension_performance(self):
        """Test list comprehension performance"""
        start = time.time()
        result = [i ** 2 for i in range(1000)]
        duration = time.time() - start
        assert len(result) == 1000
        assert duration < 1.0  # Should be very fast

    def test_string_concatenation_performance(self):
        """Test string concatenation"""
        start = time.time()
        result = "".join([str(i) for i in range(100)])
        duration = time.time() - start
        assert len(result) > 0
        assert duration < 1.0


@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
    (5, 10),
])
def test_parametrized_double(input, expected):
    """Parametrized test for doubling numbers"""
    assert input * 2 == expected


@pytest.mark.parametrize("text,length", [
    ("hello", 5),
    ("world", 5),
    ("test", 4),
    ("pytest", 6),
])
def test_parametrized_string_length(text, length):
    """Parametrized test for string lengths"""
    assert len(text) == length
