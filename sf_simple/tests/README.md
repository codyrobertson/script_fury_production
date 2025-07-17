# sf_simple Testing Suite

This directory contains comprehensive unit, integration, and end-to-end tests for the sf_simple application.

## Test Structure

```
tests/
├── unit/                   # Unit tests for individual modules
│   ├── test_text_extractor.py
│   ├── test_scene_analyzer.py
│   ├── test_storyboard_generator.py
│   └── test_print_generator.py
├── integration/            # Integration tests for Flask app
│   └── test_app.py
├── e2e/                   # End-to-end workflow tests
│   └── test_end_to_end.py
├── fixtures/              # Test data and sample files
│   ├── sample_screenplay.txt
│   ├── large_screenplay.txt
│   └── malformed_screenplay.txt
├── test_config.py         # Test configuration and utilities
└── README.md             # This file
```

## Running Tests

### Using the Test Runner

The recommended way to run tests is using the provided test runner:

```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py --type unit

# Run only integration tests
python run_tests.py --type integration

# Run with coverage reporting
python run_tests.py --coverage

# Run specific test
python run_tests.py --test tests.unit.test_text_extractor.TestTextExtractor.test_extract_plain_text_success

# List all available tests
python run_tests.py --list

# Run with minimal output
python run_tests.py --verbosity 1

# Stop on first failure
python run_tests.py --failfast
```

### Using unittest directly

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test module
python -m unittest tests.unit.test_text_extractor -v

# Run specific test class
python -m unittest tests.unit.test_text_extractor.TestTextExtractor -v

# Run specific test method
python -m unittest tests.unit.test_text_extractor.TestTextExtractor.test_extract_plain_text_success -v
```

### Using pytest (if installed)

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=utils --cov=app

# Run specific test file
pytest tests/unit/test_text_extractor.py -v

# Run with detailed output
pytest tests/ -v -s
```

## Test Categories

### Unit Tests

Test individual utility modules in isolation:

- **test_text_extractor.py**: Tests for PDF and text file extraction
- **test_scene_analyzer.py**: Tests for screenplay parsing and scene analysis
- **test_storyboard_generator.py**: Tests for frame generation and statistics
- **test_print_generator.py**: Tests for print HTML generation

### Integration Tests

Test Flask application endpoints and workflows:

- **test_app.py**: Tests for all Flask routes and complete workflows
- Tests file upload, analysis, generation, and print functionality
- Tests error handling and edge cases

### End-to-End Tests

Test complete user workflows:

- **test_end_to_end.py**: Full workflow tests from upload to print
- Performance tests with large files
- Multi-project handling
- Error recovery scenarios

## Test Data

### Fixtures

Test fixtures are stored in `tests/fixtures/`:

- **sample_screenplay.txt**: Well-formatted screenplay for standard tests
- **large_screenplay.txt**: Larger screenplay for performance testing
- **malformed_screenplay.txt**: Poorly formatted text for edge case testing

### Mock Data

The `MockDataGenerator` class in `test_config.py` provides:

- Dynamic screenplay generation with configurable scenes and characters
- Mock frame data for testing storyboard generation
- Mock analysis data for testing various scenarios

## Test Configuration

### TestConfig Class

Provides centralized configuration for tests:

- Test directory paths
- Sample data constants
- Default test values

### TestUtilities Class

Provides utility functions for tests:

- Temporary file creation and cleanup
- Mock object creation
- Path management

### BaseTestCase Class

Base class for test cases with common setup:

- Automatic cleanup of temporary files
- Common assertion methods
- Project path management

## Coverage Reporting

Run tests with coverage to see code coverage:

```bash
# Run with coverage
python run_tests.py --coverage

# View HTML report
open coverage_html/index.html
```

Expected coverage targets:
- Unit tests: >90% coverage of utility modules
- Integration tests: >80% coverage of Flask routes
- Overall: >85% combined coverage

## Test Best Practices

### Writing Tests

1. **Use descriptive test names**: `test_extract_plain_text_with_encoding`
2. **Test both success and failure cases**
3. **Use setUp() and tearDown() for cleanup**
4. **Mock external dependencies**
5. **Test edge cases and error conditions**

### Test Data

1. **Use fixtures for consistent test data**
2. **Create temporary files for file operations**
3. **Clean up resources in tearDown()**
4. **Use MockDataGenerator for dynamic data**

### Assertions

1. **Use specific assertions**: `assertEqual`, `assertIn`, `assertGreater`
2. **Check both content and structure**
3. **Verify error conditions**
4. **Test return values and side effects**

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure project root is in Python path
2. **File not found**: Check fixture file paths
3. **Permission errors**: Ensure test directories are writable
4. **Mock failures**: Verify mock patches match actual code

### Debug Mode

Add debugging to tests:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use print statements
def test_something(self):
    print(f"Testing with data: {test_data}")
    result = function_under_test(test_data)
    print(f"Result: {result}")
    self.assertEqual(result, expected)
```

### Test Isolation

Ensure tests are isolated:

```python
def setUp(self):
    # Clear global state
    projects.clear()
    generation_status.clear()
    
def tearDown(self):
    # Clean up resources
    for temp_file in self.temp_files:
        os.unlink(temp_file)
```

## Continuous Integration

For CI/CD pipelines, run tests with:

```bash
# Exit with non-zero code on failure
python run_tests.py --failfast

# Generate XML report for CI
python -m pytest tests/ --junit-xml=test-results.xml

# Run with coverage for CI
python run_tests.py --coverage --type all
```

## Contributing

When adding new features:

1. Write unit tests for new utility functions
2. Add integration tests for new Flask routes
3. Update e2e tests for new workflows
4. Ensure >85% code coverage
5. Run all tests before submitting

## Performance Testing

Performance benchmarks are included in e2e tests:

- Upload time: < 5 seconds for large files
- Analysis time: < 10 seconds for large screenplays
- Memory usage: Monitor during large file processing

Run performance tests:

```bash
python run_tests.py --test tests.e2e.test_end_to_end.TestEndToEndWorkflow.test_performance_with_large_content
```