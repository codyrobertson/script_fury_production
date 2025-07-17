"""
Unit tests for storyboard_generator.py
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime
import time

# Add the parent directory to sys.path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.storyboard_generator import (
    generate_storyboard_frames,
    generate_frame,
    create_frame_prompt,
    generate_placeholder_image,
    simulate_generation_progress,
    get_frame_metadata,
    calculate_total_cost,
    get_generation_stats
)


class TestStoryboardGenerator(unittest.TestCase):
    """Test cases for storyboard generation utilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_analysis = {
            'title': 'Test Screenplay',
            'total_scenes': 2,
            'scenes': [
                {
                    'scene_number': 1,
                    'slug_line': 'EXT. CITY STREET - DAY',
                    'location': 'CITY STREET',
                    'time_of_day': 'DAY',
                    'description': 'A bustling urban scene with cars and people.',
                    'key_visual_moment': 'Cars honking in busy traffic',
                    'characters': ['JOHN', 'SARAH'],
                    'dialogue': []
                },
                {
                    'scene_number': 2,
                    'slug_line': 'INT. COFFEE SHOP - CONTINUOUS',
                    'location': 'COFFEE SHOP',
                    'time_of_day': 'CONTINUOUS',
                    'description': 'A cozy coffee shop with warm lighting.',
                    'key_visual_moment': 'Sarah serves coffee with a smile',
                    'characters': ['SARAH', 'JOHN'],
                    'dialogue': []
                }
            ]
        }

        self.sample_scene = self.sample_analysis['scenes'][0]
        self.style_prompt = "Professional storyboard, black and white line art"

    def test_create_frame_prompt_basic(self):
        """Test basic frame prompt creation"""
        prompt = create_frame_prompt(self.sample_scene, 1, self.style_prompt)
        
        self.assertIn(self.style_prompt, prompt)
        self.assertIn("CITY STREET", prompt)
        self.assertIn("DAY", prompt)
        self.assertIn("establishing shot", prompt)

    def test_create_frame_prompt_frame_numbers(self):
        """Test frame prompt creation with different frame numbers"""
        prompt1 = create_frame_prompt(self.sample_scene, 1, self.style_prompt)
        prompt2 = create_frame_prompt(self.sample_scene, 2, self.style_prompt)
        
        # First frame should be establishing shot
        self.assertIn("establishing shot", prompt1)
        
        # Second frame should be different shot type
        self.assertNotIn("establishing shot", prompt2)
        self.assertTrue(any(shot in prompt2 for shot in ["medium shot", "close-up", "wide shot"]))

    def test_create_frame_prompt_with_characters(self):
        """Test frame prompt creation includes characters"""
        prompt = create_frame_prompt(self.sample_scene, 1, self.style_prompt)
        
        self.assertIn("JOHN", prompt)
        self.assertIn("SARAH", prompt)

    def test_create_frame_prompt_no_characters(self):
        """Test frame prompt creation without characters"""
        scene_no_chars = self.sample_scene.copy()
        scene_no_chars['characters'] = []
        
        prompt = create_frame_prompt(scene_no_chars, 1, self.style_prompt)
        
        self.assertIn(self.style_prompt, prompt)
        self.assertIn("CITY STREET", prompt)
        self.assertNotIn("featuring", prompt)

    def test_create_frame_prompt_key_visual(self):
        """Test frame prompt creation includes key visual"""
        prompt = create_frame_prompt(self.sample_scene, 1, self.style_prompt)
        
        self.assertIn("Cars honking in busy traffic", prompt)

    def test_generate_placeholder_image_basic(self):
        """Test placeholder image URL generation"""
        image_url = generate_placeholder_image(self.sample_scene, 1)
        
        self.assertIsInstance(image_url, str)
        self.assertIn("placeholder", image_url)
        self.assertIn("800x600", image_url)

    def test_generate_placeholder_image_scene_based(self):
        """Test placeholder image varies by scene type"""
        # Interior scene
        interior_scene = {
            'scene_number': 1,
            'slug_line': 'INT. COFFEE SHOP - DAY',
            'location': 'COFFEE SHOP',
            'time_of_day': 'DAY'
        }
        
        # Exterior scene
        exterior_scene = {
            'scene_number': 2,
            'slug_line': 'EXT. CITY STREET - DAY',
            'location': 'CITY STREET',
            'time_of_day': 'DAY'
        }
        
        interior_url = generate_placeholder_image(interior_scene, 1)
        exterior_url = generate_placeholder_image(exterior_scene, 1)
        
        # URLs should be different based on scene type
        self.assertNotEqual(interior_url, exterior_url)

    def test_generate_placeholder_image_time_based(self):
        """Test placeholder image varies by time of day"""
        day_scene = self.sample_scene.copy()
        day_scene['time_of_day'] = 'DAY'
        
        night_scene = self.sample_scene.copy()
        night_scene['time_of_day'] = 'NIGHT'
        
        day_url = generate_placeholder_image(day_scene, 1)
        night_url = generate_placeholder_image(night_scene, 1)
        
        # URLs should be different based on time
        self.assertNotEqual(day_url, night_url)

    def test_generate_frame_basic(self):
        """Test basic frame generation"""
        frame = generate_frame(self.sample_scene, 1, self.style_prompt)
        
        # Check required fields
        self.assertIn('frame_id', frame)
        self.assertIn('scene_number', frame)
        self.assertIn('frame_number', frame)
        self.assertIn('prompt', frame)
        self.assertIn('image_url', frame)
        self.assertIn('status', frame)
        self.assertIn('generation_time', frame)
        self.assertIn('cost', frame)

        # Check values
        self.assertEqual(frame['scene_number'], 1)
        self.assertEqual(frame['frame_number'], 1)
        self.assertEqual(frame['status'], 'completed')
        self.assertEqual(frame['cost'], 0.04)
        self.assertIn('frame_1_1', frame['frame_id'])

    def test_generate_frame_includes_scene_data(self):
        """Test frame generation includes scene data"""
        frame = generate_frame(self.sample_scene, 1, self.style_prompt)
        
        self.assertEqual(frame['location'], 'CITY STREET')
        self.assertEqual(frame['time_of_day'], 'DAY')
        self.assertEqual(frame['characters'], ['JOHN', 'SARAH'])
        self.assertEqual(frame['key_visual'], 'Cars honking in busy traffic')

    def test_generate_frame_timestamp(self):
        """Test frame generation includes valid timestamp"""
        frame = generate_frame(self.sample_scene, 1, self.style_prompt)
        
        # Should be a valid ISO timestamp
        try:
            datetime.fromisoformat(frame['generation_time'])
        except ValueError:
            self.fail("generation_time is not a valid ISO timestamp")

    @patch('utils.storyboard_generator.time.sleep')
    @patch('utils.storyboard_generator.random.randint')
    def test_generate_storyboard_frames_basic(self, mock_randint, mock_sleep):
        """Test basic storyboard frame generation"""
        # Mock randomint to return consistent values
        mock_randint.return_value = 1  # 1 frame per scene
        
        frames = generate_storyboard_frames(self.sample_analysis, self.style_prompt)
        
        # Should generate frames for all scenes
        self.assertEqual(len(frames), 2)  # 2 scenes * 1 frame each
        
        # Check frame properties
        for frame in frames:
            self.assertIn('frame_id', frame)
            self.assertIn('scene_number', frame)
            self.assertIn('frame_number', frame)
            self.assertEqual(frame['status'], 'completed')

    @patch('utils.storyboard_generator.time.sleep')
    def test_generate_storyboard_frames_one_per_scene(self, mock_sleep):
        """Test storyboard frame generation with one frame per scene"""        
        frames = generate_storyboard_frames(self.sample_analysis, self.style_prompt)
        
        # Should generate 1 frame per scene (current implementation)
        self.assertEqual(len(frames), 2)  # 2 scenes * 1 frame each
        
        # Check scene distribution
        scene1_frames = [f for f in frames if f['scene_number'] == 1]
        scene2_frames = [f for f in frames if f['scene_number'] == 2]
        
        self.assertEqual(len(scene1_frames), 1)
        self.assertEqual(len(scene2_frames), 1)

    @patch('utils.storyboard_generator.time.sleep')
    def test_generate_storyboard_frames_timing(self, mock_sleep):
        """Test storyboard frame generation includes timing delays"""
        generate_storyboard_frames(self.sample_analysis, self.style_prompt)
        
        # Should have called sleep for each generated frame
        self.assertTrue(mock_sleep.called)

    def test_get_frame_metadata_basic(self):
        """Test frame metadata extraction"""
        frame = generate_frame(self.sample_scene, 1, self.style_prompt)
        metadata = get_frame_metadata(frame)
        
        # Check required fields
        self.assertIn('frame_id', metadata)
        self.assertIn('scene_number', metadata)
        self.assertIn('frame_number', metadata)
        self.assertIn('status', metadata)
        self.assertIn('generation_time', metadata)
        self.assertIn('cost', metadata)
        self.assertIn('has_image', metadata)
        self.assertIn('prompt_length', metadata)
        self.assertIn('characters_count', metadata)
        self.assertIn('location', metadata)
        self.assertIn('time_of_day', metadata)

    def test_get_frame_metadata_values(self):
        """Test frame metadata values are correct"""
        frame = generate_frame(self.sample_scene, 1, self.style_prompt)
        metadata = get_frame_metadata(frame)
        
        self.assertEqual(metadata['scene_number'], 1)
        self.assertEqual(metadata['frame_number'], 1)
        self.assertEqual(metadata['status'], 'completed')
        self.assertTrue(metadata['has_image'])
        self.assertGreater(metadata['prompt_length'], 0)
        self.assertEqual(metadata['characters_count'], 2)
        self.assertEqual(metadata['location'], 'CITY STREET')
        self.assertEqual(metadata['time_of_day'], 'DAY')

    def test_calculate_total_cost_basic(self):
        """Test total cost calculation"""
        frames = [
            {'cost': 0.04},
            {'cost': 0.04},
            {'cost': 0.04}
        ]
        
        total_cost = calculate_total_cost(frames)
        self.assertEqual(total_cost, 0.12)

    def test_calculate_total_cost_empty(self):
        """Test total cost calculation with empty frames"""
        total_cost = calculate_total_cost([])
        self.assertEqual(total_cost, 0)

    def test_calculate_total_cost_missing_cost(self):
        """Test total cost calculation with missing cost values"""
        frames = [
            {'cost': 0.04},
            {},  # Missing cost
            {'cost': 0.04}
        ]
        
        total_cost = calculate_total_cost(frames)
        self.assertEqual(total_cost, 0.08)

    def test_get_generation_stats_basic(self):
        """Test generation statistics"""
        frames = [
            {'status': 'completed', 'cost': 0.04, 'scene_number': 1, 'generation_time': '2023-01-01T12:00:00'},
            {'status': 'completed', 'cost': 0.04, 'scene_number': 1, 'generation_time': '2023-01-01T12:01:00'},
            {'status': 'completed', 'cost': 0.04, 'scene_number': 2, 'generation_time': '2023-01-01T12:02:00'}
        ]
        
        stats = get_generation_stats(frames)
        
        # Check required fields
        self.assertIn('total_frames', stats)
        self.assertIn('completed_frames', stats)
        self.assertIn('success_rate', stats)
        self.assertIn('total_cost', stats)
        self.assertIn('avg_cost_per_frame', stats)
        self.assertIn('scenes_covered', stats)
        self.assertIn('frames_per_scene', stats)

    def test_get_generation_stats_values(self):
        """Test generation statistics values"""
        frames = [
            {'status': 'completed', 'cost': 0.04, 'scene_number': 1, 'generation_time': '2023-01-01T12:00:00'},
            {'status': 'completed', 'cost': 0.04, 'scene_number': 1, 'generation_time': '2023-01-01T12:01:00'},
            {'status': 'failed', 'cost': 0, 'scene_number': 2, 'generation_time': '2023-01-01T12:02:00'}
        ]
        
        stats = get_generation_stats(frames)
        
        self.assertEqual(stats['total_frames'], 3)
        self.assertEqual(stats['completed_frames'], 2)
        self.assertAlmostEqual(stats['success_rate'], 200/3, places=5)  # 66.67%
        self.assertEqual(stats['total_cost'], 0.08)
        self.assertEqual(stats['avg_cost_per_frame'], 0.08/3)
        self.assertEqual(stats['scenes_covered'], 2)
        self.assertEqual(stats['frames_per_scene'], {1: 2, 2: 1})

    def test_get_generation_stats_empty(self):
        """Test generation statistics with empty frames"""
        stats = get_generation_stats([])
        
        self.assertEqual(stats['total_frames'], 0)
        self.assertEqual(stats['completed_frames'], 0)
        self.assertEqual(stats['success_rate'], 0)
        self.assertEqual(stats['total_cost'], 0)
        self.assertEqual(stats['avg_cost_per_frame'], 0)
        self.assertEqual(stats['scenes_covered'], 0)
        self.assertEqual(stats['frames_per_scene'], {})

    def test_simulate_generation_progress_basic(self):
        """Test generation progress simulation"""
        progress_updates = []
        
        def callback(progress, message):
            progress_updates.append({'progress': progress, 'message': message})
        
        with patch('utils.storyboard_generator.time.sleep'):
            simulate_generation_progress(3, callback)
        
        # Should have updates for each frame plus completion
        self.assertEqual(len(progress_updates), 4)
        
        # Check progress values
        self.assertAlmostEqual(progress_updates[0]['progress'], 33.33, places=1)
        self.assertAlmostEqual(progress_updates[1]['progress'], 66.67, places=1)
        self.assertEqual(progress_updates[2]['progress'], 100)
        self.assertEqual(progress_updates[3]['progress'], 100)
        
        # Check final message
        self.assertEqual(progress_updates[3]['message'], "Generation complete!")

    def test_simulate_generation_progress_no_callback(self):
        """Test generation progress simulation without callback"""
        # Should not raise an exception
        with patch('utils.storyboard_generator.time.sleep'):
            simulate_generation_progress(2, None)

    def test_frame_id_format(self):
        """Test frame ID format consistency"""
        frame1 = generate_frame(self.sample_scene, 1, self.style_prompt)
        frame2 = generate_frame(self.sample_scene, 2, self.style_prompt)
        
        # Frame IDs should follow consistent format
        self.assertTrue(frame1['frame_id'].startswith('frame_'))
        self.assertTrue(frame2['frame_id'].startswith('frame_'))
        
        # Should include scene and frame numbers
        self.assertIn('_1_1', frame1['frame_id'])
        self.assertIn('_1_2', frame2['frame_id'])

    def test_frame_prompt_consistency(self):
        """Test frame prompt consistency across generations"""
        frame1 = generate_frame(self.sample_scene, 1, self.style_prompt)
        frame2 = generate_frame(self.sample_scene, 1, self.style_prompt)
        
        # Same scene and frame number should produce similar prompts
        self.assertIn(self.style_prompt, frame1['prompt'])
        self.assertIn(self.style_prompt, frame2['prompt'])
        self.assertIn("CITY STREET", frame1['prompt'])
        self.assertIn("CITY STREET", frame2['prompt'])

    def test_frame_image_url_format(self):
        """Test frame image URL format"""
        frame = generate_frame(self.sample_scene, 1, self.style_prompt)
        
        image_url = frame['image_url']
        self.assertIsInstance(image_url, str)
        self.assertTrue(image_url.startswith('http'))
        self.assertIn('placeholder', image_url)

    def test_frame_scene_description_included(self):
        """Test frame includes scene description"""
        frame = generate_frame(self.sample_scene, 1, self.style_prompt)
        
        self.assertEqual(frame['scene_description'], self.sample_scene['description'])
        self.assertEqual(frame['key_visual'], self.sample_scene['key_visual_moment'])

    def test_generation_with_different_styles(self):
        """Test generation with different style prompts"""
        style1 = "Classic storyboard style"
        style2 = "Cinematic style"
        
        frame1 = generate_frame(self.sample_scene, 1, style1)
        frame2 = generate_frame(self.sample_scene, 1, style2)
        
        # Prompts should include different styles
        self.assertIn(style1, frame1['prompt'])
        self.assertIn(style2, frame2['prompt'])
        self.assertNotEqual(frame1['prompt'], frame2['prompt'])


class TestStoryboardGeneratorIntegration(unittest.TestCase):
    """Integration tests for storyboard generator"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')

    def test_generate_from_sample_analysis(self):
        """Test generating frames from sample analysis"""
        # Create analysis structure similar to scene_analyzer output
        analysis = {
            'title': 'Test Movie',
            'scenes': [
                {
                    'scene_number': 1,
                    'slug_line': 'EXT. BEACH - DAY',
                    'location': 'BEACH',
                    'time_of_day': 'DAY',
                    'description': 'Waves crash against the shore.',
                    'key_visual_moment': 'Surfer rides a big wave',
                    'characters': ['SURFER', 'LIFEGUARD']
                }
            ]
        }
        
        with patch('utils.storyboard_generator.time.sleep'):
            frames = generate_storyboard_frames(analysis, "Professional storyboard")
        
        self.assertGreater(len(frames), 0)
        
        # Check frame quality
        for frame in frames:
            self.assertEqual(frame['status'], 'completed')
            self.assertIsNotNone(frame['image_url'])
            self.assertGreater(len(frame['prompt']), 0)


if __name__ == '__main__':
    unittest.main()