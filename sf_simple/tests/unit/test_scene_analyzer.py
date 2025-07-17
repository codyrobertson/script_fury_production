"""
Unit tests for scene_analyzer.py
"""

import unittest
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.scene_analyzer import (
    analyze_screenplay,
    extract_title,
    extract_scenes,
    is_scene_header,
    extract_location,
    extract_time_of_day,
    extract_key_visual,
    extract_characters,
    is_character_name,
    clean_character_name,
    extract_primary_setting,
    estimate_pages
)


class TestSceneAnalyzer(unittest.TestCase):
    """Test cases for scene analysis utilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_screenplay = """
THE TEST SCREENPLAY

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

EXT. POLICE STATION - DAY

John walks up the steps.

FADE OUT.
"""

        self.complex_screenplay = """
THE COMPLEX SCREENPLAY

FADE IN:

EXT. MOUNTAIN RANGE - DAWN

Vast mountains stretch across the horizon. Snow-capped peaks glisten.

ALEX WINTER (40s), a wilderness guide, studies a map.

ALEX
Storm's coming in fast.

MAYA CHEN (30s) approaches with hiking gear.

MAYA
Weather's changing rapidly.

INT. CABIN - NIGHT

Alex and Maya huddle around a fire.

ALEX
We need to get out of here.

MAYA
(worried)
The radio's dead.

EXT. HELICOPTER PAD - DAY

PILOT JONES (50s) checks weather reports.

PILOT JONES
(into radio)
Ground control, requesting 
permission for rescue operation.

FADE OUT.
"""

    def test_extract_title_simple(self):
        """Test title extraction from simple screenplay"""
        title = extract_title(self.sample_screenplay)
        self.assertEqual(title, "THE TEST SCREENPLAY")

    def test_extract_title_with_formatting(self):
        """Test title extraction with formatting characters"""
        screenplay_with_formatting = '"THE MOVIE TITLE:"\n\nFADE IN:'
        title = extract_title(screenplay_with_formatting)
        self.assertEqual(title, "THE MOVIE TITLE")

    def test_extract_title_no_title(self):
        """Test title extraction when no clear title exists"""
        screenplay_no_title = "FADE IN:\n\nEXT. LOCATION - DAY"
        title = extract_title(screenplay_no_title)
        self.assertEqual(title, "Untitled Screenplay")

    def test_extract_title_with_common_elements(self):
        """Test title extraction skips common screenplay elements"""
        screenplay_with_elements = """
WRITTEN BY
JOHN SMITH

THE REAL TITLE

FADE IN:
"""
        title = extract_title(screenplay_with_elements)
        self.assertEqual(title, "THE REAL TITLE")

    def test_is_scene_header_basic(self):
        """Test scene header detection with basic formats"""
        self.assertTrue(is_scene_header("EXT. CITY STREET - DAY"))
        self.assertTrue(is_scene_header("INT. COFFEE SHOP - NIGHT"))
        self.assertTrue(is_scene_header("EXTERIOR. PARK - DAWN"))
        self.assertTrue(is_scene_header("INTERIOR HOUSE - DUSK"))
        self.assertFalse(is_scene_header("JOHN walks down the street"))
        self.assertFalse(is_scene_header("FADE IN:"))

    def test_is_scene_header_variations(self):
        """Test scene header detection with variations"""
        self.assertTrue(is_scene_header("EXT BEACH - DAY"))  # No period
        self.assertTrue(is_scene_header("int. car - night"))  # Lowercase
        self.assertTrue(is_scene_header("EXT. FOREST - CONTINUOUS"))
        self.assertFalse(is_scene_header(""))
        self.assertFalse(is_scene_header("JOHN"))

    def test_extract_location_basic(self):
        """Test location extraction from scene headers"""
        self.assertEqual(extract_location("EXT. CITY STREET - DAY"), "CITY STREET")
        self.assertEqual(extract_location("INT. COFFEE SHOP - NIGHT"), "COFFEE SHOP")
        self.assertEqual(extract_location("EXT. MOUNTAIN RANGE - DAWN"), "MOUNTAIN RANGE")

    def test_extract_location_variations(self):
        """Test location extraction with variations"""
        self.assertEqual(extract_location("EXTERIOR PARK - DAY"), "PARK")
        self.assertEqual(extract_location("EXT BEACH"), "BEACH")
        self.assertEqual(extract_location("INT. HOUSE/KITCHEN - NIGHT"), "HOUSE/KITCHEN")

    def test_extract_time_of_day_basic(self):
        """Test time of day extraction"""
        self.assertEqual(extract_time_of_day("EXT. CITY STREET - DAY"), "DAY")
        self.assertEqual(extract_time_of_day("INT. COFFEE SHOP - NIGHT"), "NIGHT")
        self.assertEqual(extract_time_of_day("EXT. PARK - DAWN"), "DAWN")
        self.assertEqual(extract_time_of_day("INT. HOUSE - DUSK"), "DUSK")

    def test_extract_time_of_day_variations(self):
        """Test time of day extraction with variations"""
        self.assertEqual(extract_time_of_day("EXT. BEACH - MORNING"), "MORNING")
        self.assertEqual(extract_time_of_day("INT. OFFICE - AFTERNOON"), "AFTERNOON")
        self.assertEqual(extract_time_of_day("EXT. STREET - CONTINUOUS"), "CONTINUOUS")

    def test_extract_time_of_day_no_time(self):
        """Test time of day extraction when no time specified"""
        self.assertEqual(extract_time_of_day("EXT. CITY STREET"), "DAY")  # Default

    def test_extract_key_visual_basic(self):
        """Test key visual extraction from descriptions"""
        description = "A bustling urban scene. Cars honk in the distance. People walk quickly."
        visual = extract_key_visual(description)
        self.assertEqual(visual, "A bustling urban scene")

    def test_extract_key_visual_empty(self):
        """Test key visual extraction with empty description"""
        visual = extract_key_visual("")
        self.assertEqual(visual, "Scene establishing shot")

    def test_extract_key_visual_no_sentence(self):
        """Test key visual extraction with no clear sentences"""
        description = "Short"
        visual = extract_key_visual(description)
        self.assertEqual(visual, "Short")

    def test_extract_key_visual_long_description(self):
        """Test key visual extraction with long description"""
        long_description = "This is a very long description that goes on and on and should be truncated when it gets too long for the key visual moment display."
        visual = extract_key_visual(long_description)
        self.assertTrue(len(visual) <= 103)  # Should be truncated with "..."

    def test_is_character_name_basic(self):
        """Test character name detection"""
        self.assertTrue(is_character_name("JOHN"))
        self.assertTrue(is_character_name("SARAH"))
        self.assertTrue(is_character_name("ALEX WINTER"))
        self.assertFalse(is_character_name(""))
        self.assertFalse(is_character_name("a"))
        self.assertFalse(is_character_name("This is a long line that is not a character name"))

    def test_is_character_name_scene_headers(self):
        """Test character name detection excludes scene headers"""
        self.assertFalse(is_character_name("EXT. CITY STREET - DAY"))
        self.assertFalse(is_character_name("INT. COFFEE SHOP"))
        self.assertFalse(is_character_name("FADE IN:"))
        self.assertFalse(is_character_name("FADE OUT"))

    def test_is_character_name_action_lines(self):
        """Test character name detection excludes action indicators"""
        self.assertFalse(is_character_name("CONTINUED"))
        self.assertFalse(is_character_name("CUT TO:"))
        self.assertFalse(is_character_name("DISSOLVE TO:"))

    def test_clean_character_name_basic(self):
        """Test character name cleaning"""
        self.assertEqual(clean_character_name("JOHN"), "JOHN")
        self.assertEqual(clean_character_name("SARAH  "), "SARAH")
        self.assertEqual(clean_character_name("  ALEX  "), "ALEX")

    def test_clean_character_name_parentheticals(self):
        """Test character name cleaning removes parentheticals"""
        self.assertEqual(clean_character_name("JOHN (O.S.)"), "JOHN")
        self.assertEqual(clean_character_name("SARAH (V.O.)"), "SARAH")
        self.assertEqual(clean_character_name("ALEX (CONT'D)"), "ALEX")

    def test_extract_characters_basic(self):
        """Test character extraction from screenplay"""
        characters = extract_characters(self.sample_screenplay)
        self.assertIn("JOHN", characters)
        self.assertIn("SARAH", characters)
        self.assertEqual(len(characters), 2)

    def test_extract_characters_complex(self):
        """Test character extraction from complex screenplay"""
        characters = extract_characters(self.complex_screenplay)
        self.assertIn("ALEX", characters)
        self.assertIn("MAYA", characters)
        self.assertIn("PILOT JONES", characters)
        self.assertEqual(len(characters), 3)

    def test_extract_characters_empty(self):
        """Test character extraction from empty screenplay"""
        characters = extract_characters("")
        self.assertEqual(characters, [])

    def test_extract_scenes_basic(self):
        """Test scene extraction from screenplay"""
        scenes = extract_scenes(self.sample_screenplay, max_scenes=10)
        
        self.assertGreater(len(scenes), 0)
        self.assertEqual(scenes[0]['scene_number'], 1)
        self.assertEqual(scenes[0]['slug_line'], "EXT. CITY STREET - DAY")
        self.assertEqual(scenes[0]['location'], "CITY STREET")
        self.assertEqual(scenes[0]['time_of_day'], "DAY")
        self.assertIn("JOHN", scenes[0]['characters'])

    def test_extract_scenes_max_limit(self):
        """Test scene extraction respects max_scenes limit"""
        scenes = extract_scenes(self.complex_screenplay, max_scenes=2)
        self.assertLessEqual(len(scenes), 2)

    def test_extract_scenes_empty(self):
        """Test scene extraction from empty screenplay"""
        scenes = extract_scenes("", max_scenes=5)
        self.assertEqual(scenes, [])

    def test_extract_primary_setting_basic(self):
        """Test primary setting extraction"""
        scenes = extract_scenes(self.sample_screenplay, max_scenes=10)
        setting = extract_primary_setting(scenes)
        self.assertIsNotNone(setting)
        self.assertNotEqual(setting, "Unknown")

    def test_extract_primary_setting_empty(self):
        """Test primary setting extraction with empty scenes"""
        setting = extract_primary_setting([])
        self.assertEqual(setting, "Unknown")

    def test_estimate_pages_basic(self):
        """Test page estimation"""
        pages = estimate_pages(self.sample_screenplay)
        self.assertGreater(pages, 0)
        self.assertIsInstance(pages, int)

    def test_estimate_pages_empty(self):
        """Test page estimation with empty text"""
        pages = estimate_pages("")
        self.assertEqual(pages, 0)

    def test_analyze_screenplay_basic(self):
        """Test complete screenplay analysis"""
        analysis = analyze_screenplay(self.sample_screenplay, max_scenes=5)
        
        # Check structure
        self.assertIn('title', analysis)
        self.assertIn('total_scenes', analysis)
        self.assertIn('scenes', analysis)
        self.assertIn('characters', analysis)
        self.assertIn('page_count', analysis)
        self.assertIn('word_count', analysis)
        self.assertIn('analyzed_at', analysis)

        # Check content
        self.assertEqual(analysis['title'], "THE TEST SCREENPLAY")
        self.assertGreater(analysis['total_scenes'], 0)
        self.assertGreater(analysis['page_count'], 0)
        self.assertGreater(analysis['word_count'], 0)
        self.assertIn("JOHN", analysis['characters'])
        self.assertIn("SARAH", analysis['characters'])

    def test_analyze_screenplay_complex(self):
        """Test screenplay analysis with complex screenplay"""
        analysis = analyze_screenplay(self.complex_screenplay, max_scenes=10)
        
        self.assertEqual(analysis['title'], "THE COMPLEX SCREENPLAY")
        self.assertGreater(analysis['total_scenes'], 0)
        self.assertIn("ALEX", analysis['characters'])
        self.assertIn("MAYA", analysis['characters'])
        self.assertIn("PILOT JONES", analysis['characters'])

    def test_analyze_screenplay_empty(self):
        """Test screenplay analysis with empty input"""
        analysis = analyze_screenplay("", max_scenes=5)
        
        self.assertEqual(analysis['title'], "Untitled Screenplay")
        self.assertEqual(analysis['total_scenes'], 0)
        self.assertEqual(analysis['scenes'], [])
        self.assertEqual(analysis['characters'], [])
        self.assertEqual(analysis['page_count'], 0)
        self.assertEqual(analysis['word_count'], 0)

    def test_analyze_screenplay_timestamp(self):
        """Test screenplay analysis includes timestamp"""
        analysis = analyze_screenplay(self.sample_screenplay, max_scenes=5)
        
        self.assertIn('analyzed_at', analysis)
        # Should be a valid ISO timestamp
        try:
            datetime.fromisoformat(analysis['analyzed_at'])
        except ValueError:
            self.fail("analyzed_at is not a valid ISO timestamp")

    def test_analyze_screenplay_defaults(self):
        """Test screenplay analysis includes default values"""
        analysis = analyze_screenplay(self.sample_screenplay, max_scenes=5)
        
        self.assertEqual(analysis['genre'], 'Unknown')
        self.assertEqual(analysis['themes'], ['Action', 'Drama'])
        self.assertIn('setting', analysis)

    def test_scenes_have_required_fields(self):
        """Test that extracted scenes have all required fields"""
        scenes = extract_scenes(self.sample_screenplay, max_scenes=10)
        
        for scene in scenes:
            self.assertIn('scene_number', scene)
            self.assertIn('slug_line', scene)
            self.assertIn('location', scene)
            self.assertIn('time_of_day', scene)
            self.assertIn('description', scene)
            self.assertIn('key_visual_moment', scene)
            self.assertIn('characters', scene)
            self.assertIn('dialogue', scene)
            
            # Check data types
            self.assertIsInstance(scene['scene_number'], int)
            self.assertIsInstance(scene['slug_line'], str)
            self.assertIsInstance(scene['location'], str)
            self.assertIsInstance(scene['time_of_day'], str)
            self.assertIsInstance(scene['description'], str)
            self.assertIsInstance(scene['key_visual_moment'], str)
            self.assertIsInstance(scene['characters'], list)
            self.assertIsInstance(scene['dialogue'], list)

    def test_character_extraction_ignores_scene_headers(self):
        """Test that character extraction doesn't include scene headers"""
        screenplay_with_headers = """
EXT. CITY STREET - DAY

JOHN walks down the street.

JOHN
Hello there.

INT. COFFEE SHOP - NIGHT

SARAH serves coffee.

SARAH
Welcome to our shop.
"""
        characters = extract_characters(screenplay_with_headers)
        
        # Should only include character names, not scene headers
        self.assertIn("JOHN", characters)
        self.assertIn("SARAH", characters)
        self.assertNotIn("EXT. CITY STREET - DAY", characters)
        self.assertNotIn("INT. COFFEE SHOP - NIGHT", characters)


class TestSceneAnalyzerIntegration(unittest.TestCase):
    """Integration tests for scene analyzer with fixture files"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')

    def test_analyze_sample_screenplay(self):
        """Test analyzing sample screenplay fixture"""
        sample_file = os.path.join(self.test_dir, 'sample_screenplay.txt')
        if os.path.exists(sample_file):
            with open(sample_file, 'r') as f:
                text = f.read()
            
            analysis = analyze_screenplay(text, max_scenes=10)
            
            # Check expected content
            self.assertEqual(analysis['title'], "THE TEST SCREENPLAY")
            self.assertGreater(analysis['total_scenes'], 0)
            self.assertIn("JOHN", analysis['characters'])
            self.assertIn("SARAH", analysis['characters'])

    def test_analyze_large_screenplay(self):
        """Test analyzing large screenplay fixture"""
        large_file = os.path.join(self.test_dir, 'large_screenplay.txt')
        if os.path.exists(large_file):
            with open(large_file, 'r') as f:
                text = f.read()
            
            analysis = analyze_screenplay(text, max_scenes=10)
            
            # Check expected content
            self.assertEqual(analysis['title'], "LARGE SCREENPLAY TEST")
            self.assertGreater(analysis['total_scenes'], 0)
            self.assertIn("ALEX", analysis['characters'])
            self.assertIn("MAYA", analysis['characters'])

    def test_analyze_malformed_screenplay(self):
        """Test analyzing malformed screenplay fixture"""
        malformed_file = os.path.join(self.test_dir, 'malformed_screenplay.txt')
        if os.path.exists(malformed_file):
            with open(malformed_file, 'r') as f:
                text = f.read()
            
            analysis = analyze_screenplay(text, max_scenes=10)
            
            # Should still work but with limited results
            self.assertIsNotNone(analysis)
            self.assertIn('title', analysis)
            self.assertIn('total_scenes', analysis)
            self.assertIn('scenes', analysis)


if __name__ == '__main__':
    unittest.main()