"""Pytest regression tests for ConversationManager edge cases.

These tests focus on the previously buggy areas so that future
changes cannot re-introduce them.  We bypass Streamlit runtime
by monkey-patching a minimal mock module.
"""

from types import ModuleType
import sys
import pytest

# ---------------------------------------------------------------------------
# Provide a minimal mock for the `streamlit` module so that ConversationManager
# can import and use st.session_state in a pure-python environment.
# ---------------------------------------------------------------------------
mock_st = ModuleType("streamlit")

class _MockSessionState(dict):
    """Dict subclass that also allows attribute-style access."""
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)
    def __setattr__(self, key, value):
        self[key] = value

mock_st.session_state = _MockSessionState()

def _reset_session_state():
    """Utility to reset the in-memory session state between tests."""
    mock_st.session_state = _MockSessionState()

sys.modules["streamlit"] = mock_st  # Inject before ConversationManager import

# ---------------------------------------------------------------------------
# Now we can import the application code
# ---------------------------------------------------------------------------
from src.chatbot.conversation_manager import ConversationManager
from src.config.settings import AppConfig, ConversationState

# Provide a lightweight test config.  Only the mandatory fields are supplied.
TEST_CONFIG = AppConfig(
    groq_api_key="dummy",
    google_sheet_id="dummy",
    google_service_account_json="{}",
    secret_key="dummy",
    encryption_key="dummy",
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def clean_state():
    """Ensure Streamlit session state is clean before every test."""
    _reset_session_state()
    yield
    _reset_session_state()

@pytest.fixture()
def cm():
    """Provide a fresh ConversationManager instance for each test."""
    return ConversationManager(TEST_CONFIG)

# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_is_dont_know_detection(cm):
    """`_is_dont_know_response` should flag only genuine 'don't know' inputs."""
    assert cm._is_dont_know_response("I dont know") is True
    assert cm._is_dont_know_response("idk") is True
    # Should NOT trigger on legitimate words containing 'na'
    assert cm._is_dont_know_response("analyst") is False
    # Random valid sentence
    assert cm._is_dont_know_response("Worked as analyst") is False


def _prepare_work_experience_state(cm):
    """Helper to place the session in the work-experience question state."""
    session = cm.get_session()
    session.current_state = ConversationState.INFO_COLLECTION
    # Candidate info stored as a simple mutable dict during collection stage
    session.candidate_info = {
        "experience_years": 2,
        "current_field": "work_experience_description",
    }
    return session


def test_valid_work_experience_is_accepted(cm):
    """A sensible work-experience answer should advance to next field."""
    session = _prepare_work_experience_state(cm)
    prompt = (
        "Worked as a Data Analyst at PGAGI Technologies for 2 years, "
        "focusing on data cleaning, visualization and deriving insights."
    )
    response = cm._handle_info_collection(prompt)

    assert "Thank you for sharing" in response
    assert session.candidate_info["current_field"] == "why_good_candidate"


def test_dont_know_rejected_for_work_experience(cm):
    """'I don't know' is not acceptable for mandatory work-experience field."""
    session = _prepare_work_experience_state(cm)
    response = cm._handle_info_collection("I don't know")

    assert "This information is **required**" in response
    # Field should remain unchanged (still asking for work experience)
    assert session.candidate_info["current_field"] == "work_experience_description"
