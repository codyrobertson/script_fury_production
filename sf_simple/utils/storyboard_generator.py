"""
AI-powered storyboard frame generator
Uses OpenAI to generate actual frames like the main app
"""

import time
import random
import os
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from openai import AsyncOpenAI
from dotenv import load_dotenv
from .model_config import get_model_for_task

# Load environment variables
load_dotenv()

def generate_storyboard_frames(analysis: Dict[str, Any], style_prompt: str) -> List[Dict[str, Any]]:
    """
    Generate storyboard frames from analysis using AI
    
    Args:
        analysis: Screenplay analysis
        style_prompt: Style prompt for generation
        
    Returns:
        List of frame dictionaries
    """
    
    # Calculate optimal frames per scene based on scene importance
    frames = []
    
    # Run AI frame generation
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    client = None
    try:
        # Get OpenAI client
        client = get_openai_client()
        
        frames = loop.run_until_complete(
            ai_generate_frames(client, analysis, style_prompt)
        )
        
    except Exception as e:
        print(f"AI frame generation failed: {e}")
        # Fallback to simulated generation
        frames = simulate_frame_generation(analysis, style_prompt)
    finally:
        # CRITICAL: Close client connections before closing event loop
        if client:
            try:
                loop.run_until_complete(client.close())
            except Exception as e:
                print(f"⚠️ Client cleanup warning: {e}")
        
        # Always cleanup event loop
        loop.close()
    
    return frames

def get_openai_client() -> AsyncOpenAI:
    """Get OpenAI client with API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return AsyncOpenAI(api_key=api_key)

async def ai_generate_frames(client: AsyncOpenAI, analysis: Dict[str, Any], style_prompt: str) -> List[Dict[str, Any]]:
    """
    Generate frames using AI like the main app
    """
    frames = []
    
    # Get style DNA (like main app)
    style_dna = get_style_dna(style_prompt)
    
    # Get character database for consistency
    character_database = analysis.get('characters', {})
    
    for scene in analysis['scenes']:
        # Use AI-determined frame count (more conservative)
        frames_per_scene = scene.get('frames_needed', 1)
        
        # Additional safety: Cap at 2 frames max to avoid repetition
        frames_per_scene = min(frames_per_scene, 2)
        
        for frame_num in range(frames_per_scene):
            try:
                # Generate frame using AI with character consistency
                frame = await generate_ai_frame(client, scene, frame_num + 1, style_dna, character_database)
                frames.append(frame)
                
                # Small delay between frames
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"Frame generation failed for scene {scene['scene_number']}: {e}")
                # Fallback to placeholder frame
                frame = generate_placeholder_frame(scene, frame_num + 1, style_prompt)
                frames.append(frame)
    
    return frames

def get_style_dna(style_prompt: str) -> str:
    """
    Get EXACT Style DNA from main Script Fury app with enhanced consistency
    """
    
    # ENHANCED Style DNA - Handles lighting, skin tone, and day/night consistency
    STORYBOARD_STYLE_DNA = {
        "base": "Professional storyboard, black and white line art only",
        "technique": "Clean vector-like lines, no shading, no gradients", 
        "detail": "Minimal detail, focus on clear action and composition",
        "line_weight": "Consistent medium-weight black lines on white background",
        "reference": "Animation studio storyboard style, broadcast quality",
        "no_color": "STRICTLY black and white, no gray values except for subtle shadows",
        "composition": "Wide cinematic framing, clear staging",
        "consistency": "Uniform art style throughout, consistent character proportions, same drawing technique",
        "lighting": "Simple line-based lighting indication, avoid complex shadows or highlights",
        "skin_tone": "All characters drawn with identical line art style, no skin tone variations or shading differences",
        "color_accuracy": "STRICTLY monochrome black and white only, no color bleeding, pure line art",
        "character_consistency": "Same facial features, body proportions, and distinctive clothing throughout all frames",
        "background_simplicity": "Minimal background details, focus on essential environmental elements only",
        "avoid_photorealism": "NO photographic elements, NO realistic rendering, pure line art illustration only"
    }
    
    # Extract style key from prompt
    if 'cinematic' in style_prompt.lower():
        style_key = 'cinematic'
    elif 'sketch' in style_prompt.lower():
        style_key = 'sketch'
    elif 'comic' in style_prompt.lower():
        style_key = 'comic'
    else:
        style_key = 'classic'
    
    # Build complete style DNA with ALL enhanced elements
    base_dna = f"{STORYBOARD_STYLE_DNA['base']}, {STORYBOARD_STYLE_DNA['technique']}, {STORYBOARD_STYLE_DNA['detail']}, {STORYBOARD_STYLE_DNA['reference']}, {STORYBOARD_STYLE_DNA['no_color']}, {STORYBOARD_STYLE_DNA['composition']}, {STORYBOARD_STYLE_DNA['consistency']}, {STORYBOARD_STYLE_DNA['lighting']}, {STORYBOARD_STYLE_DNA['skin_tone']}, {STORYBOARD_STYLE_DNA['color_accuracy']}, {STORYBOARD_STYLE_DNA['character_consistency']}, {STORYBOARD_STYLE_DNA['background_simplicity']}, {STORYBOARD_STYLE_DNA['avoid_photorealism']}"
    
    # Style-specific additions that MAINTAIN all consistency controls
    style_additions = {
        'classic': "",  # Base enhanced DNA is perfect for classic
        'cinematic': ", dramatic composition, film-style framing, CINEMATIC EXCEPTION: allow monochrome grays and gradients for depth, BUT maintaining character consistency",
        'sketch': ", hand-drawn ink pen sketch appearance, organic ink pen strokes, loose artistic ink lines, pen and ink illustration style, BUT keeping identical character features", 
        'comic': ", inky dramatic comic book panel style, bold inky lines, high contrast ink work, dynamic dramatic panels, graphic novel ink illustration, BUT preserving consistent character appearance"
    }
    
    # Ensure ALL styles maintain enhanced consistency controls
    style_suffix = style_additions.get(style_key, "")
    consistency_reinforcement = ", CRITICAL: maintain identical character features, same facial proportions, consistent line art style throughout all frames"
    
    return base_dna + style_suffix + consistency_reinforcement

async def generate_ai_frame(client: AsyncOpenAI, scene: Dict[str, Any], frame_number: int, style_dna: str, character_database: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate a single frame using AI with prompt sanitization and character consistency
    """
    
    # Create frame prompt with character database for consistency
    raw_prompt = create_ai_frame_prompt(scene, frame_number, style_dna, character_database)
    
    # AI-based prompt sanitization (pure, side-effect-free)
    from utils.prompt_sanitizer import sanitize_prompt_for_storyboard
    sanitized_prompt, changes_made, is_sensitive = sanitize_prompt_for_storyboard(raw_prompt)
    
    # Log sanitization results
    if changes_made and len(changes_made) > 1:  # More than just "Added storyboard context only"
        print(f"🧹 Prompt sanitized: {len(changes_made)} changes made")
    
    # Generate image using configured image generation model
    image_model = get_model_for_task('image_generation')
    print(f"🎨 Generating image for frame {scene['scene_number']}.{frame_number} using {image_model}")
    print(f"   Prompt: {sanitized_prompt[:100]}...")
    
    image_response = await client.images.generate(
        model=image_model,
        prompt=sanitized_prompt,
        size="1024x1024",
        quality="medium",
        n=1
    )
    
    # gpt-image-1 returns base64 directly in the response
    # Check if it's base64 or URL
    if hasattr(image_response.data[0], 'b64_json') and image_response.data[0].b64_json:
        # Base64 format
        b64_image = image_response.data[0].b64_json
        image_url = f"data:image/png;base64,{b64_image}"
    else:
        # URL format (fallback)
        image_url = image_response.data[0].url
    
    # Create frame metadata with sanitization info
    frame = {
        'frame_id': f"frame_{scene['scene_number']}_{frame_number}",
        'scene_number': scene['scene_number'],
        'frame_number': frame_number,
        'prompt': raw_prompt,  # Original prompt
        'prompt_used': sanitized_prompt,  # Sanitized prompt actually used
        'prompt_sanitized': len(changes_made) > 1,  # Whether sanitization occurred
        'sanitization_changes': changes_made,  # What changes were made
        'is_sensitive_content': is_sensitive,  # Whether content was flagged
        'image_url': image_url,
        'status': 'completed',
        'generation_time': datetime.now().isoformat(),
        'cost': 0.020,  # gpt-image-1 cost
        'scene_description': scene.get('description', ''),
        'key_visual': scene.get('key_visual_moment', ''),
        'location': scene.get('location', 'Unknown'),
        'time_of_day': scene.get('time_of_day', 'DAY'),
        'characters': scene.get('characters', []),
        'camera_angles': scene.get('camera_angles', []),
        'mood': scene.get('mood', 'neutral'),
        'story_beat': scene.get('story_beat', 'Unknown'),
        'importance': scene.get('importance', 5)
    }
    
    print(f"✅ Generated frame {frame['frame_id']}")
    return frame

def create_ai_frame_prompt(scene: Dict[str, Any], frame_number: int, style_dna: str, character_database: Dict[str, Any] = None) -> str:
    """
    Create AI frame prompt with detailed character consistency
    """
    
    # Base components
    location = scene.get('location', 'Unknown Location')
    time_of_day = scene.get('time_of_day', 'DAY')
    key_visual = scene.get('key_visual_moment', '')
    characters = scene.get('characters', [])
    mood = scene.get('mood', 'neutral')
    
    # Frame-specific shot type
    shot_types = scene.get('camera_angles', ['medium shot', 'wide shot', 'close-up'])
    shot_type = shot_types[min(frame_number - 1, len(shot_types) - 1)]
    
    # Build prompt
    prompt = f"{style_dna}, {shot_type} of {location} during {time_of_day}"
    
    # Add detailed character descriptions for consistency
    if characters and character_database:
        character_details = []
        for char_name in characters[:2]:  # Max 2 characters for clarity
            char_info = character_database.get(char_name)
            if char_info and isinstance(char_info, dict):
                # Build detailed character description
                char_desc_parts = []
                
                # Age and build
                if char_info.get('age_group'):
                    char_desc_parts.append(char_info['age_group'])
                if char_info.get('build'):
                    char_desc_parts.append(char_info['build'])
                
                # Distinctive features
                if char_info.get('distinctive_features'):
                    char_desc_parts.append(char_info['distinctive_features'])
                
                # Clothing
                if char_info.get('clothing'):
                    char_desc_parts.append(f"wearing {char_info['clothing']}")
                
                # Props
                if char_info.get('props'):
                    char_desc_parts.append(f"with {char_info['props']}")
                
                if char_desc_parts:
                    detailed_desc = f"{char_name} ({', '.join(char_desc_parts)})"
                    character_details.append(detailed_desc)
                else:
                    character_details.append(char_name)
            else:
                # Fallback to simple name if no detailed info
                character_details.append(char_name)
        
        if character_details:
            prompt += f", featuring {', and '.join(character_details)}"
    elif characters:
        # Fallback to simple character list
        char_list = ', '.join(characters[:2])
        prompt += f", featuring {char_list}"
    
    # Add key visual
    if key_visual:
        prompt += f", {key_visual}"
    
    # Add mood
    if mood and mood != 'neutral':
        prompt += f", {mood} mood"
    
    # Add quality constraints for consistency
    prompt += ", professional storyboard quality, clear composition, consistent art style, uniform line weight"
    
    return prompt

def simulate_frame_generation(analysis: Dict[str, Any], style_prompt: str) -> List[Dict[str, Any]]:
    """
    Fallback frame generation with placeholders
    """
    frames = []
    
    print(f"🎬 Generating frames for {len(analysis['scenes'])} scenes...")
    
    for i, scene in enumerate(analysis['scenes']):
        # Generate 1 frame per scene for consistency
        frame = generate_placeholder_frame(scene, 1, style_prompt)
        frames.append(frame)
        
        print(f"   📝 Generated frame {i+1}/{len(analysis['scenes'])}: {frame['frame_id']}")
        
        # Simulate realistic generation time (shorter)
        time.sleep(0.5)
    
    print(f"✅ Frame generation complete: {len(frames)} frames")
    return frames

def generate_ai_frame_sync(scene: Dict[str, Any], frame_number: int, style_prompt: str, analysis: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Synchronous wrapper for AI frame generation with character consistency
    """
    try:
        # Get OpenAI client
        client = get_openai_client()
        
        # Get style DNA
        style_dna = get_style_dna(style_prompt)
        
        # Get character database for consistency
        character_database = analysis.get('characters', {}) if analysis else {}
        
        # Run async generation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        frame = loop.run_until_complete(
            generate_ai_frame(client, scene, frame_number, style_dna, character_database)
        )
        
        loop.close()
        return frame
        
    except Exception as e:
        print(f"❌ AI generation failed for scene {scene['scene_number']}: {e}")
        print("   Falling back to placeholder...")
        # Fallback to placeholder
        return generate_placeholder_frame(scene, frame_number, style_prompt)

def generate_placeholder_frame(scene: Dict[str, Any], frame_number: int, style_prompt: str) -> Dict[str, Any]:
    """
    Generate placeholder frame when AI fails
    """
    
    # Create frame prompt
    prompt = create_frame_prompt(scene, frame_number, style_prompt)
    
    # Generate placeholder image
    image_url = generate_placeholder_image(scene, frame_number)
    
    frame = {
        'frame_id': f"frame_{scene['scene_number']}_{frame_number}",
        'scene_number': scene['scene_number'],
        'frame_number': frame_number,
        'prompt': prompt,
        'prompt_used': prompt,
        'image_url': image_url,
        'status': 'completed',
        'generation_time': datetime.now().isoformat(),
        'cost': 0.04,  # Simulated cost
        'scene_description': scene.get('description', ''),
        'key_visual': scene.get('key_visual_moment', ''),
        'location': scene.get('location', 'Unknown'),
        'time_of_day': scene.get('time_of_day', 'DAY'),
        'characters': scene.get('characters', [])
    }
    
    return frame

def generate_frame(scene: Dict[str, Any], frame_number: int, style_prompt: str) -> Dict[str, Any]:
    """Generate a single frame"""
    
    # Simulate frame generation
    frame_id = f"frame_{scene['scene_number']}_{frame_number}"
    
    # Create descriptive prompt
    prompt = create_frame_prompt(scene, frame_number, style_prompt)
    
    # Simulate image generation (use placeholder)
    image_url = generate_placeholder_image(scene, frame_number)
    
    frame = {
        'frame_id': frame_id,
        'scene_number': scene['scene_number'],
        'frame_number': frame_number,
        'prompt': prompt,
        'image_url': image_url,
        'status': 'completed',
        'generation_time': datetime.now().isoformat(),
        'cost': 0.04,  # Simulated cost
        'scene_description': scene['description'],
        'key_visual': scene['key_visual_moment'],
        'location': scene['location'],
        'time_of_day': scene['time_of_day'],
        'characters': scene['characters']
    }
    
    return frame

def create_frame_prompt(scene: Dict[str, Any], frame_number: int, style_prompt: str) -> str:
    """Create descriptive prompt for frame"""
    
    # Base prompt components
    location = scene['location']
    time_of_day = scene['time_of_day']
    key_visual = scene['key_visual_moment']
    
    # Frame-specific elements
    if frame_number == 1:
        shot_type = "establishing shot"
        focus = f"showing {location}"
    else:
        shot_type = random.choice(["medium shot", "close-up", "wide shot"])
        focus = f"focusing on {key_visual}"
    
    # Combine into prompt
    prompt = f"{style_prompt}, {shot_type} of {location} during {time_of_day}, {focus}"
    
    # Add character information if available
    if scene['characters']:
        characters = ', '.join(scene['characters'][:2])  # Max 2 characters
        prompt += f", featuring {characters}"
    
    # Add scene context
    if key_visual:
        prompt += f", {key_visual}"
    
    return prompt

def generate_placeholder_image(scene: Dict[str, Any], frame_number: int) -> str:
    """Generate placeholder image URL"""
    
    # Use a placeholder service with scene-specific parameters
    width = 800
    height = 600
    
    # Create scene-based placeholder
    location = scene['location'].replace(' ', '+')
    time_of_day = scene['time_of_day'].lower()
    
    # Different placeholder styles based on scene
    slug_line = scene.get('slug_line', f"EXT. {scene['location']} - {time_of_day}")
    if 'interior' in scene['location'].lower() or 'int.' in slug_line.lower():
        bg_color = '333333'
        text_color = 'ffffff'
    else:
        bg_color = '87CEEB' if time_of_day == 'day' else '2F4F4F'
        text_color = '000000' if time_of_day == 'day' else 'ffffff'
    
    # Create descriptive text for placeholder
    placeholder_text = f"Scene {scene['scene_number']}.{frame_number}\\n{location}\\n{time_of_day}"
    
    # Use placeholder.com or similar service
    placeholder_url = f"https://via.placeholder.com/{width}x{height}/{bg_color}/{text_color}?text={placeholder_text}"
    
    return placeholder_url

def simulate_generation_progress(total_frames: int, callback=None):
    """Simulate generation progress for UI updates"""
    
    for i in range(total_frames):
        # Simulate work
        time.sleep(random.uniform(1.0, 2.0))
        
        progress = (i + 1) / total_frames * 100
        
        if callback:
            callback(progress, f"Generating frame {i + 1} of {total_frames}")
    
    if callback:
        callback(100, "Generation complete!")

def get_frame_metadata(frame: Dict[str, Any]) -> Dict[str, Any]:
    """Get metadata for a frame"""
    return {
        'frame_id': frame['frame_id'],
        'scene_number': frame['scene_number'],
        'frame_number': frame['frame_number'],
        'status': frame['status'],
        'generation_time': frame['generation_time'],
        'cost': frame['cost'],
        'has_image': bool(frame.get('image_url')),
        'prompt_length': len(frame.get('prompt', '')),
        'characters_count': len(frame.get('characters', [])),
        'location': frame.get('location'),
        'time_of_day': frame.get('time_of_day')
    }

def calculate_total_cost(frames: List[Dict[str, Any]]) -> float:
    """Calculate total cost for all frames"""
    return sum(frame.get('cost', 0) for frame in frames)

def get_generation_stats(frames: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get generation statistics"""
    total_frames = len(frames)
    completed_frames = len([f for f in frames if f['status'] == 'completed'])
    total_cost = calculate_total_cost(frames)
    
    # Scene distribution
    scene_counts = {}
    for frame in frames:
        scene_num = frame['scene_number']
        scene_counts[scene_num] = scene_counts.get(scene_num, 0) + 1
    
    return {
        'total_frames': total_frames,
        'completed_frames': completed_frames,
        'success_rate': (completed_frames / total_frames * 100) if total_frames > 0 else 0,
        'total_cost': total_cost,
        'avg_cost_per_frame': total_cost / total_frames if total_frames > 0 else 0,
        'scenes_covered': len(scene_counts),
        'frames_per_scene': scene_counts,
        'generation_time': frames[-1]['generation_time'] if frames else None
    }