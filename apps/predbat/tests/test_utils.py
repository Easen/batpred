from utils import time_to_minutes


def test_time_to_minutes():
    """HH:MM:SS strings convert to minutes since midnight; garbage converts to 0."""
    assert time_to_minutes("00:00:00") == 0
    assert time_to_minutes("05:30:00") == 330
    assert time_to_minutes("23:59:00") == 1439
    assert time_to_minutes("garbage") == 0


def run_utils_tests(my_predbat=None):
    """Run all Utils tests (registry entry point).

    Args:
        my_predbat: The shared Predbat fixture from unit_test.py, used by the registry resolution test; None when run standalone, which skips that test.
    """
    test_time_to_minutes()
