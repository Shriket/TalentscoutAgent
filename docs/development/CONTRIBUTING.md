# 🤝 Contributing to TalentScout Hiring Assistant

We welcome contributions to TalentScout! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- **Be respectful**: Treat all community members with respect and kindness
- **Be inclusive**: Welcome newcomers and help them get started
- **Be collaborative**: Work together to improve the project
- **Be professional**: Maintain professional communication standards

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of Streamlit and AI/ML concepts
- Familiarity with GDPR compliance principles

### First-Time Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/talentscout-hiring-assistant.git
   cd talentscout-hiring-assistant
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your development API keys
   ```

## 🛠️ Development Setup

### Project Structure Understanding

```
TalentScoutAgent/
├── src/                    # Source code
│   ├── chatbot/           # Conversation logic
│   ├── config/            # Configuration and settings
│   ├── data/              # Data models and handlers
│   ├── ui/                # User interface components
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
└── main.py               # Application entry point
```

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code standards outlined below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   python -m pytest tests/
   
   # Run automated interview test
   python final_test.py
   
   # Check code quality
   flake8 src/
   black src/
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   git push origin feature/your-feature-name
   ```

## 📏 Code Standards

### Python Code Style

We follow PEP 8 with some project-specific guidelines:

#### Formatting
- Use **Black** for code formatting
- Line length: 88 characters (Black default)
- Use double quotes for strings
- Use f-strings for string formatting

#### Naming Conventions
```python
# Classes: PascalCase
class ConversationManager:
    pass

# Functions and variables: snake_case
def process_user_input():
    user_name = "John Smith"

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3

# Private methods: leading underscore
def _validate_internal_data():
    pass
```

#### Type Hints
Always use type hints for function parameters and return values:

```python
from typing import List, Dict, Optional

def validate_input(input_value: str, field_name: str) -> bool:
    """Validate user input for specific field."""
    return True

def get_candidate_data() -> Optional[Dict[str, str]]:
    """Retrieve candidate data."""
    return {"name": "John"}
```

#### Docstrings
Use Google-style docstrings:

```python
def process_user_input(self, user_input: str) -> str:
    """Process user input and generate appropriate response.
    
    Args:
        user_input: The user's text input
        
    Returns:
        Generated response message
        
    Raises:
        ValidationError: If input validation fails
    """
    pass
```

### Error Handling

Always implement proper error handling:

```python
import logging

logger = logging.getLogger(__name__)

def api_call_example():
    try:
        # API call logic
        response = make_api_call()
        return response
    except APIError as e:
        logger.error(f"API call failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/                  # Unit tests
│   ├── test_conversation_manager.py
│   ├── test_gdpr_compliance.py
│   └── test_sheets_handler.py
├── integration/           # Integration tests
│   ├── test_end_to_end_flow.py
│   └── test_api_integration.py
└── fixtures/              # Test data and fixtures
    └── sample_data.py
```

### Writing Tests

#### Unit Tests
```python
import pytest
from src.chatbot.conversation_manager import ConversationManager

class TestConversationManager:
    def setup_method(self):
        """Setup test fixtures before each test method."""
        self.manager = ConversationManager(mock_session_state)
    
    def test_input_validation_valid_name(self):
        """Test that valid full names pass validation."""
        result = self.manager.validate_input("John Smith", "full_name")
        assert result is True
    
    def test_input_validation_invalid_name(self):
        """Test that invalid names fail validation."""
        result = self.manager.validate_input("J", "full_name")
        assert result is False
```

#### Integration Tests
```python
def test_complete_interview_flow():
    """Test complete interview from greeting to completion."""
    # Test implementation
    pass
```

### Test Coverage

Maintain minimum 80% test coverage:

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m pytest tests/
coverage report
coverage html  # Generate HTML report
```

## 📚 Documentation

### Code Documentation

- **Docstrings**: All public functions and classes must have docstrings
- **Comments**: Use comments to explain complex logic
- **Type hints**: Always include type hints

### README Updates

When adding new features, update relevant sections in:
- `README.md`: Main project documentation
- `API_DOCUMENTATION.md`: API reference
- `TECHNICAL_DOCUMENTATION.md`: Technical details

### Changelog

Update `CHANGELOG.md` with your changes:

```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description
```

## 🐛 Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.9.7]
- TalentScout version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

### Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Any other relevant information
```

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure tests pass**
   ```bash
   python -m pytest tests/
   python final_test.py
   ```

2. **Check code quality**
   ```bash
   flake8 src/
   black --check src/
   mypy src/
   ```

3. **Update documentation**
   - Update relevant documentation files
   - Add docstrings to new functions
   - Update API documentation if needed

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Integration tests updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. **Automated checks**: All CI checks must pass
2. **Code review**: At least one maintainer review required
3. **Testing**: Manual testing of new features
4. **Documentation**: Verify documentation is complete

## 🏷️ Commit Message Guidelines

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(conversation): add support for multiple languages
fix(gdpr): resolve encryption key rotation issue
docs(api): update API documentation for new endpoints
test(integration): add end-to-end interview flow test
```

## 🌟 Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project documentation

## 📞 Getting Help

- **Discord**: [Project Discord Server]
- **GitHub Discussions**: Use for questions and discussions
- **Email**: [maintainer-email@example.com]

## 📝 License

By contributing to TalentScout, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing to TalentScout! Your efforts help make AI-powered hiring more accessible and effective for everyone. 🚀
