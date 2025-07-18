#!/usr/bin/env python3
"""
Test script to verify AI-powered scene analysis is working
"""

import os
import sys
import asyncio
from utils.scene_analyzer import analyze_screenplay, detect_optimal_scene_count
from utils.storyboard_generator import generate_storyboard_frames

# Sample screenplay text
SAMPLE_SCREENPLAY = """
FADE IN:

EXT. CITY STREET - DAY

A bustling city street filled with people. JOHN SMITH (30s), a detective in a worn coat, walks quickly through the crowd.

JOHN
(into phone)
I need backup at Fifth and Main. Now.

John reaches into his jacket and pulls out a gun. He looks around nervously.

INT. WAREHOUSE - NIGHT

A dark, empty warehouse. SARAH JOHNSON (20s), a hacker with bright green hair, sits at a computer terminal.

SARAH
(typing furiously)
Come on, come on... Got it!

She turns to face the camera, a smile spreading across her face.

EXT. ROOFTOP - SUNSET

John and Sarah meet on a rooftop overlooking the city. The sun sets behind them.

JOHN
Did you get the files?

SARAH
Everything we need. But we're not alone.

They hear footsteps approaching.

FADE OUT.
"""

def test_scene_detection():
    """Test automatic scene detection"""
    print("🎯 Testing automatic scene detection...")
    
    scene_count = detect_optimal_scene_count(SAMPLE_SCREENPLAY)
    print(f"   Detected optimal scene count: {scene_count}")
    
    return scene_count

def test_scene_analysis():
    """Test AI-powered scene analysis"""
    print("🤖 Testing AI-powered scene analysis...")
    
    try:
        # Set a test API key if not already set
        if not os.getenv('OPENAI_API_KEY'):
            os.environ['OPENAI_API_KEY'] = 'sk-test-key-placeholder'
        
        # Test with automatic scene detection
        analysis = analyze_screenplay(SAMPLE_SCREENPLAY)
        
        print(f"   Title: {analysis['title']}")
        print(f"   Total scenes: {analysis['total_scenes']}")
        print(f"   Characters: {list(analysis['characters'].keys())}")
        print(f"   Analysis type: {analysis['analysis_type']}")
        
        # Print scene details
        for i, scene in enumerate(analysis['scenes'][:3]):  # Show first 3 scenes
            print(f"   Scene {i+1}: {scene['location']} - {scene['time_of_day']}")
            print(f"      Characters: {scene.get('characters', [])}")
            print(f"      Key visual: {scene.get('key_visual_moment', 'N/A')[:50]}...")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ AI analysis failed: {e}")
        print("   📝 Note: This is expected without a real OpenAI API key")
        return None

def test_frame_generation(analysis):
    """Test AI-powered frame generation"""
    print("🎨 Testing AI-powered frame generation...")
    
    if not analysis:
        print("   ⚠️  Skipping frame generation - no analysis available")
        return
    
    try:
        # Test with classic style
        frames = generate_storyboard_frames(analysis, 'classic')
        
        print(f"   Generated {len(frames)} frames")
        
        # Show first frame details
        if frames:
            frame = frames[0]
            print(f"   First frame: {frame['frame_id']}")
            print(f"   Scene: {frame['scene_number']}")
            print(f"   Status: {frame['status']}")
            print(f"   Prompt: {frame['prompt'][:100]}...")
            print(f"   Image URL: {frame['image_url'][:50]}...")
        
        return frames
        
    except Exception as e:
        print(f"   ❌ Frame generation failed: {e}")
        print("   📝 Note: This is expected without a real OpenAI API key")
        return None

def main():
    """Main test function"""
    print("🧪 Testing SF Simple AI Integration")
    print("=" * 50)
    
    # Test 1: Scene detection
    scene_count = test_scene_detection()
    print()
    
    # Test 2: Scene analysis
    analysis = test_scene_analysis()
    print()
    
    # Test 3: Frame generation
    frames = test_frame_generation(analysis)
    print()
    
    # Summary
    print("📊 Test Summary:")
    print("=" * 50)
    print(f"✅ Scene detection: {scene_count} scenes detected")
    print(f"{'✅' if analysis else '❌'} Scene analysis: {'Working' if analysis else 'Failed (expected without API key)'}")
    print(f"{'✅' if frames else '❌'} Frame generation: {'Working' if frames else 'Failed (expected without API key)'}")
    
    if analysis and analysis['analysis_type'] == 'AI-powered':
        print("🎉 AI integration is working correctly!")
    else:
        print("🔄 Using fallback analysis (normal without API key)")

if __name__ == "__main__":
    main()