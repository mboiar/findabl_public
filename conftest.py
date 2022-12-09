import pytest

@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pl_PL']

@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return 12345