#!/usr/bin/env python3
"""
Quick Model Performance Test for Script Fury Simple
Tests FAST vs SMART model configurations for optimal performance
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_analyzer import fast_ai_analyze_screenplay, detect_optimal_scene_count

# Quick test script
TEST_SCRIPT = """
FADE IN:

EXT. CITY STREET - DAY

JACK REACHER, a tough ex-military investigator, walks down the busy street.

JACK
(determined)
I need to find the truth.

A BLACK SUV screeches to a halt. THREE ARMED MEN jump out.

GUNMAN #1
(shouting)
There he is! Get him!

Jack dives behind a parked car as bullets fly. He pulls out his pistol.

JACK
(to himself)
Not today.

He fires back, taking down two gunmen. The third escapes.

JACK
(breathing heavily)
This is just the beginning.

INT. POLICE STATION - LATER

DETECTIVE SARAH MARTINEZ reviews the case files.

SARAH
(to Jack)
You're in deep trouble.

JACK
I'm just getting started.

FADE OUT.
"""

# Model configurations to test
MODEL_CONFIGS = [
    {
        "name": "FAST",
        "CHARACTER_MODEL": "o3-mini",
        "SCENE_MODEL": "o3-mini",
        "INFO_MODEL": "o3-mini",
        "SANITIZATION_MODEL": "o3-mini"
    },
    {
        "name": "BALANCED",
        "CHARACTER_MODEL": "gpt-4o",
        "SCENE_MODEL": "gpt-4o",
        "INFO_MODEL": "gpt-4o-mini",
        "SANITIZATION_MODEL": "o3-mini"
    },
    {
        "name": "SMART",
        "CHARACTER_MODEL": "gpt-4o",
        "SCENE_MODEL": "gpt-4o",
        "INFO_MODEL": "gpt-4o",
        "SANITIZATION_MODEL": "gpt-4o"
    }
]

def test_model_config(config):
    """Test a specific model configuration"""
    print(f"\n🧪 Testing {config['name']} configuration...")
    
    # Set environment variables
    original_env = {}
    for key, value in config.items():
        if key != 'name':
            original_env[key] = os.getenv(key)
            os.environ[key] = value
    
    try:
        # Time the analysis
        start_time = time.time()
        
        # Detect optimal scene count
        detected_scenes = detect_optimal_scene_count(TEST_SCRIPT)
        
        # Run analysis
        analysis = fast_ai_analyze_screenplay(TEST_SCRIPT, detected_scenes)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Extract metrics
        characters = analysis.get('characters', {})
        scenes = analysis.get('scenes', [])
        total_scenes = analysis.get('total_scenes', 0)
        total_frames = analysis.get('total_frames', 0)
        
        # Calculate frame accuracy
        actual_frames = sum(scene.get('frames_needed', 1) for scene in scenes)
        
        # Results
        result = {
            'config': config['name'],
            'duration': duration,
            'detected_scenes': detected_scenes,
            'total_scenes': total_scenes,
            'total_frames': total_frames,
            'actual_frames': actual_frames,
            'character_count': len(characters),
            'characters': list(characters.keys()),
            'frame_accuracy': total_frames == actual_frames,
            'success': True
        }
        
        print(f"   ✅ Duration: {duration:.2f}s")
        print(f"   📊 Detected scenes: {detected_scenes}")
        print(f"   🎬 Total scenes: {total_scenes}")
        print(f"   🖼️  Total frames: {total_frames} (actual: {actual_frames})")
        print(f"   👥 Characters: {len(characters)} - {list(characters.keys())}")
        print(f"   🎯 Frame accuracy: {'✅' if result['frame_accuracy'] else '❌'}")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {
            'config': config['name'],
            'duration': 999,
            'success': False,
            'error': str(e)
        }
        
    finally:
        # Restore original environment
        for key, value in original_env.items():
            if value:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]

def main():
    """Run quick model comparison"""
    print("🚀 QUICK MODEL PERFORMANCE TEST")
    print("=" * 60)
    
    results = []
    
    for config in MODEL_CONFIGS:
        result = test_model_config(config)
        results.append(result)
        
    # Summary
    print("\n📊 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    successful_results = [r for r in results if r.get('success', False)]
    
    if successful_results:
        # Sort by duration (fastest first)
        successful_results.sort(key=lambda x: x['duration'])
        
        print("\n🏆 SPEED RANKING:")
        for i, result in enumerate(successful_results, 1):
            print(f"{i}. {result['config']}: {result['duration']:.2f}s")
            
        # Quality comparison
        print("\n📈 QUALITY COMPARISON:")
        for result in successful_results:
            print(f"{result['config']}:")
            print(f"   Characters: {result['character_count']}")
            print(f"   Scenes: {result['total_scenes']}")
            print(f"   Frames: {result['total_frames']}")
            print(f"   Frame Accuracy: {'✅' if result['frame_accuracy'] else '❌'}")
            print()
            
        # Recommendation
        fastest = successful_results[0]
        most_characters = max(successful_results, key=lambda x: x['character_count'])
        
        print("💡 RECOMMENDATIONS:")
        print(f"⚡ Fastest: {fastest['config']} ({fastest['duration']:.2f}s)")
        print(f"🎯 Best Character Detection: {most_characters['config']} ({most_characters['character_count']} characters)")
        
        # Overall recommendation
        if fastest['character_count'] >= most_characters['character_count'] * 0.8:
            print(f"🥇 RECOMMENDED: {fastest['config']} (good balance of speed and quality)")
        else:
            print(f"🥇 RECOMMENDED: {most_characters['config']} (better quality worth the extra time)")
            
    else:
        print("❌ All configurations failed!")

if __name__ == "__main__":
    main()