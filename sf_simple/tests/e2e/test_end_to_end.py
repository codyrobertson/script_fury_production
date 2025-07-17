"""
End-to-end tests for sf_simple application
"""

import unittest
import json
import os
import tempfile
import sys
import time
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import app, projects, generation_status
from tests.test_config import TestConfig, TestUtilities, MockDataGenerator


class TestEndToEndWorkflow(unittest.TestCase):
    """End-to-end workflow tests"""

    def setUp(self):
        """Set up test environment"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear any existing projects and status
        projects.clear()
        generation_status.clear()
        
        # Create test utilities
        self.test_utils = TestUtilities()
        self.mock_data = MockDataGenerator()
        
        # Sample screenplays of different sizes
        self.small_screenplay = self.mock_data.generate_screenplay(scenes=2)
        self.medium_screenplay = self.mock_data.generate_screenplay(scenes=5)
        self.large_screenplay = self.mock_data.generate_screenplay(scenes=10)
        
        # Track temporary files for cleanup
        self.temp_files = []

    def tearDown(self):
        """Clean up after tests"""
        projects.clear()
        generation_status.clear()
        
        # Clean up temporary files
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except OSError:
                pass

    def create_temp_file(self, content: str, suffix: str = '.txt') -> str:
        """Create a temporary file and track it for cleanup"""
        temp_file = self.test_utils.create_temp_file(content, suffix)
        self.temp_files.append(temp_file)
        return temp_file

    @patch('app.generate_storyboard_frames')
    def test_complete_small_screenplay_workflow(self, mock_generate):
        """Test complete workflow with small screenplay"""
        # Mock frame generation
        mock_generate.return_value = self.mock_data.generate_frames(2, 1)
        
        # Create temporary screenplay file
        temp_file = self.create_temp_file(self.small_screenplay)
        
        # Step 1: Upload screenplay
        with open(temp_file, 'rb') as f:
            upload_response = self.app.post('/upload', data={
                'file': (f, 'small_screenplay.txt')
            })
        
        self.assertEqual(upload_response.status_code, 200)
        upload_data = json.loads(upload_response.data)
        project_id = upload_data['project_id']
        
        self.assertIn('project_id', upload_data)
        self.assertIn('text_length', upload_data)
        self.assertGreater(upload_data['text_length'], 0)
        
        # Step 2: Quick analysis
        analyze_response = self.app.post('/quick-analyze',
                                       data=json.dumps({'project_id': project_id}),
                                       content_type='application/json')
        
        self.assertEqual(analyze_response.status_code, 200)
        analyze_data = json.loads(analyze_response.data)
        
        self.assertIn('analysis', analyze_data)
        analysis = analyze_data['analysis']
        self.assertIn('title', analysis)
        self.assertIn('characters', analysis)
        self.assertIn('scenes', analysis)
        self.assertGreater(len(analysis['scenes']), 0)
        
        # Step 3: Generate storyboard
        generate_response = self.app.post('/generate',
                                        data=json.dumps({
                                            'project_id': project_id,
                                            'style': 'classic',
                                            'max_scenes': 5
                                        }),
                                        content_type='application/json')
        
        self.assertEqual(generate_response.status_code, 200)
        generate_data = json.loads(generate_response.data)
        
        self.assertIn('project_id', generate_data)
        self.assertIn('status', generate_data)
        self.assertEqual(generate_data['status'], 'processing')
        
        # Step 4: Check status (simulating polling)
        status_response = self.app.get(f'/status/{project_id}')
        self.assertEqual(status_response.status_code, 200)
        status_data = json.loads(status_response.data)
        
        self.assertIn('project', status_data)
        self.assertIn('status', status_data)
        self.assertEqual(status_data['project']['id'], project_id)
        
        # Step 5: Access print version
        print_response = self.app.get(f'/print/{project_id}')
        self.assertEqual(print_response.status_code, 200)
        
        # Verify print page contains expected content
        self.assertIn(b'printable-storyboard', print_response.data)
        self.assertIn(b'TEST SCREENPLAY', print_response.data)
        self.assertIn(b'frame-panel', print_response.data)

    @patch('app.generate_storyboard_frames')
    def test_complete_large_screenplay_workflow(self, mock_generate):
        """Test complete workflow with large screenplay"""
        # Mock frame generation with more frames
        mock_generate.return_value = self.mock_data.generate_frames(10, 2)
        
        # Create temporary screenplay file
        temp_file = self.create_temp_file(self.large_screenplay)
        
        # Step 1: Upload large screenplay
        with open(temp_file, 'rb') as f:
            upload_response = self.app.post('/upload', data={
                'file': (f, 'large_screenplay.txt')
            })
        
        self.assertEqual(upload_response.status_code, 200)
        upload_data = json.loads(upload_response.data)
        project_id = upload_data['project_id']
        
        # Verify large file handling
        self.assertGreater(upload_data['text_length'], 1000)
        self.assertGreater(upload_data['word_count'], 100)
        
        # Step 2: Quick analysis
        analyze_response = self.app.post('/quick-analyze',
                                       data=json.dumps({'project_id': project_id}),
                                       content_type='application/json')
        
        self.assertEqual(analyze_response.status_code, 200)
        analyze_data = json.loads(analyze_response.data)
        
        analysis = analyze_data['analysis']
        self.assertGreater(analysis['total_scenes'], 5)
        self.assertGreater(len(analysis['characters']), 0)
        
        # Step 3: Generate with higher scene limit
        generate_response = self.app.post('/generate',
                                        data=json.dumps({
                                            'project_id': project_id,
                                            'style': 'cinematic',
                                            'max_scenes': 10
                                        }),
                                        content_type='application/json')
        
        self.assertEqual(generate_response.status_code, 200)
        generate_data = json.loads(generate_response.data)
        self.assertEqual(generate_data['status'], 'processing')
        
        # Step 4: Verify status tracking
        status_response = self.app.get(f'/status/{project_id}')
        self.assertEqual(status_response.status_code, 200)
        status_data = json.loads(status_response.data)
        
        # Should have more frames for large screenplay
        if 'frames' in status_data['status']:
            self.assertGreater(len(status_data['status']['frames']), 5)
        
        # Step 5: Print should handle large content
        print_response = self.app.get(f'/print/{project_id}')
        self.assertEqual(print_response.status_code, 200)
        
        # Should contain multiple scenes
        scene_count = print_response.data.count(b'scene-section')
        self.assertGreater(scene_count, 5)

    def test_multiple_file_formats(self):
        """Test workflow with different file formats"""
        # Test with .txt file
        txt_file = self.create_temp_file(self.small_screenplay, '.txt')
        
        with open(txt_file, 'rb') as f:
            txt_response = self.app.post('/upload', data={
                'file': (f, 'screenplay.txt')
            })
        
        self.assertEqual(txt_response.status_code, 200)
        txt_data = json.loads(txt_response.data)
        self.assertIn('project_id', txt_data)
        
        # Test with .fountain file
        fountain_file = self.create_temp_file(self.small_screenplay, '.fountain')
        
        with open(fountain_file, 'rb') as f:
            fountain_response = self.app.post('/upload', data={
                'file': (f, 'screenplay.fountain')
            })
        
        self.assertEqual(fountain_response.status_code, 200)
        fountain_data = json.loads(fountain_response.data)
        self.assertIn('project_id', fountain_data)
        
        # Both should have similar text lengths
        self.assertAlmostEqual(
            txt_data['text_length'], 
            fountain_data['text_length'], 
            delta=10
        )

    @patch('app.generate_storyboard_frames')
    def test_error_recovery_workflow(self, mock_generate):
        """Test workflow with error conditions and recovery"""
        # Mock generation failure initially
        mock_generate.side_effect = Exception("Generation failed")
        
        # Create temporary screenplay file
        temp_file = self.create_temp_file(self.small_screenplay)
        
        # Step 1: Upload screenplay
        with open(temp_file, 'rb') as f:
            upload_response = self.app.post('/upload', data={
                'file': (f, 'error_test.txt')
            })
        
        self.assertEqual(upload_response.status_code, 200)
        project_id = json.loads(upload_response.data)['project_id']
        
        # Step 2: Quick analysis should still work
        analyze_response = self.app.post('/quick-analyze',
                                       data=json.dumps({'project_id': project_id}),
                                       content_type='application/json')
        
        self.assertEqual(analyze_response.status_code, 200)
        
        # Step 3: Generation should handle errors gracefully
        generate_response = self.app.post('/generate',
                                        data=json.dumps({
                                            'project_id': project_id,
                                            'style': 'classic',
                                            'max_scenes': 3
                                        }),
                                        content_type='application/json')
        
        # Should return error response
        self.assertEqual(generate_response.status_code, 500)
        
        # Step 4: Status should reflect error
        status_response = self.app.get(f'/status/{project_id}')
        self.assertEqual(status_response.status_code, 200)
        status_data = json.loads(status_response.data)
        
        # Should have error information
        if 'status' in status_data:
            self.assertIn('error', status_data['status'])
        
        # Step 5: Fix the generation and retry
        mock_generate.side_effect = None
        mock_generate.return_value = self.mock_data.generate_frames(2, 1)
        
        # Retry generation
        retry_response = self.app.post('/generate',
                                     data=json.dumps({
                                         'project_id': project_id,
                                         'style': 'classic',
                                         'max_scenes': 3
                                     }),
                                     content_type='application/json')
        
        self.assertEqual(retry_response.status_code, 200)

    def test_concurrent_project_handling(self):
        """Test handling multiple concurrent projects"""
        project_ids = []
        
        # Create multiple projects
        for i in range(3):
            screenplay = self.mock_data.generate_screenplay(
                scenes=3, 
                characters=[f'CHAR{i}A', f'CHAR{i}B']
            )
            temp_file = self.create_temp_file(screenplay)
            
            with open(temp_file, 'rb') as f:
                upload_response = self.app.post('/upload', data={
                    'file': (f, f'project_{i}.txt')
                })
            
            self.assertEqual(upload_response.status_code, 200)
            project_id = json.loads(upload_response.data)['project_id']
            project_ids.append(project_id)
        
        # Verify all projects exist
        self.assertEqual(len(projects), 3)
        
        # Analyze all projects
        for i, project_id in enumerate(project_ids):
            analyze_response = self.app.post('/quick-analyze',
                                           data=json.dumps({'project_id': project_id}),
                                           content_type='application/json')
            
            self.assertEqual(analyze_response.status_code, 200)
            analyze_data = json.loads(analyze_response.data)
            
            # Each project should have its own characters
            characters = analyze_data['analysis']['characters']
            self.assertIn(f'CHAR{i}A', characters)
            self.assertIn(f'CHAR{i}B', characters)
        
        # Check status for all projects
        for project_id in project_ids:
            status_response = self.app.get(f'/status/{project_id}')
            self.assertEqual(status_response.status_code, 200)
            status_data = json.loads(status_response.data)
            self.assertEqual(status_data['project']['id'], project_id)

    @patch('app.generate_storyboard_frames')
    def test_style_variation_workflow(self, mock_generate):
        """Test workflow with different style options"""
        # Mock generation with different styles
        mock_generate.return_value = self.mock_data.generate_frames(2, 1)
        
        temp_file = self.create_temp_file(self.small_screenplay)
        
        # Test different styles
        styles = ['classic', 'cinematic', 'modern', 'sketch']
        
        for style in styles:
            with open(temp_file, 'rb') as f:
                upload_response = self.app.post('/upload', data={
                    'file': (f, f'{style}_screenplay.txt')
                })
            
            self.assertEqual(upload_response.status_code, 200)
            project_id = json.loads(upload_response.data)['project_id']
            
            # Generate with specific style
            generate_response = self.app.post('/generate',
                                            data=json.dumps({
                                                'project_id': project_id,
                                                'style': style,
                                                'max_scenes': 3
                                            }),
                                            content_type='application/json')
            
            self.assertEqual(generate_response.status_code, 200)
            
            # Verify style is recorded
            status_response = self.app.get(f'/status/{project_id}')
            self.assertEqual(status_response.status_code, 200)
            status_data = json.loads(status_response.data)
            
            if 'status' in status_data and 'style' in status_data['status']:
                self.assertEqual(status_data['status']['style'], style)

    def test_performance_with_large_content(self):
        """Test performance with large content"""
        # Create very large screenplay
        large_screenplay = self.mock_data.generate_screenplay(
            scenes=20, 
            characters=['HERO', 'VILLAIN', 'SIDEKICK', 'MENTOR']
        )
        
        temp_file = self.create_temp_file(large_screenplay)
        
        # Measure upload time
        start_time = time.time()
        
        with open(temp_file, 'rb') as f:
            upload_response = self.app.post('/upload', data={
                'file': (f, 'large_performance_test.txt')
            })
        
        upload_time = time.time() - start_time
        
        self.assertEqual(upload_response.status_code, 200)
        self.assertLess(upload_time, 5.0)  # Should upload within 5 seconds
        
        project_id = json.loads(upload_response.data)['project_id']
        
        # Measure analysis time
        start_time = time.time()
        
        analyze_response = self.app.post('/quick-analyze',
                                       data=json.dumps({'project_id': project_id}),
                                       content_type='application/json')
        
        analyze_time = time.time() - start_time
        
        self.assertEqual(analyze_response.status_code, 200)
        self.assertLess(analyze_time, 10.0)  # Should analyze within 10 seconds
        
        # Verify analysis quality
        analyze_data = json.loads(analyze_response.data)
        analysis = analyze_data['analysis']
        
        self.assertGreater(analysis['total_scenes'], 10)
        self.assertGreater(len(analysis['characters']), 2)
        self.assertGreater(analysis['word_count'], 500)

    def test_ui_page_accessibility(self):
        """Test that all UI pages are accessible"""
        pages = [
            '/',
            '/upload',
            '/generate',
            '/processing'
        ]
        
        for page in pages:
            response = self.app.get(page)
            self.assertEqual(response.status_code, 200)
            
            # Check for basic HTML structure
            self.assertIn(b'<!DOCTYPE html>', response.data)
            self.assertIn(b'<html', response.data)
            self.assertIn(b'<head>', response.data)
            self.assertIn(b'<body>', response.data)
            
            # Check for navigation or basic UI elements
            self.assertIn(b'Script Fury', response.data)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity throughout the workflow"""

    def setUp(self):
        """Set up test environment"""
        self.app = app.test_client()
        self.app.testing = True
        
        projects.clear()
        generation_status.clear()
        
        self.mock_data = MockDataGenerator()
        self.temp_files = []

    def tearDown(self):
        """Clean up after tests"""
        projects.clear()
        generation_status.clear()
        
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except OSError:
                pass

    def test_data_consistency_across_workflow(self):
        """Test that data remains consistent across workflow steps"""
        # Create test screenplay
        screenplay = self.mock_data.generate_screenplay(scenes=3)
        temp_file = TestUtilities.create_temp_file(screenplay)
        self.temp_files.append(temp_file)
        
        # Upload and track original data
        with open(temp_file, 'rb') as f:
            upload_response = self.app.post('/upload', data={
                'file': (f, 'consistency_test.txt')
            })
        
        self.assertEqual(upload_response.status_code, 200)
        upload_data = json.loads(upload_response.data)
        project_id = upload_data['project_id']
        
        # Verify project data integrity
        self.assertIn(project_id, projects)
        project = projects[project_id]
        
        self.assertEqual(project['filename'], 'consistency_test.txt')
        self.assertEqual(len(project['text']), upload_data['text_length'])
        self.assertEqual(project['word_count'], upload_data['word_count'])
        
        # Analyze and verify consistency
        analyze_response = self.app.post('/quick-analyze',
                                       data=json.dumps({'project_id': project_id}),
                                       content_type='application/json')
        
        self.assertEqual(analyze_response.status_code, 200)
        analyze_data = json.loads(analyze_response.data)
        analysis = analyze_data['analysis']
        
        # Check that analysis references match project data
        self.assertEqual(analysis['word_count'], project['word_count'])
        self.assertGreater(analysis['total_scenes'], 0)
        self.assertGreater(len(analysis['characters']), 0)
        
        # Verify status endpoint consistency
        status_response = self.app.get(f'/status/{project_id}')
        self.assertEqual(status_response.status_code, 200)
        status_data = json.loads(status_response.data)
        
        # Project data should match original
        status_project = status_data['project']
        self.assertEqual(status_project['id'], project_id)
        self.assertEqual(status_project['filename'], 'consistency_test.txt')
        self.assertEqual(status_project['word_count'], upload_data['word_count'])

    def test_character_extraction_consistency(self):
        """Test that character extraction is consistent"""
        # Create screenplay with known characters
        screenplay = """TEST CHARACTER CONSISTENCY

FADE IN:

EXT. PARK - DAY

ALICE walks through the park.

ALICE
Beautiful day today.

BOB approaches from behind.

BOB
Alice! Wait up!

ALICE
Oh, hi Bob.

CHARLIE appears from behind a tree.

CHARLIE
Surprise!

FADE OUT.
"""
        
        temp_file = TestUtilities.create_temp_file(screenplay)
        self.temp_files.append(temp_file)
        
        with open(temp_file, 'rb') as f:
            upload_response = self.app.post('/upload', data={
                'file': (f, 'character_test.txt')
            })
        
        project_id = json.loads(upload_response.data)['project_id']
        
        # Analyze multiple times to check consistency
        characters_sets = []
        
        for i in range(3):
            analyze_response = self.app.post('/quick-analyze',
                                           data=json.dumps({'project_id': project_id}),
                                           content_type='application/json')
            
            self.assertEqual(analyze_response.status_code, 200)
            analyze_data = json.loads(analyze_response.data)
            characters = set(analyze_data['analysis']['characters'])
            characters_sets.append(characters)
        
        # All character sets should be identical
        for i in range(1, len(characters_sets)):
            self.assertEqual(characters_sets[0], characters_sets[i])
        
        # Should contain expected characters
        expected_characters = {'ALICE', 'BOB', 'CHARLIE'}
        self.assertEqual(characters_sets[0], expected_characters)


if __name__ == '__main__':
    unittest.main()