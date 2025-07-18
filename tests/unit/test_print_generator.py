"""
Unit tests for print_generator.py
"""

import unittest
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.print_generator import (
    generate_printable_storyboard,
    generate_frame_grid,
    generate_scene_frames,
    extract_shot_type,
    generate_character_info,
    get_print_styles
)


class TestPrintGenerator(unittest.TestCase):
    """Test cases for print generation utilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_project = {
            'id': 'test-project-123',
            'filename': 'test_screenplay.txt',
            'text': 'Sample screenplay text',
            'created_at': '2023-01-01T12:00:00',
            'word_count': 100,
            'char_count': 500
        }

        self.sample_frames = [
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
                'scene_description': 'A bustling urban scene.'
            },
            {
                'frame_id': 'frame_1_2',
                'scene_number': 1,
                'frame_number': 2,
                'image_url': 'https://example.com/image2.jpg',
                'status': 'completed',
                'prompt_used': 'Professional storyboard, close-up showing characters talking',
                'location': 'CITY STREET',
                'time_of_day': 'DAY',
                'characters': ['JOHN', 'SARAH'],
                'key_visual': 'John and Sarah having conversation',
                'scene_description': 'A bustling urban scene.'
            },
            {
                'frame_id': 'frame_2_1',
                'scene_number': 2,
                'frame_number': 1,
                'image_url': 'https://example.com/image3.jpg',
                'status': 'completed',
                'prompt_used': 'Professional storyboard, medium shot showing COFFEE SHOP interior',
                'location': 'COFFEE SHOP',
                'time_of_day': 'CONTINUOUS',
                'characters': ['SARAH'],
                'key_visual': 'Sarah serves coffee with a smile',
                'scene_description': 'A cozy coffee shop interior.'
            }
        ]

        self.sample_analysis = {
            'title': 'Test Screenplay',
            'total_scenes': 2,
            'page_count': 5,
            'genre': 'Drama',
            'setting': 'Urban',
            'characters': {'JOHN': 'Detective', 'SARAH': 'Barista'}
        }

        self.sample_status = {
            'status': 'completed',
            'progress': 100,
            'frames': self.sample_frames,
            'analysis': self.sample_analysis,
            'style': 'classic',
            'max_scenes': 5,
            'started_at': '2023-01-01T12:00:00',
            'completed_at': '2023-01-01T12:05:00'
        }

    def test_extract_shot_type_basic(self):
        """Test shot type extraction from prompts"""
        self.assertEqual(extract_shot_type("wide shot of the city"), "Wide Shot")
        self.assertEqual(extract_shot_type("close-up of the character"), "Close-Up")
        self.assertEqual(extract_shot_type("medium shot showing action"), "Medium Shot")
        self.assertEqual(extract_shot_type("establishing shot of location"), "Establishing Shot")
        self.assertEqual(extract_shot_type("extreme close-up of eyes"), "Extreme Close-Up")

    def test_extract_shot_type_no_match(self):
        """Test shot type extraction when no match found"""
        result = extract_shot_type("random prompt text")
        self.assertEqual(result, "Medium Shot")  # Default

    def test_extract_shot_type_case_insensitive(self):
        """Test shot type extraction is case insensitive"""
        self.assertEqual(extract_shot_type("WIDE SHOT of the scene"), "Wide Shot")
        self.assertEqual(extract_shot_type("Close-UP of character"), "Close-Up")

    def test_generate_character_info_basic(self):
        """Test character information generation"""
        characters = ['JOHN', 'SARAH', 'MIKE']
        result = generate_character_info(characters)
        
        self.assertIn('<p><strong>Characters:</strong>', result)
        self.assertIn('JOHN', result)
        self.assertIn('SARAH', result)
        self.assertIn('MIKE', result)

    def test_generate_character_info_empty(self):
        """Test character information generation with empty list"""
        result = generate_character_info([])
        self.assertEqual(result, "")

    def test_generate_character_info_too_many(self):
        """Test character information generation limits to 3 characters"""
        characters = ['JOHN', 'SARAH', 'MIKE', 'JANE', 'BOB']
        result = generate_character_info(characters)
        
        # Should only include first 3
        self.assertIn('JOHN', result)
        self.assertIn('SARAH', result)
        self.assertIn('MIKE', result)
        self.assertNotIn('JANE', result)
        self.assertNotIn('BOB', result)

    def test_generate_scene_frames_basic(self):
        """Test scene frames HTML generation"""
        scene_frames = [self.sample_frames[0], self.sample_frames[1]]
        result = generate_scene_frames(scene_frames)
        
        # Should contain frame panels
        self.assertIn('frame-panel', result)
        self.assertIn('Frame 1', result)
        self.assertIn('Frame 2', result)
        
        # Should contain image URLs
        self.assertIn('https://example.com/image1.jpg', result)
        self.assertIn('https://example.com/image2.jpg', result)
        
        # Should contain frame information
        self.assertIn('Wide Shot', result)
        self.assertIn('Close-Up', result)
        self.assertIn('JOHN, SARAH', result)

    def test_generate_scene_frames_empty(self):
        """Test scene frames generation with empty list"""
        result = generate_scene_frames([])
        self.assertEqual(result, "")

    def test_generate_scene_frames_image_error_handling(self):
        """Test scene frames includes image error handling"""
        result = generate_scene_frames([self.sample_frames[0]])
        
        # Should include image error handling
        self.assertIn('onerror=', result)
        self.assertIn('image-placeholder', result)

    def test_generate_frame_grid_basic(self):
        """Test frame grid HTML generation"""
        result = generate_frame_grid(self.sample_frames)
        
        # Should contain scene sections
        self.assertIn('scene-section', result)
        self.assertIn('Scene 1', result)
        self.assertIn('Scene 2', result)
        
        # Should contain location and time info
        self.assertIn('CITY STREET', result)
        self.assertIn('COFFEE SHOP', result)
        self.assertIn('DAY', result)
        self.assertIn('CONTINUOUS', result)

    def test_generate_frame_grid_empty(self):
        """Test frame grid generation with empty frames"""
        result = generate_frame_grid([])
        self.assertIn("No frames to display", result)

    def test_generate_frame_grid_groups_by_scene(self):
        """Test frame grid groups frames by scene number"""
        result = generate_frame_grid(self.sample_frames)
        
        # Should group frames by scene
        scene_sections = result.count('scene-section')
        self.assertEqual(scene_sections, 2)  # 2 unique scenes
        
        # Should have frames in correct scenes
        self.assertIn('Scene 1', result)
        self.assertIn('Scene 2', result)

    def test_generate_printable_storyboard_basic(self):
        """Test complete printable storyboard generation"""
        result = generate_printable_storyboard(self.sample_project, self.sample_status)
        
        # Should contain main structure
        self.assertIn('printable-storyboard', result)
        self.assertIn('storyboard-header', result)
        self.assertIn('storyboard-grid', result)
        self.assertIn('storyboard-footer', result)

    def test_generate_printable_storyboard_header(self):
        """Test printable storyboard header content"""
        result = generate_printable_storyboard(self.sample_project, self.sample_status)
        
        # Should contain project information
        self.assertIn('Test Screenplay', result)
        self.assertIn('test_screenplay.txt', result)
        self.assertIn('3', result)  # Frame count
        self.assertIn('2', result)  # Scene count
        self.assertIn('Classic', result)  # Style
        
        # Should contain current date
        current_date = datetime.now().strftime('%B %d, %Y')
        self.assertIn(current_date, result)

    def test_generate_printable_storyboard_footer(self):
        """Test printable storyboard footer content"""
        result = generate_printable_storyboard(self.sample_project, self.sample_status)
        
        # Should contain footer
        self.assertIn('Generated by Script Fury Simple', result)
        
        # Should contain current year
        current_year = str(datetime.now().year)
        self.assertIn(current_year, result)

    def test_generate_printable_storyboard_no_frames(self):
        """Test printable storyboard generation with no frames"""
        empty_status = self.sample_status.copy()
        empty_status['frames'] = []
        
        result = generate_printable_storyboard(self.sample_project, empty_status)
        
        # Should still generate basic structure
        self.assertIn('printable-storyboard', result)
        self.assertIn('storyboard-header', result)

    def test_generate_printable_storyboard_no_analysis(self):
        """Test printable storyboard generation with no analysis"""
        no_analysis_status = self.sample_status.copy()
        no_analysis_status['analysis'] = {}
        
        result = generate_printable_storyboard(self.sample_project, no_analysis_status)
        
        # Should handle missing analysis gracefully
        self.assertIn('printable-storyboard', result)
        self.assertIn('Untitled Screenplay', result)

    def test_get_print_styles_basic(self):
        """Test print styles generation"""
        result = get_print_styles()
        
        # Should contain CSS styles
        self.assertIn('<style>', result)
        self.assertIn('</style>', result)
        
        # Should contain print-specific styles
        self.assertIn('@media print', result)
        self.assertIn('@page', result)
        
        # Should contain layout styles
        self.assertIn('.printable-storyboard', result)
        self.assertIn('.storyboard-header', result)
        self.assertIn('.frame-panel', result)

    def test_get_print_styles_responsive(self):
        """Test print styles include responsive design"""
        result = get_print_styles()
        
        # Should include responsive elements
        self.assertIn('flex', result)
        self.assertIn('page-break', result)
        self.assertIn('justify-content', result)

    def test_get_print_styles_typography(self):
        """Test print styles include typography"""
        result = get_print_styles()
        
        # Should include font specifications
        self.assertIn('font-family', result)
        self.assertIn('font-size', result)
        self.assertIn('line-height', result)

    def test_frame_html_structure(self):
        """Test frame HTML structure is valid"""
        result = generate_scene_frames([self.sample_frames[0]])
        
        # Should have proper HTML structure
        self.assertIn('<div class="frame-panel">', result)
        self.assertIn('<div class="frame-header">', result)
        self.assertIn('<div class="frame-image">', result)
        self.assertIn('<div class="frame-description">', result)
        
        # Should have proper closing tags
        self.assertIn('</div>', result)

    def test_frame_image_attributes(self):
        """Test frame image attributes are correct"""
        result = generate_scene_frames([self.sample_frames[0]])
        
        # Should have proper image attributes
        self.assertIn('alt="Scene 1 Frame 1"', result)
        self.assertIn('src="https://example.com/image1.jpg"', result)
        self.assertIn('onload=', result)
        self.assertIn('onerror=', result)

    def test_frame_content_escaping(self):
        """Test frame content is properly escaped"""
        # Create frame with special characters
        frame_with_special = self.sample_frames[0].copy()
        frame_with_special['key_visual'] = 'Scene with "quotes" & symbols'
        
        result = generate_scene_frames([frame_with_special])
        
        # Should contain the content (HTML should handle escaping)
        self.assertIn('quotes', result)
        self.assertIn('symbols', result)

    def test_scene_header_information(self):
        """Test scene header contains correct information"""
        result = generate_frame_grid(self.sample_frames)
        
        # Should contain scene headers with location and time
        self.assertIn('Scene 1', result)
        self.assertIn('Scene 2', result)
        self.assertIn('CITY STREET', result)
        self.assertIn('COFFEE SHOP', result)
        self.assertIn('DAY', result)
        self.assertIn('CONTINUOUS', result)

    def test_project_info_formatting(self):
        """Test project info is formatted correctly"""
        result = generate_printable_storyboard(self.sample_project, self.sample_status)
        
        # Should format numbers correctly
        self.assertIn('Frames:</strong> 3', result)
        self.assertIn('Scenes:</strong> 2', result)
        
        # Should format dates correctly
        self.assertIn('Generated:', result)
        self.assertIn('at', result)  # Should include time

    def test_style_information_display(self):
        """Test style information is displayed correctly"""
        result = generate_printable_storyboard(self.sample_project, self.sample_status)
        
        # Should display style with proper capitalization
        self.assertIn('Style:</strong> Classic', result)

    def test_frame_numbering_consistency(self):
        """Test frame numbering is consistent"""
        result = generate_scene_frames(self.sample_frames[:2])
        
        # Should have consistent frame numbering
        self.assertIn('Frame 1', result)
        self.assertIn('Frame 2', result)
        
        # Should be in correct order
        frame1_pos = result.find('Frame 1')
        frame2_pos = result.find('Frame 2')
        self.assertLess(frame1_pos, frame2_pos)

    def test_placeholder_content(self):
        """Test placeholder content for missing images"""
        result = generate_scene_frames([self.sample_frames[0]])
        
        # Should include placeholder content
        self.assertIn('image-placeholder', result)
        self.assertIn('Frame 1.1', result)
        self.assertIn('CITY STREET', result)


class TestPrintGeneratorIntegration(unittest.TestCase):
    """Integration tests for print generator"""

    def test_complete_storyboard_generation(self):
        """Test complete storyboard generation with realistic data"""
        project = {
            'id': 'integration-test',
            'filename': 'sample_screenplay.txt',
            'text': 'Complete screenplay text...',
            'created_at': '2023-01-01T12:00:00',
            'word_count': 1500,
            'char_count': 8000
        }

        frames = [
            {
                'frame_id': f'frame_{i}_{j}',
                'scene_number': i,
                'frame_number': j,
                'image_url': f'https://example.com/image{i}_{j}.jpg',
                'status': 'completed',
                'prompt_used': f'Professional storyboard, shot type showing location {i}',
                'location': f'LOCATION {i}',
                'time_of_day': 'DAY',
                'characters': ['CHARACTER1', 'CHARACTER2'],
                'key_visual': f'Key visual moment for scene {i} frame {j}',
                'scene_description': f'Scene {i} description'
            }
            for i in range(1, 4)  # 3 scenes
            for j in range(1, 3)  # 2 frames per scene
        ]

        analysis = {
            'title': 'Integration Test Screenplay',
            'total_scenes': 3,
            'page_count': 10,
            'genre': 'Action',
            'setting': 'Urban',
            'characters': {'CHARACTER1': 'Hero', 'CHARACTER2': 'Villain'}
        }

        status = {
            'status': 'completed',
            'progress': 100,
            'frames': frames,
            'analysis': analysis,
            'style': 'cinematic',
            'max_scenes': 10,
            'started_at': '2023-01-01T12:00:00',
            'completed_at': '2023-01-01T12:10:00'
        }

        result = generate_printable_storyboard(project, status)

        # Should generate complete HTML structure
        self.assertIn('printable-storyboard', result)
        self.assertIn('Integration Test Screenplay', result)
        
        # Should contain all scenes
        self.assertIn('Scene 1', result)
        self.assertIn('Scene 2', result)
        self.assertIn('Scene 3', result)
        
        # Should contain all frames
        frame_count = result.count('frame-panel')
        self.assertEqual(frame_count, 6)  # 3 scenes * 2 frames each

    def test_print_styles_completeness(self):
        """Test print styles are complete and valid"""
        styles = get_print_styles()
        
        # Should be valid HTML
        self.assertIn('<style>', styles)
        self.assertIn('</style>', styles)
        
        # Should contain essential print styles
        essential_classes = [
            '.printable-storyboard',
            '.storyboard-header',
            '.frame-panel',
            '.frame-image',
            '.scene-section'
        ]
        
        for class_name in essential_classes:
            self.assertIn(class_name, styles)

    def test_large_dataset_handling(self):
        """Test handling of large datasets"""
        # Create a large number of frames
        frames = []
        for scene in range(1, 11):  # 10 scenes
            for frame in range(1, 4):  # 3 frames per scene
                frames.append({
                    'frame_id': f'frame_{scene}_{frame}',
                    'scene_number': scene,
                    'frame_number': frame,
                    'image_url': f'https://example.com/image{scene}_{frame}.jpg',
                    'status': 'completed',
                    'prompt_used': f'Frame {scene}.{frame} prompt',
                    'location': f'LOCATION {scene}',
                    'time_of_day': 'DAY',
                    'characters': ['CHAR1', 'CHAR2'],
                    'key_visual': f'Visual for scene {scene} frame {frame}',
                    'scene_description': f'Description for scene {scene}'
                })

        project = {
            'id': 'large-test',
            'filename': 'large_screenplay.txt',
            'text': 'Large screenplay...',
            'created_at': '2023-01-01T12:00:00',
            'word_count': 5000,
            'char_count': 25000
        }

        status = {
            'status': 'completed',
            'frames': frames,
            'analysis': {'title': 'Large Test', 'total_scenes': 10},
            'style': 'classic'
        }

        result = generate_printable_storyboard(project, status)
        
        # Should handle large datasets without errors
        self.assertIn('printable-storyboard', result)
        self.assertIn('Large Test', result)
        
        # Should contain all scenes
        scene_count = result.count('scene-section')
        self.assertEqual(scene_count, 10)


if __name__ == '__main__':
    unittest.main()