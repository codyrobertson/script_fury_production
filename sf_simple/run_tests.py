#!/usr/bin/env python3
"""
Test runner for sf_simple application
"""

import os
import sys
import unittest
import argparse
from io import StringIO

# Add the current directory to sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestRunner:
    """Test runner with various options"""
    
    def __init__(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), 'tests')
        self.unit_test_dir = os.path.join(self.test_dir, 'unit')
        self.integration_test_dir = os.path.join(self.test_dir, 'integration')
    
    def discover_tests(self, test_type='all'):
        """Discover tests based on type"""
        if test_type == 'unit':
            return unittest.TestLoader().discover(self.unit_test_dir, pattern='test_*.py')
        elif test_type == 'integration':
            return unittest.TestLoader().discover(self.integration_test_dir, pattern='test_*.py')
        elif test_type == 'all':
            # Combine unit and integration tests
            unit_suite = unittest.TestLoader().discover(self.unit_test_dir, pattern='test_*.py')
            integration_suite = unittest.TestLoader().discover(self.integration_test_dir, pattern='test_*.py')
            
            combined_suite = unittest.TestSuite()
            combined_suite.addTest(unit_suite)
            combined_suite.addTest(integration_suite)
            
            return combined_suite
        else:
            raise ValueError(f"Unknown test type: {test_type}")
    
    def run_tests(self, test_type='all', verbosity=2, failfast=False):
        """Run tests with specified options"""
        print(f"Running {test_type} tests...")
        print(f"Test directory: {self.test_dir}")
        print("-" * 60)
        
        # Discover tests
        test_suite = self.discover_tests(test_type)
        
        # Configure test runner
        runner = unittest.TextTestRunner(
            verbosity=verbosity,
            failfast=failfast,
            stream=sys.stdout
        )
        
        # Run tests
        result = runner.run(test_suite)
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            print(f"\nFAILURES:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if result.errors:
            print(f"\nERRORS:")
            for test, traceback in result.errors:
                print(f"  - {test}")
        
        # Return success status
        return result.wasSuccessful()
    
    def run_specific_test(self, test_name, verbosity=2):
        """Run a specific test by name"""
        print(f"Running specific test: {test_name}")
        print("-" * 60)
        
        # Try to load the specific test
        try:
            suite = unittest.TestLoader().loadTestsFromName(test_name)
            runner = unittest.TextTestRunner(verbosity=verbosity)
            result = runner.run(suite)
            return result.wasSuccessful()
        except Exception as e:
            print(f"Error loading test '{test_name}': {e}")
            return False
    
    def list_tests(self, test_type='all'):
        """List all available tests"""
        print(f"Available {test_type} tests:")
        print("-" * 60)
        
        test_suite = self.discover_tests(test_type)
        
        def extract_test_names(suite):
            test_names = []
            for test in suite:
                if hasattr(test, '_tests'):
                    test_names.extend(extract_test_names(test))
                else:
                    test_names.append(str(test))
            return test_names
        
        test_names = extract_test_names(test_suite)
        
        for test_name in sorted(test_names):
            print(f"  - {test_name}")
        
        print(f"\nTotal tests: {len(test_names)}")
    
    def run_coverage(self, test_type='all'):
        """Run tests with coverage reporting"""
        try:
            import coverage
        except ImportError:
            print("Coverage package not installed. Install with: pip install coverage")
            return False
        
        print(f"Running {test_type} tests with coverage...")
        print("-" * 60)
        
        # Start coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Run tests
        success = self.run_tests(test_type, verbosity=1)
        
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        
        print("\n" + "=" * 60)
        print("COVERAGE REPORT")
        print("=" * 60)
        
        # Generate coverage report
        cov.report()
        
        # Generate HTML report
        html_dir = os.path.join(os.path.dirname(__file__), 'coverage_html')
        cov.html_report(directory=html_dir)
        print(f"\nHTML coverage report generated: {html_dir}/index.html")
        
        return success


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Run sf_simple tests')
    parser.add_argument('--type', choices=['unit', 'integration', 'all'], 
                      default='all', help='Type of tests to run')
    parser.add_argument('--verbosity', type=int, choices=[0, 1, 2], 
                      default=2, help='Test output verbosity')
    parser.add_argument('--failfast', action='store_true', 
                      help='Stop on first failure')
    parser.add_argument('--list', action='store_true', 
                      help='List available tests')
    parser.add_argument('--coverage', action='store_true', 
                      help='Run tests with coverage reporting')
    parser.add_argument('--test', type=str, 
                      help='Run specific test by name')
    
    args = parser.parse_args()
    
    # Create test runner
    runner = TestRunner()
    
    # Handle different commands
    if args.list:
        runner.list_tests(args.type)
        return
    
    if args.test:
        success = runner.run_specific_test(args.test, args.verbosity)
    elif args.coverage:
        success = runner.run_coverage(args.type)
    else:
        success = runner.run_tests(args.type, args.verbosity, args.failfast)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()