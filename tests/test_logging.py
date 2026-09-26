import logging

import pytest

from app.logging_config import get_log_level


def test_get_log_level_accepts_standard_levels():
    assert get_log_level("debug") == logging.DEBUG


def test_get_log_level_rejects_invalid_value():
    with pytest.raises(ValueError, match="Invalid LOG_LEVEL"):
        get_log_level("verbose")
