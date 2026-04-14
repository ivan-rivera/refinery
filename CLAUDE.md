# Project Rules

## General
- Do not modify unrelated files
- Respect existing project structure and patterns
- Avoid overengineering MVP features

## Python Style (applies to *.py files)
- Follow the Google Python Style Guide
- Use "double quotes" for strings
- Prefer explicit imports
- Keep functions short and composable
- Avoid magic numbers — put constants in `src/config/constants.py`
- Prefer small, surgical changes over large rewrites

## Testing (applies to tests/*.py)
- Use pytest for testing, NEVER use unittest or import from it
- Write tests for new functionality
- Write the shortest, most minimalist tests possible that cover core functionality
- Use coverage.py to track test coverage
- Use pytest-cov to report test coverage
- Use pytest-mock to mock dependencies
