"""
AI-powered screenplay scene analysis
Uses OpenAI to properly extract scenes, characters, and analysis like the main app
"""

import re
import os
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from openai import AsyncOpenAI
from .model_config import get_model_for_task

def analyze_screenplay(text: str, max_scenes: int = None) -> Dict[str, Any]:
    """
    Analyze screenplay and extract scenes using AI
    
    Args:
        text: Screenplay text
        max_scenes: Maximum number of scenes to extract (None = auto-detect)
        
    Returns:
        Analysis dict with title, scenes, and metadata
    """
    
    # Auto-detect optimal scene count if not specified
    if max_scenes is None:
        max_scenes = detect_optimal_scene_count(text)
    
    # Use AI to extract comprehensive analysis
    try:
        # Use AI to extract comprehensive analysis in background thread
        import concurrent.futures
        import threading
        
        print(f"🤖 Starting AI analysis for {max_scenes} scenes...")
        
        # Calculate timeout based on script size (more time for larger scripts)
        word_count = len(text.split())
        if word_count > 20000:  # Very large script (like 21 Jump Street)
            timeout = 120  # 2 minutes
        elif word_count > 15000:  # Large script
            timeout = 90
        elif word_count > 8000:  # Medium script  
            timeout = 60
        else:  # Small script
            timeout = 30
            
        print(f"📏 Script size: {word_count} words, using {timeout}s timeout")
        
        # Run AI analysis in separate thread to prevent blocking Flask main thread
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_ai_analysis_sync, text, max_scenes)
            
            # Set dynamic timeout based on script size
            try:
                analysis = future.result(timeout=timeout)
                print(f"✅ AI analysis complete: {analysis.get('total_scenes', 0)} scenes")
                return analysis
            except concurrent.futures.TimeoutError:
                print(f"❌ AI analysis timed out after {timeout} seconds - falling back to basic analysis")
                # Don't raise exception, fall through to basic analysis
                
    except Exception as e:
        print(f"AI analysis failed: {e}")
        # Fallback to basic analysis
        return basic_analyze_screenplay(text, max_scenes)

def _run_ai_analysis_sync(text: str, max_scenes: int) -> Dict[str, Any]:
    """
    Helper function to run async AI analysis synchronously in background thread
    FIXED: Proper AsyncOpenAI client cleanup prevents event loop errors
    """
    # Create new event loop for this thread only
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    client = None
    try:
        client = get_openai_client()
        analysis = loop.run_until_complete(
            ai_analyze_screenplay(client, text, max_scenes)
        )
        return analysis
    finally:
        # CRITICAL: Close client connections before closing event loop
        if client:
            try:
                loop.run_until_complete(client.close())
            except Exception as e:
                print(f"⚠️ Client cleanup warning: {e}")
        
        # Always cleanup event loop
        loop.close()

def detect_optimal_scene_count(text: str) -> int:
    """
    Detect optimal scene count based on screenplay analysis.
    Uses industry standard: 1 scene per 2-3 pages for features
    
    OPTIMIZED: Caps scenes for very large scripts to prevent AI overload
    """
    # Estimate pages
    pages = estimate_pages(text)
    word_count = len(text.split())
    
    # Count actual scene headers for comparison  
    scene_headers = count_scene_headers(text)
    
    # OPTIMIZATION: For very large scripts, use stricter limits
    if word_count > 20000:  # Very large script (like 21 Jump Street)
        max_scenes = 15  # Limit to essential scenes only
        print(f"🔧 Large script detected ({word_count} words) - limiting to {max_scenes} essential scenes")
    elif word_count > 15000:  # Large script
        max_scenes = 25
    elif word_count > 8000:  # Medium script
        max_scenes = 35
    else:  # Small script
        max_scenes = 50
    
    # Industry standard: 1 scene per 2-3 pages for features
    # Use conservative page-based calculation as the BASE
    page_based_estimate = max(5, min(pages // 2, max_scenes))
    
    # Use scene headers if reasonable, otherwise use page-based
    if scene_headers > 0 and scene_headers <= page_based_estimate * 1.5:
        # Scene headers seem reasonable
        scene_count = min(scene_headers, max_scenes)
    else:
        # Scene headers are too high or zero, use page-based
        scene_count = page_based_estimate
    
    # Final reasonable limits
    scene_count = max(3, min(scene_count, max_scenes))
    
    print(f"🎯 Detected optimal scene count: {scene_count} (pages: {pages}, headers: {scene_headers}, page_based: {page_based_estimate}, max_allowed: {max_scenes})")
    return scene_count

def count_scene_headers(text: str) -> int:
    """
    Count scene headers using EXACT regex patterns from main app
    Copied from: src/screenplay_storyboard/parser/extractors/scene_extractor.py
    """
    import re
    
    lines = text.split('\n')
    count = 0
    
    # EXACT patterns from main app's _extract_scenes_with_regex
    patterns = [
        r'^\s*(INT\.|INTERIOR)\s+(.+?)\s*[-–—]\s*(.+)$',
        r'^\s*(EXT\.|EXTERIOR)\s+(.+?)\s*[-–—]\s*(.+)$', 
        r'^\s*(INT/EXT\.|INT\./EXT\.)\s+(.+?)\s*[-–—]\s*(.+)$',
        r'^\s*(I/E\.?)\s+(.+?)\s*[-–—]\s*(.+)$',
        # Handle cases without dashes
        r'^\s*(INT\.|INTERIOR)\s+(.+?)\s+(DAY|NIGHT|DAWN|DUSK|MORNING|AFTERNOON|EVENING|CONTINUOUS|LATER).*$',
        r'^\s*(EXT\.|EXTERIOR)\s+(.+?)\s+(DAY|NIGHT|DAWN|DUSK|MORNING|AFTERNOON|EVENING|CONTINUOUS|LATER).*$',
    ]
    
    for line in lines:
        line_stripped = line.strip()
        if line_stripped:
            for pattern in patterns:
                match = re.match(pattern, line_stripped, re.IGNORECASE)
                if match:
                    count += 1
                    break
    
    return count

def get_openai_client() -> AsyncOpenAI:
    """Get OpenAI client with API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return AsyncOpenAI(api_key=api_key)

async def ai_analyze_screenplay(client: AsyncOpenAI, text: str, max_scenes: int) -> Dict[str, Any]:
    """
    Use AI to analyze screenplay like the main app
    """
    
    # Step 1: Extract basic info using configured model
    info_response = await client.chat.completions.create(
        model=get_model_for_task('basic_info_extraction'),
        messages=[
            {
                "role": "system",
                "content": """You are a screenplay analysis expert. Extract basic information from the screenplay text.

Return a JSON object with:
- title: The screenplay title
- genre: The genre (Drama, Action, Comedy, etc.)
- setting: Primary setting/location
- page_count: Estimated page count
- runtime_estimate: Estimated runtime in minutes
- themes: Array of main themes"""
            },
            {
                "role": "user",
                "content": f"Analyze this screenplay:\n\n{text[:3000]}..."
            }
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        import json
        basic_info = json.loads(info_response.choices[0].message.content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse AI response as JSON: {e}")
        raise Exception("Invalid JSON response from OpenAI API")
    
    # Step 2: Extract scenes using configured model
    scenes_response = await client.chat.completions.create(
        model=get_model_for_task('scene_analysis'),
        messages=[
            {
                "role": "system",
                "content": f"""You are a screenplay scene expert. Extract the {max_scenes} most important scenes for storyboarding.

Return a JSON object with a "scenes" array. Each scene should have:
- scene_number: Integer scene number
- slug_line: Scene header (EXT./INT. LOCATION - TIME)
- location: Location name
- time_of_day: Time of day
- description: Scene description
- key_visual_moment: Most important visual moment
- characters: Array of character names present
- dialogue: Array of key dialogue lines
- camera_angles: Suggested camera angles
- mood: Scene mood/tone
- importance: 1-10 importance score for storyboarding

Focus on visually interesting and story-critical scenes."""
            },
            {
                "role": "user",
                "content": f"Extract scenes from this screenplay:\n\n{text}"
            }
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        scenes_data = json.loads(scenes_response.choices[0].message.content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse scenes AI response as JSON: {e}")
        raise Exception("Invalid JSON response for scenes from OpenAI API")
    
    # Step 3: Extract characters using configured model
    characters_response = await client.chat.completions.create(
        model=get_model_for_task('character_extraction'),
        messages=[
            {
                "role": "system",
                "content": """You are a character analysis expert. Extract main characters with detailed visual descriptions.

Return a JSON object with a "characters" object where each key is a character name and the value is their detailed visual description for storyboard consistency.

Focus on:
- Physical appearance
- Clothing/costume
- Distinctive features
- Age and build
- Personality traits that affect appearance"""
            },
            {
                "role": "user",
                "content": f"Extract characters from this screenplay:\n\n{text}"
            }
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        characters_data = json.loads(characters_response.choices[0].message.content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse characters AI response as JSON: {e}")
        raise Exception("Invalid JSON response for characters from OpenAI API")
    
    # Calculate accurate frame totals
    scenes_list = scenes_data.get('scenes', [])
    total_frames = 0
    
    # Ensure each scene has proper frame count
    for scene in scenes_list:
        frames_needed = scene.get('frames_needed', 1)
        # Validate frames_needed is reasonable (1-3)
        if not isinstance(frames_needed, int) or frames_needed < 1 or frames_needed > 3:
            frames_needed = 1
            scene['frames_needed'] = frames_needed
        total_frames += frames_needed
    
    # Combine all analysis
    analysis = {
        'title': basic_info.get('title', 'Unknown Title'),
        'genre': basic_info.get('genre', 'Unknown'),
        'setting': basic_info.get('setting', 'Various Locations'),
        'themes': basic_info.get('themes', ['Drama']),
        'page_count': basic_info.get('page_count', estimate_pages(text)),
        'runtime_estimate': basic_info.get('runtime_estimate', 90),
        'total_scenes': len(scenes_list),
        'total_frames': total_frames,
        'scenes': scenes_list,
        'characters': characters_data.get('characters', {}),
        'word_count': len(text.split()),
        'analyzed_at': datetime.now().isoformat(),
        'analysis_type': 'AI-powered'
    }
    
    return analysis

def basic_analyze_screenplay(text: str, max_scenes: int) -> Dict[str, Any]:
    """
    Fallback basic analysis when AI fails
    Uses minimal analysis without pattern matching
    """
    
    # Extract basic info
    title = extract_title(text)
    scenes = extract_scenes(text, max_scenes)
    
    # No character extraction in fallback to avoid garbage
    # Users should fix their API configuration instead
    characters_dict = {
        'MAIN CHARACTER': {
            'description': 'Primary character in the story',
            'distinctive_features': 'To be determined by proper AI analysis',
            'clothing': 'Appropriate for story context',
            'role': 'protagonist'
        }
    }
    
    print("⚠️ Using basic fallback analysis - character extraction disabled")
    print("   Please ensure your AI configuration is working for better results")
    
    analysis = {
        'title': title,
        'total_scenes': len(scenes),
        'scenes': scenes,
        'characters': characters_dict,
        'page_count': estimate_pages(text),
        'word_count': len(text.split()),
        'analyzed_at': datetime.now().isoformat(),
        'genre': 'Unknown',
        'setting': extract_primary_setting(scenes),
        'themes': ['Action', 'Drama'],
        'analysis_type': 'Basic fallback'
    }
    
    return analysis

def extract_title(text: str) -> str:
    """Extract screenplay title"""
    lines = text.split('\n')
    
    # Look for title in first few lines
    skip_next = False
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Skip lines after "WRITTEN BY"
        if skip_next:
            skip_next = False
            continue
            
        # Skip common screenplay elements
        if any(keyword in line.upper() for keyword in [
            'FADE IN', 'DRAFT', 'TREATMENT', 'LOGLINE', 'FADE OUT'
        ]):
            continue
            
        # Skip "WRITTEN BY" and next line
        if 'WRITTEN BY' in line.upper() or line.upper() == 'BY':
            skip_next = True
            continue
            
        # Skip scene headers
        if line.upper().startswith(('INT.', 'EXT.', 'FADE')):
            continue
            
        # If it's a substantial line that looks like a title
        if len(line) > 3 and line.isupper():
            # Remove common formatting
            title = line.replace(':', '').replace('"', '').strip()
            if title and not any(char.islower() for char in title):
                return title
    
    return "Untitled Screenplay"

def extract_scenes(text: str, max_scenes: int) -> List[Dict[str, Any]]:
    """Extract scenes from screenplay"""
    scenes = []
    lines = text.split('\n')
    
    current_scene = None
    current_description = []
    scene_number = 0
    
    for line in lines:
        line = line.strip()
        
        # Check if this is a scene header
        if is_scene_header(line):
            # Save previous scene if exists
            if current_scene and len(scenes) < max_scenes:
                current_scene['description'] = '\n'.join(current_description).strip()
                current_scene['key_visual_moment'] = extract_key_visual(current_scene['description'])
                scenes.append(current_scene)
            
            # Start new scene
            if len(scenes) < max_scenes:
                scene_number += 1
                current_scene = {
                    'scene_number': scene_number,
                    'slug_line': line,
                    'location': extract_location(line),
                    'time_of_day': extract_time_of_day(line),
                    'description': '',
                    'key_visual_moment': '',
                    'characters': [],
                    'dialogue': [],
                    'camera_angles': ['medium shot', 'wide shot', 'close-up'],
                    'mood': 'neutral',
                    'importance': 5
                }
                current_description = []
        
        elif current_scene and len(scenes) < max_scenes:
            # Add to current scene description
            if line and not is_character_name(line):
                current_description.append(line)
            elif is_character_name(line):
                # Add character to scene
                char_name = line.strip()
                if char_name not in current_scene['characters']:
                    current_scene['characters'].append(char_name)
    
    # Add final scene
    if current_scene and len(scenes) < max_scenes:
        current_scene['description'] = '\n'.join(current_description).strip()
        current_scene['key_visual_moment'] = extract_key_visual(current_scene['description'])
        scenes.append(current_scene)
    
    return scenes

def is_scene_header(line: str) -> bool:
    """Check if line is a scene header"""
    line = line.strip().upper()
    return (
        line.startswith(('INT.', 'EXT.', 'INTERIOR', 'EXTERIOR')) or
        re.match(r'^(INT|EXT)\.?\s+', line) is not None
    )

def extract_location(scene_header: str) -> str:
    """Extract location from scene header"""
    # Remove INT./EXT. and time
    header = scene_header.strip()
    
    # Pattern: INT./EXT. LOCATION - TIME
    match = re.match(r'^(INT|EXT)\.?\s+([^-]+?)(?:\s*-\s*(.+))?$', header, re.IGNORECASE)
    
    if match:
        location = match.group(2).strip()
        return location
    
    # Fallback - just remove INT/EXT
    for prefix in ['INT.', 'EXT.', 'INTERIOR', 'EXTERIOR']:
        if header.upper().startswith(prefix):
            location = header[len(prefix):].strip()
            if ' - ' in location:
                location = location.split(' - ')[0].strip()
            return location
    
    return header

def extract_time_of_day(scene_header: str) -> str:
    """Extract time of day from scene header"""
    header = scene_header.strip().upper()
    
    # Common time indicators
    time_indicators = ['DAY', 'NIGHT', 'DAWN', 'DUSK', 'MORNING', 'AFTERNOON', 'EVENING', 'CONTINUOUS']
    
    for time_indicator in time_indicators:
        if time_indicator in header:
            return time_indicator
    
    # Look for pattern after dash
    if ' - ' in header:
        time_part = header.split(' - ', 1)[1].strip()
        return time_part if time_part else 'DAY'
    
    return 'DAY'

def extract_key_visual(description: str) -> str:
    """Extract key visual moment from scene description"""
    if not description:
        return "Scene establishing shot"
    
    # Take first substantial sentence
    sentences = re.split(r'[.!?]+', description)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:  # Substantial sentence
            # Truncate if too long
            if len(sentence) > 100:
                return sentence[:100].strip() + "..."
            return sentence
    
    # Fallback to first 100 characters
    return description[:100].strip() + "..." if len(description) > 100 else description

def extract_characters(text: str) -> List[str]:
    """
    DEPRECATED: Old pattern matching character extraction
    This function is disabled in favor of pure AI-based extraction
    """
    print("⚠️ DEPRECATED: Pattern matching character extraction disabled")
    print("   Using AI-based extraction only for better accuracy")
    return []  # Return empty list to prevent garbage extraction

def is_character_name(line: str) -> bool:
    """
    DEPRECATED: Old pattern matching character detection
    This function is disabled in favor of pure AI-based extraction
    """
    print("⚠️ DEPRECATED: Pattern matching character detection disabled")
    return False  # Always return False to prevent garbage extraction

def clean_character_name(line: str) -> str:
    """
    DEPRECATED: Old pattern matching character name cleaning
    This function is disabled in favor of pure AI-based extraction
    """
    print("⚠️ DEPRECATED: Pattern matching character cleaning disabled")
    return ""  # Return empty string to prevent garbage extraction

def extract_primary_setting(scenes: List[Dict[str, Any]]) -> str:
    """Extract primary setting from scenes"""
    if not scenes:
        return "Unknown"
    
    locations = [scene['location'] for scene in scenes]
    
    # Find most common location type
    location_counts = {}
    for location in locations:
        location_counts[location] = location_counts.get(location, 0) + 1
    
    if location_counts:
        primary_location = max(location_counts, key=location_counts.get)
        return primary_location
    
    return "Various Locations"

def estimate_pages(text: str) -> int:
    """
    Estimate screenplay pages using industry standards.
    Standard screenplay format: ~55 lines per page (including blanks)
    or ~250 words per page for dialogue-heavy scripts.
    """
    if not text:
        return 0
    
    lines = text.split('\n')
    words = text.split()
    
    # Method 1: Line-based estimation (standard screenplay format)
    # Standard format: ~55 lines per page (including blanks for formatting)
    line_based_pages = max(1, len(lines) // 55)
    
    # Method 2: Word-based estimation (for dialogue-heavy scripts)
    # Standard: ~250 words per page in screenplay format
    word_based_pages = max(1, len(words) // 250)
    
    # Use the higher estimate for better accuracy (scripts vary in format)
    estimated_pages = max(line_based_pages, word_based_pages)
    
    # Reasonable bounds (minimum 1 page)
    return max(1, estimated_pages)

def fast_ai_analyze_screenplay(text: str, detected_scenes: int) -> Dict[str, Any]:
    """
    FIXED: Fast targeted AI analysis with proper client cleanup
    Uses AI to properly extract characters, story beats, and settings
    """
    # Run async analysis
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    client = None
    try:
        # Get OpenAI client
        client = get_openai_client()
        
        analysis = loop.run_until_complete(
            fast_ai_extract_for_generation(client, text, detected_scenes)
        )
        
        return analysis
        
    except Exception as e:
        print(f"❌ Fast AI analysis failed: {e}")
        print("   Falling back to basic analysis...")
        # Fallback to basic analysis
        return basic_analyze_screenplay(text, detected_scenes)
    finally:
        # CRITICAL: Close client connections before closing event loop
        if client:
            try:
                loop.run_until_complete(client.close())
            except Exception as e:
                print(f"⚠️ Client cleanup warning: {e}")
        
        # Always cleanup event loop
        loop.close()

async def fast_ai_extract_for_generation(client: AsyncOpenAI, text: str, max_scenes: int) -> Dict[str, Any]:
    """
    Fast targeted AI extraction for generation flow
    Focuses on characters, story beats, and settings - not redundant scene detection
    
    OPTIMIZED for large scripts: Limits text sent to AI to prevent hanging
    """
    
    # IMPROVED: Smart text sampling for character extraction - use FULL script for better character detection
    word_count = len(text.split())
    if word_count > 20000:
        # For very large scripts, use strategic sampling: beginning + middle + end
        words = text.split()
        beginning = words[:5000]
        middle_start = len(words) // 2 - 2000
        middle = words[middle_start:middle_start + 4000]
        end = words[-3000:]
        text_sample = ' '.join(beginning + ['...MIDDLE SECTION...'] + middle + ['...FINAL SECTION...'] + end)
        print(f"🔧 Large script optimization: Using {len(text_sample.split())} words from {word_count} total (beginning+middle+end)")
    elif word_count > 10000:
        # For medium scripts, use first 8000 words (more than before)
        words = text.split()
        text_sample = ' '.join(words[:8000]) + '...TRUNCATED...'
        print(f"🔧 Medium script optimization: Using {len(text_sample.split())} words from {word_count} total")
    else:
        # Small scripts - use full text (no change)
        text_sample = text
        print(f"📝 Using full script: {word_count} words")
    
    # Step 1: Extract ALL characters using INTELLIGENT AI analysis - NO REGEX FALLBACKS
    characters_response = await client.chat.completions.create(
        model=get_model_for_task('character_extraction'),
        messages=[
            {
                "role": "system",
                "content": """You are an expert screenplay character analyst. Extract ONLY actual human character names from this screenplay.

🚫 DO NOT EXTRACT:
- Sound effects: "AAAAAH!", "AAAAARGH!", "WOOOOOOOOOOOOOO!"
- Dialogue content: "FUCK YEAH!", "I LOVE YOU!", "STOP!"
- Locations: "AUDITORIUM", "SCHOOL", "CAFETERIA"
- Organizations: "LAPD", "SWAT", "FBI"
- Objects: "NUNCHUCKS", "PHONE", "CAR"
- Random text: "END OF MESSAGE", "21 JUMP STREET", "OUT"
- Camera directions: "C/U", "POV", "EXT", "INT"
- Time stamps: "DAY", "NIGHT", "LATER"
- Punctuation-only: "YEP.", "STINKS.", "DRIVE!"

✅ ONLY EXTRACT actual human character names that:
- Are proper names of people (first name, last name, or both)
- Have speaking roles or perform actions
- Are referenced as characters in the story
- Are human beings, not objects or sounds

INTELLIGENCE RULES:
- "JENKO" = character ✅
- "SCHMIDT" = character ✅  
- "CAPTAIN DICKS" = character ✅
- "AAAAAH!" = sound effect ❌
- "LAPD!" = organization ❌
- "AUDITORIUM." = location ❌

Return a JSON object with:
- "characters": object where each key is a character name and value is an object with:
  - "description": Brief physical description (age, build, key features)
  - "distinctive_features": Most recognizable visual elements (glasses, beard, clothing style)
  - "clothing": Typical clothing/costume if mentioned
  - "role": Character's role in story (protagonist, antagonist, supporting, etc.)

Be VERY selective. Only include actual human character names."""
            },
            {
                "role": "user", 
                "content": f"Extract ONLY actual human character names from this screenplay:\n\n{text_sample}"
            }
        ],
        response_format={"type": "json_object"}
    )
    
    # Step 2: INTELLIGENT scene detection with variable frames per scene using configured model
    story_response = await client.chat.completions.create(
        model=get_model_for_task('scene_analysis'),
        messages=[
            {
                "role": "system",
                "content": f"""You are an expert storyboard director and story analyst. Analyze this screenplay and intelligently select the {max_scenes} most important scenes for storyboarding.

INTELLIGENCE RULES:
1. **Scene Types & Frame Requirements:**
   - Action sequences: 2 frames (setup + action)
   - Dialogue scenes: 1 frame (single shot sufficient)
   - Establishing shots: 1 frame (wide establishing)
   - Emotional beats: 1 frame (reaction/emotion)
   - Transitions: 1 frame (single transition)
   - Climactic moments: 2 frames (buildup + climax)
   - Repetitive actions: 1 frame (avoid duplicates)

2. **Genre Considerations:**
   - Action films: Focus on stunts, fights, chases
   - Drama: Focus on emotional moments, character reactions  
   - Comedy: Focus on visual gags, reactions
   - Thriller: Focus on tension, reveals
   - Horror: Focus on scares, atmosphere

3. **Story Structure Priority:**
   - Opening (setup): HIGH priority
   - Inciting incident: HIGHEST priority
   - Plot points: HIGH priority  
   - Climax: HIGHEST priority
   - Resolution: MEDIUM priority
   - Exposition scenes: LOW priority

Return a JSON object with:
- "scenes": array of scene objects with:
  - scene_number: integer
  - slug_line: scene header (EXT./INT. LOCATION - TIME)
  - location: location name
  - time_of_day: time of day
  - description: scene description
  - key_visual_moment: most important visual moment
  - characters: array of ONLY actual human character names present (NO sound effects, locations, or organizations)
  - story_beat: what happens in the story (setup, inciting_incident, plot_point_1, midpoint, plot_point_2, climax, resolution)
  - scene_type: type of scene (action, dialogue, establishing, emotional, transition, climax)
  - importance: 1-10 importance for storyboarding
  - frames_needed: 1-3 frames needed for this scene
  - mood: emotional tone
  - camera_angles: suggested camera angles for storyboard
  - visual_complexity: simple/medium/complex

CRITICAL for "characters" array: Only include actual human character names, NOT:
- Sound effects: "AAAAAH!", "WOOOOOO!"
- Locations: "AUDITORIUM", "SCHOOL"
- Organizations: "LAPD", "SWAT"
- Objects: "NUNCHUCKS", "PHONE"
- Random text: "END OF MESSAGE", "OUT"

Focus on scenes that tell the story visually and require multiple angles or have high dramatic impact.

CRITICAL: Avoid repetitive scenes. If a character "realizes something" or "discovers something", use only 1 frame. Don't create multiple frames for the same realization or simple actions."""
            },
            {
                "role": "user",
                "content": f"Analyze this screenplay and select the most important scenes for storyboarding:\n\n{text_sample}"
            }
        ],
        response_format={"type": "json_object"}
    )
    
    # Parse responses
    import json
    try:
        characters_data = json.loads(characters_response.choices[0].message.content)
        story_data = json.loads(story_response.choices[0].message.content)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse AI response: {e}")
        raise Exception("Invalid JSON response from OpenAI API")
    
    # PURE AI-BASED CHARACTER EXTRACTION - NO REGEX FALLBACKS
    ai_characters = set(characters_data.get('characters', {}).keys())
    
    # Validate AI results - remove any obvious garbage that slipped through
    validated_characters = {}
    for char_name, char_info in characters_data.get('characters', {}).items():
        # Basic validation - skip obvious garbage
        if (len(char_name) > 1 and 
            not char_name.endswith('!') and 
            not char_name.endswith('.') and
            not char_name.startswith('AAAA') and
            not char_name.startswith('WOOO') and
            not char_name in ['LAPD', 'SWAT', 'FBI', 'OUT', 'STOP', 'DRIVE'] and
            'JUMP STREET' not in char_name):
            validated_characters[char_name] = char_info
        else:
            print(f"🗑️ Filtered out garbage: {char_name}")
    
    # Update with validated characters only
    characters_data['characters'] = validated_characters
    
    print(f"✅ AI-based character extraction complete: {len(validated_characters)} valid characters found")
    
    # Calculate accurate frame totals
    scenes_list = story_data.get('scenes', [])
    total_frames = 0
    
    # Ensure each scene has proper frame count
    for scene in scenes_list:
        frames_needed = scene.get('frames_needed', 1)
        # Validate frames_needed is reasonable (1-3)
        if not isinstance(frames_needed, int) or frames_needed < 1 or frames_needed > 3:
            frames_needed = 1
            scene['frames_needed'] = frames_needed
        total_frames += frames_needed
    
    # Build analysis result with ACCURATE counts
    analysis = {
        'title': extract_title(text),
        'total_scenes': len(scenes_list),
        'total_frames': total_frames,
        'scenes': scenes_list,
        'characters': characters_data.get('characters', {}),
        'page_count': estimate_pages(text),
        'word_count': len(text.split()),
        'analyzed_at': datetime.now().isoformat(),
        'genre': 'Unknown',
        'setting': extract_primary_setting_from_scenes(scenes_list),
        'themes': ['Action', 'Drama'],
        'analysis_type': 'Fast AI-powered'
    }
    
    print(f"✅ Fast AI analysis complete: {len(analysis['characters'])} characters, {analysis['total_scenes']} scenes, {analysis['total_frames']} frames")
    return analysis

def extract_primary_setting_from_scenes(scenes: List[Dict[str, Any]]) -> str:
    """Extract general setting overview from AI-analyzed scenes"""
    if not scenes:
        return "Unknown"
    
    locations = [scene.get('location', 'Unknown') for scene in scenes]
    
    # Categorize locations to get general setting
    interior_locations = []
    exterior_locations = []
    
    for location in locations:
        location_lower = location.lower()
        if any(indoor in location_lower for indoor in ['office', 'room', 'house', 'building', 'interior', 'int.', 'apartment', 'store', 'restaurant', 'bar', 'lab', 'classroom']):
            interior_locations.append(location)
        else:
            exterior_locations.append(location)
    
    # Build general setting description
    setting_parts = []
    
    # Get unique location types
    unique_exteriors = list(set(exterior_locations))
    unique_interiors = list(set(interior_locations))
    
    if unique_exteriors:
        if len(unique_exteriors) == 1:
            setting_parts.append(unique_exteriors[0])
        elif len(unique_exteriors) <= 3:
            setting_parts.append(", ".join(unique_exteriors))
        else:
            # Categorize exterior types
            if any('city' in loc.lower() or 'street' in loc.lower() for loc in unique_exteriors):
                setting_parts.append("Urban environments")
            elif any('school' in loc.lower() or 'campus' in loc.lower() for loc in unique_exteriors):
                setting_parts.append("School campus")
            elif any('canyon' in loc.lower() or 'desert' in loc.lower() or 'mountain' in loc.lower() for loc in unique_exteriors):
                setting_parts.append("Natural landscapes")
            else:
                setting_parts.append("Various outdoor locations")
    
    if unique_interiors:
        if len(unique_interiors) == 1:
            setting_parts.append(unique_interiors[0])
        elif len(unique_interiors) <= 3:
            setting_parts.append(", ".join(unique_interiors))
        else:
            # Categorize interior types
            if any('office' in loc.lower() or 'workplace' in loc.lower() for loc in unique_interiors):
                setting_parts.append("Office/workplace interiors")
            elif any('home' in loc.lower() or 'house' in loc.lower() or 'apartment' in loc.lower() for loc in unique_interiors):
                setting_parts.append("Residential interiors")
            elif any('school' in loc.lower() or 'classroom' in loc.lower() for loc in unique_interiors):
                setting_parts.append("School interiors")
            else:
                setting_parts.append("Various indoor locations")
    
    if setting_parts:
        return " and ".join(setting_parts)
    else:
        return "Various locations"

def extract_character_context(text: str, character: str) -> str:
    """Extract basic visual context for a character from screenplay text"""
    # Look for descriptions near character name mentions
    lines = text.split('\n')
    char_descriptions = []
    
    for i, line in enumerate(lines):
        if character.upper() in line.upper():
            # Look at surrounding lines for descriptions
            context_start = max(0, i - 3)
            context_end = min(len(lines), i + 3)
            context_lines = lines[context_start:context_end]
            
            for context_line in context_lines:
                # Look for descriptive text (usually in parentheses or action lines)
                if any(word in context_line.lower() for word in 
                      ['young', 'old', 'tall', 'short', 'beard', 'hair', 'wearing', 'dressed', 
                       'looks', 'appears', 'age', 'years', 'man', 'woman', 'boy', 'girl']):
                    char_descriptions.append(context_line.strip())
    
    if char_descriptions:
        # Return the most descriptive line
        best_description = max(char_descriptions, key=len)
        return f"Character: {best_description[:100]}..."
    else:
        # Fallback description based on character name
        return f"Character appearing in screenplay: {character}"