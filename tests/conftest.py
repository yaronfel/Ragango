import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True, scope="session")
def patch_supabase_create_client():
    with patch("agno_server.main.create_client", return_value=MagicMock()):
        yield
