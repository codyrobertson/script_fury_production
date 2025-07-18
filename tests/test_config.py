"""
Test configuration and utilities
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock


class TestConfig:
    """Configuration for testing"""
    
    # Test directories
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    FIXTURES_DIR = os.path.join(TEST_DIR, 'fixtures')
    PROJECT_ROOT = os.path.dirname(TEST_DIR)
    
    # Test data
    SAMPLE_SCREENPLAY = """THE TEST SCREENPLAY

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

    LARGE_SCREENPLAY = """LARGE SCREENPLAY TEST

FADE IN:

EXT. MOUNTAIN RANGE - DAY

Vast mountains stretch across the horizon.

ALEX
Storm's coming in fast.

EXT. FOREST PATH - DAY

A group of hikers makes their way through dense trees.

MAYA
Stay close everyone.

INT. CABIN - NIGHT

Alex and Maya huddle around a fire.

ALEX
We need to get out of here.

MAYA
(worried)
The radio's dead.

EXT. HELICOPTER PAD - DAY

A rescue helicopter sits on a landing pad.

PILOT JONES
(into radio)
Ground control, requesting permission.

FADE OUT.
"""

    # Sample analysis data
    SAMPLE_ANALYSIS = {
        'title': 'Test Screenplay',
        'total_scenes': 2,
        'scenes': [
            {
                'scene_number': 1,
                'slug_line': 'EXT. CITY STREET - DAY',
                'location': 'CITY STREET',
                'time_of_day': 'DAY',
                'description': 'A bustling urban scene.',
                'key_visual_moment': 'Cars honking in busy traffic',
                'characters': ['JOHN', 'SARAH'],
                'dialogue': []
            },
            {
                'scene_number': 2,
                'slug_line': 'INT. COFFEE SHOP - CONTINUOUS',
                'location': 'COFFEE SHOP',
                'time_of_day': 'CONTINUOUS',
                'description': 'A cozy coffee shop.',
                'key_visual_moment': 'Sarah serves coffee with a smile',
                'characters': ['SARAH', 'JOHN'],
                'dialogue': []
            }
        ],
        'characters': ['JOHN', 'SARAH'],
        'page_count': 2,
        'word_count': 50,
        'analyzed_at': '2023-01-01T12:00:00'
    }

    # Sample frames data
    SAMPLE_FRAMES = [
        {
            'frame_id': 'frame_1_1',
            'scene_number': 1,
            'frame_number': 1,
            'image_url': 'https://example.com/image1.jpg',
            'status': 'completed',
            'prompt_used': 'Professional storyboard, wide shot showing CITY STREET during DAY',
            'location': 'CITY STREET',
            'time_of_day': 'DAY',
            'characters': ['JOHN', 'SARAH'],
            'key_visual': 'Cars honking in busy traffic',
            'scene_description': 'A bustling urban scene.',
            'cost': 0.04,
            'generation_time': '2023-01-01T12:00:00'
        },
        {
            'frame_id': 'frame_2_1',
            'scene_number': 2,
            'frame_number': 1,
            'image_url': 'https://example.com/image2.jpg',
            'status': 'completed',
            'prompt_used': 'Professional storyboard, medium shot showing COFFEE SHOP interior',
            'location': 'COFFEE SHOP',
            'time_of_day': 'CONTINUOUS',
            'characters': ['SARAH'],
            'key_visual': 'Sarah serves coffee with a smile',
            'scene_description': 'A cozy coffee shop.',
            'cost': 0.04,
            'generation_time': '2023-01-01T12:01:00'
        }
    ]


class TestUtilities:
    """Utilities for testing"""
    
    @staticmethod
    def create_temp_file(content: str, suffix: str = '.txt') -> str:
        """Create a temporary file with content"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            return f.name
    
    @staticmethod
    def create_temp_screenplay(title: str = "Test Screenplay") -> str:
        """Create a temporary screenplay file"""
        content = f"""{title}

FADE IN:

EXT. LOCATION - DAY

A test scene.

CHARACTER
Test dialogue.

FADE OUT.
"""
        return TestUtilities.create_temp_file(content)
    
    @staticmethod
    def create_mock_project(project_id: str = 'test-project-123'):
        """Create a mock project dictionary"""
        return {
            'id': project_id,
            'filename': 'test_screenplay.txt',
            'text': TestConfig.SAMPLE_SCREENPLAY,
            'created_at': '2023-01-01T12:00:00',
            'word_count': 50,
            'char_count': 250
        }
    
    @staticmethod
    def create_mock_generation_status(project_id: str = 'test-project-123'):
        """Create a mock generation status dictionary"""
        return {
            'status': 'completed',
            'progress': 100,
            'frames': TestConfig.SAMPLE_FRAMES,
            'analysis': TestConfig.SAMPLE_ANALYSIS,
            'style': 'classic',
            'max_scenes': 5,
            'started_at': '2023-01-01T12:00:00',
            'completed_at': '2023-01-01T12:05:00'
        }
    
    @staticmethod
    def setup_project_path():
        """Add project root to sys.path for imports"""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
    
    @staticmethod
    def create_mock_flask_app():
        """Create a mock Flask app for testing"""
        from unittest.mock import MagicMock
        
        app = MagicMock()
        app.test_client.return_value = MagicMock()
        app.testing = True
        
        return app


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Set up test environment"""
        TestUtilities.setup_project_path()
        
        # Create fixtures directory if it doesn't exist
        os.makedirs(TestConfig.FIXTURES_DIR, exist_ok=True)
        
        # Clear any existing project data
        self.temp_files = []
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up temporary files
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except OSError:
                pass
    
    def create_temp_file(self, content: str, suffix: str = '.txt') -> str:
        """Create a temporary file and track it for cleanup"""
        temp_file = TestUtilities.create_temp_file(content, suffix)
        self.temp_files.append(temp_file)
        return temp_file
    
    def assertFileExists(self, filepath: str):
        """Assert that a file exists"""
        self.assertTrue(os.path.exists(filepath), f"File does not exist: {filepath}")
    
    def assertFileContains(self, filepath: str, content: str):
        """Assert that a file contains specific content"""
        with open(filepath, 'r') as f:
            file_content = f.read()
        self.assertIn(content, file_content)
    
    def assertDictContainsSubset(self, subset: dict, dictionary: dict):
        """Assert that dictionary contains all key-value pairs from subset"""
        for key, value in subset.items():
            self.assertIn(key, dictionary)
            self.assertEqual(dictionary[key], value)


class MockDataGenerator:
    """Generate mock data for testing"""
    
    @staticmethod
    def generate_screenplay(scenes: int = 3, characters: list = None) -> str:
        """Generate a screenplay with specified number of scenes"""
        if characters is None:
            characters = ['JOHN', 'SARAH', 'MIKE']
        
        screenplay = "TEST SCREENPLAY\n\nFADE IN:\n\n"
        
        for i in range(1, scenes + 1):
            location = f"LOCATION {i}"
            time_of_day = "DAY" if i % 2 == 1 else "NIGHT"
            screenplay += f"EXT. {location} - {time_of_day}\n\n"
            screenplay += f"Scene {i} description.\n\n"
            
            # Add a character line
            if i <= len(characters):
                character = characters[i - 1]
                screenplay += f"{character}\nDialogue for scene {i}.\n\n"
        
        screenplay += "FADE OUT.\n"
        return screenplay
    
    @staticmethod
    def generate_frames(scene_count: int = 2, frames_per_scene: int = 1) -> list:
        """Generate mock frames data"""
        frames = []
        
        for scene_num in range(1, scene_count + 1):
            for frame_num in range(1, frames_per_scene + 1):
                frame = {
                    'frame_id': f'frame_{scene_num}_{frame_num}',
                    'scene_number': scene_num,
                    'frame_number': frame_num,
                    'image_url': f'https://example.com/image{scene_num}_{frame_num}.jpg',
                    'status': 'completed',
                    'prompt_used': f'Professional storyboard for scene {scene_num}',
                    'location': f'LOCATION {scene_num}',
                    'time_of_day': 'DAY' if scene_num % 2 == 1 else 'NIGHT',
                    'characters': ['JOHN', 'SARAH'],
                    'key_visual': f'Visual moment for scene {scene_num}',
                    'scene_description': f'Description for scene {scene_num}',
                    'cost': 0.04,
                    'generation_time': '2023-01-01T12:00:00'
                }
                frames.append(frame)
        
        return frames
    
    @staticmethod
    def generate_analysis(title: str = "Test Analysis", scene_count: int = 2) -> dict:
        """Generate mock analysis data"""
        scenes = []
        
        for i in range(1, scene_count + 1):
            scene = {
                'scene_number': i,
                'slug_line': f'EXT. LOCATION {i} - DAY',
                'location': f'LOCATION {i}',
                'time_of_day': 'DAY',
                'description': f'Scene {i} description.',
                'key_visual_moment': f'Visual moment {i}',
                'characters': ['JOHN', 'SARAH'],
                'dialogue': []
            }
            scenes.append(scene)
        
        return {
            'title': title,
            'total_scenes': scene_count,
            'scenes': scenes,
            'characters': ['JOHN', 'SARAH'],
            'page_count': scene_count,
            'word_count': scene_count * 25,
            'analyzed_at': '2023-01-01T12:00:00'
        }


# Global test configuration
TEST_CONFIG = TestConfig()
TEST_UTILS = TestUtilities()
MOCK_DATA = MockDataGenerator()