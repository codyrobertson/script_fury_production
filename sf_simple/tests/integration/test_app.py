"""
Integration tests for the Flask application
"""

import unittest
import json
import os
import tempfile
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import app, projects, generation_status
from utils.text_extractor import extract_text_from_file
from utils.scene_analyzer import analyze_screenplay
from utils.storyboard_generator import generate_storyboard_frames
from utils.print_generator import generate_printable_storyboard


class TestFlaskApp(unittest.TestCase):
    """Integration tests for Flask application endpoints"""

    def setUp(self):
        """Set up test fixtures and Flask test client"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear any existing projects and status
        projects.clear()
        generation_status.clear()
        
        # Create test directory if it doesn't exist
        self.test_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Sample screenplay content
        self.sample_screenplay = """THE TEST SCREENPLAY

FADE IN:

EXT. CITY STREET - DAY

A bustling urban scene. Cars honk in the distance.

JOHN
(determined)
Another day, another case.

He stops at a coffee shop.

INT. COFFEE SHOP - CONTINUOUS

SARAH serves customers with a smile.

SARAH
John! Come in!

JOHN
The usual?

SARAH
You know me too well.

FADE OUT.
"""

    def tearDown(self):
        """Clean up after each test"""
        projects.clear()
        generation_status.clear()

    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Script Fury Simple', response.data)
        self.assertIn(b'Upload', response.data)

    def test_upload_page(self):
        """Test upload page loads correctly"""
        response = self.app.get('/upload')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload Screenplay', response.data)
        self.assertIn(b'Choose File', response.data)

    def test_upload_file_success(self):
        """Test successful file upload"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.sample_screenplay)
            temp_path = f.name
        
        try:
            with open(temp_path, 'rb') as f:
                response = self.app.post('/upload', data={
                    'file': (f, 'test_screenplay.txt')
                })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('project_id', data)
            self.assertIn('text_length', data)
            self.assertIn('word_count', data)
            self.assertIn('char_count', data)
            
            # Check project was created
            project_id = data['project_id']
            self.assertIn(project_id, projects)
            
        finally:
            os.unlink(temp_path)

    def test_upload_file_no_file(self):
        """Test upload with no file provided"""
        response = self.app.post('/upload', data={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No file provided')

    def test_upload_file_empty_filename(self):
        """Test upload with empty filename"""
        response = self.app.post('/upload', data={
            'file': (b'', '')
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No file selected')

    def test_quick_analyze_success(self):
        """Test quick analysis endpoint"""
        # First upload a file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.sample_screenplay)
            temp_path = f.name
        
        try:
            with open(temp_path, 'rb') as f:
                upload_response = self.app.post('/upload', data={
                    'file': (f, 'test_screenplay.txt')
                })
            
            project_id = json.loads(upload_response.data)['project_id']
            
            # Then analyze it
            response = self.app.post('/quick-analyze', 
                                   data=json.dumps({'project_id': project_id}),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('analysis', data)
            self.assertIn('title', data['analysis'])
            self.assertIn('characters', data['analysis'])
            self.assertIn('scenes', data['analysis'])
            
        finally:
            os.unlink(temp_path)

    def test_quick_analyze_invalid_project(self):
        """Test quick analysis with invalid project ID"""
        response = self.app.post('/quick-analyze',
                               data=json.dumps({'project_id': 'invalid-id'}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Project not found')

    def test_generate_page(self):
        """Test generate page loads correctly"""
        response = self.app.get('/generate')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Generate Storyboard', response.data)
        self.assertIn(b'Style Selection', response.data)

    @patch('app.generate_storyboard_frames')
    def test_generate_storyboard_success(self, mock_generate):
        """Test successful storyboard generation"""
        # Mock the generation function
        mock_generate.return_value = [
            {
                'frame_id': 'frame_1_1',
                'scene_number': 1,
                'frame_number': 1,
                'status': 'completed',
                'image_url': 'http://example.com/image.jpg',
                'cost': 0.04
            }
        ]
        
        # First upload a file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.sample_screenplay)
            temp_path = f.name
        
        try:
            with open(temp_path, 'rb') as f:
                upload_response = self.app.post('/upload', data={
                    'file': (f, 'test_screenplay.txt')
                })
            
            project_id = json.loads(upload_response.data)['project_id']
            
            # Generate storyboard
            response = self.app.post('/generate',
                                   data=json.dumps({
                                       'project_id': project_id,
                                       'style': 'classic',
                                       'max_scenes': 3
                                   }),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('project_id', data)
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'processing')
            
            # Check generation status was created
            self.assertIn(project_id, generation_status)
            
        finally:
            os.unlink(temp_path)

    def test_generate_storyboard_invalid_project(self):
        """Test storyboard generation with invalid project ID"""
        response = self.app.post('/generate',
                               data=json.dumps({
                                   'project_id': 'invalid-id',
                                   'style': 'classic',
                                   'max_scenes': 3
                               }),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Project not found')

    def test_processing_page(self):
        """Test processing page loads correctly"""
        response = self.app.get('/processing')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Processing', response.data)
        self.assertIn(b'Generation Progress', response.data)

    def test_status_endpoint_success(self):
        """Test status endpoint with valid project"""
        # Create a project with generation status
        project_id = 'test-project-123'
        projects[project_id] = {
            'id': project_id,
            'filename': 'test.txt',
            'text': self.sample_screenplay,
            'created_at': '2023-01-01T12:00:00'
        }
        
        generation_status[project_id] = {
            'status': 'completed',
            'progress': 100,
            'frames': [
                {
                    'frame_id': 'frame_1_1',
                    'scene_number': 1,
                    'frame_number': 1,
                    'status': 'completed'
                }
            ],
            'analysis': {
                'title': 'Test Screenplay',
                'total_scenes': 1
            }
        }
        
        response = self.app.get(f'/status/{project_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('project', data)
        self.assertIn('status', data)
        self.assertEqual(data['status']['status'], 'completed')
        self.assertEqual(data['status']['progress'], 100)

    def test_status_endpoint_invalid_project(self):
        """Test status endpoint with invalid project ID"""
        response = self.app.get('/status/invalid-id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Project not found')

    def test_print_page_success(self):
        """Test print page loads correctly with valid project"""
        # Create a project with generation status
        project_id = 'test-project-456'
        projects[project_id] = {
            'id': project_id,
            'filename': 'test.txt',
            'text': self.sample_screenplay,
            'created_at': '2023-01-01T12:00:00'
        }
        
        generation_status[project_id] = {
            'status': 'completed',
            'progress': 100,
            'frames': [
                {
                    'frame_id': 'frame_1_1',
                    'scene_number': 1,
                    'frame_number': 1,
                    'status': 'completed',
                    'image_url': 'http://example.com/image.jpg'
                }
            ],
            'analysis': {
                'title': 'Test Screenplay',
                'total_scenes': 1
            }
        }
        
        response = self.app.get(f'/print/{project_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'printable-storyboard', response.data)
        self.assertIn(b'Test Screenplay', response.data)

    def test_print_page_invalid_project(self):
        """Test print page with invalid project ID"""
        response = self.app.get('/print/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Project not found', response.data)

    def test_print_page_no_frames(self):
        """Test print page with project that has no frames"""
        project_id = 'test-project-789'
        projects[project_id] = {
            'id': project_id,
            'filename': 'test.txt',
            'text': self.sample_screenplay,
            'created_at': '2023-01-01T12:00:00'
        }
        
        generation_status[project_id] = {
            'status': 'completed',
            'progress': 100,
            'frames': [],
            'analysis': {
                'title': 'Test Screenplay',
                'total_scenes': 0
            }
        }
        
        response = self.app.get(f'/print/{project_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'printable-storyboard', response.data)
        self.assertIn(b'Test Screenplay', response.data)

    def test_static_files_accessible(self):
        """Test that static files are accessible"""
        # Test CSS file
        response = self.app.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'body', response.data)
        
        # Test JS file
        response = self.app.get('/static/js/app.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'function', response.data)


class TestFlaskAppWorkflow(unittest.TestCase):
    """Integration tests for complete application workflows"""

    def setUp(self):
        """Set up test fixtures and Flask test client"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear any existing projects and status
        projects.clear()
        generation_status.clear()
        
        # Sample screenplay content
        self.sample_screenplay = """THE WORKFLOW TEST

FADE IN:

EXT. BEACH - DAY

Waves crash against the shore. A surfer rides a big wave.

SURFER
(excited)
This is incredible!

LIFEGUARD
(concerned)
Be careful out there!

INT. BEACH HOUSE - CONTINUOUS

The lifeguard watches through binoculars.

LIFEGUARD
(into radio)
All clear on the beach.

FADE OUT.
"""

    def tearDown(self):
        """Clean up after each test"""
        projects.clear()
        generation_status.clear()

    @patch('app.generate_storyboard_frames')
    def test_complete_workflow(self, mock_generate):
        """Test complete workflow from upload to print"""
        # Mock the generation function
        mock_generate.return_value = [
            {
                'frame_id': 'frame_1_1',
                'scene_number': 1,
                'frame_number': 1,
                'status': 'completed',
                'image_url': 'http://example.com/image1.jpg',
                'cost': 0.04,
                'location': 'BEACH',
                'time_of_day': 'DAY',
                'characters': ['SURFER', 'LIFEGUARD'],
                'key_visual': 'Surfer rides a big wave',
                'prompt': 'Professional storyboard showing beach scene'
            },
            {
                'frame_id': 'frame_2_1',
                'scene_number': 2,
                'frame_number': 1,
                'status': 'completed',
                'image_url': 'http://example.com/image2.jpg',
                'cost': 0.04,
                'location': 'BEACH HOUSE',
                'time_of_day': 'CONTINUOUS',
                'characters': ['LIFEGUARD'],
                'key_visual': 'Lifeguard watches through binoculars',
                'prompt': 'Professional storyboard showing beach house interior'
            }
        ]
        
        # Step 1: Upload file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.sample_screenplay)
            temp_path = f.name
        
        try:
            with open(temp_path, 'rb') as f:
                upload_response = self.app.post('/upload', data={
                    'file': (f, 'workflow_test.txt')
                })
            
            self.assertEqual(upload_response.status_code, 200)
            upload_data = json.loads(upload_response.data)
            project_id = upload_data['project_id']
            
            # Step 2: Quick analyze
            analyze_response = self.app.post('/quick-analyze',
                                           data=json.dumps({'project_id': project_id}),
                                           content_type='application/json')
            
            self.assertEqual(analyze_response.status_code, 200)
            analyze_data = json.loads(analyze_response.data)
            self.assertIn('analysis', analyze_data)
            self.assertEqual(analyze_data['analysis']['title'], 'THE WORKFLOW TEST')
            
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
            self.assertEqual(generate_data['status'], 'processing')
            
            # Step 4: Check status
            status_response = self.app.get(f'/status/{project_id}')
            self.assertEqual(status_response.status_code, 200)
            status_data = json.loads(status_response.data)
            self.assertIn('project', status_data)
            self.assertIn('status', status_data)
            
            # Step 5: Access print page
            print_response = self.app.get(f'/print/{project_id}')
            self.assertEqual(print_response.status_code, 200)
            self.assertIn(b'printable-storyboard', print_response.data)
            self.assertIn(b'THE WORKFLOW TEST', print_response.data)
            
        finally:
            os.unlink(temp_path)

    def test_error_handling_workflow(self):
        """Test error handling throughout the workflow"""
        # Test invalid project ID at each step
        invalid_id = 'invalid-project-id'
        
        # Quick analyze with invalid ID
        analyze_response = self.app.post('/quick-analyze',
                                       data=json.dumps({'project_id': invalid_id}),
                                       content_type='application/json')
        self.assertEqual(analyze_response.status_code, 404)
        
        # Generate with invalid ID
        generate_response = self.app.post('/generate',
                                        data=json.dumps({
                                            'project_id': invalid_id,
                                            'style': 'classic',
                                            'max_scenes': 3
                                        }),
                                        content_type='application/json')
        self.assertEqual(generate_response.status_code, 404)
        
        # Status with invalid ID
        status_response = self.app.get(f'/status/{invalid_id}')
        self.assertEqual(status_response.status_code, 404)
        
        # Print with invalid ID
        print_response = self.app.get(f'/print/{invalid_id}')
        self.assertEqual(print_response.status_code, 404)

    def test_concurrent_projects(self):
        """Test handling multiple concurrent projects"""
        # Create multiple projects
        projects_data = []
        
        for i in range(3):
            screenplay = f"""PROJECT {i+1}

FADE IN:

EXT. LOCATION {i+1} - DAY

Scene description for project {i+1}.

CHARACTER{i+1}
Line for project {i+1}.

FADE OUT.
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(screenplay)
                temp_path = f.name
            
            try:
                with open(temp_path, 'rb') as f:
                    upload_response = self.app.post('/upload', data={
                        'file': (f, f'project_{i+1}.txt')
                    })
                
                self.assertEqual(upload_response.status_code, 200)
                upload_data = json.loads(upload_response.data)
                projects_data.append({
                    'id': upload_data['project_id'],
                    'temp_path': temp_path
                })
                
            except Exception as e:
                os.unlink(temp_path)
                raise e
        
        try:
            # Verify all projects exist
            for project_data in projects_data:
                project_id = project_data['id']
                self.assertIn(project_id, projects)
                
                # Test quick analyze for each
                analyze_response = self.app.post('/quick-analyze',
                                               data=json.dumps({'project_id': project_id}),
                                               content_type='application/json')
                self.assertEqual(analyze_response.status_code, 200)
                
                # Test status endpoint
                status_response = self.app.get(f'/status/{project_id}')
                self.assertEqual(status_response.status_code, 200)
            
        finally:
            # Clean up temporary files
            for project_data in projects_data:
                os.unlink(project_data['temp_path'])


if __name__ == '__main__':
    unittest.main()