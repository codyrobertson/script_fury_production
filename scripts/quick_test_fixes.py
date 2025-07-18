#!/usr/bin/env python3
"""
Quick Test for Performance Fixes
Proves the 4 main fixes work:
1. Faster AI analysis 
2. No event loop conflicts
3. Better frame counts
4. Style consistency
"""

import os
import sys
import time
import asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_analyzer import detect_optimal_scene_count, fast_ai_analyze_screenplay
from utils.prompt_sanitizer import sanitize_prompt_for_storyboard
from utils.storyboard_generator import get_style_dna

# Short test screenplay
TEST_SCRIPT = """
EXT. CANYON - DAY
Aaron hikes through the canyon.

INT. CANYON CREVICE - CONTINUOUS  
A boulder traps Aaron's arm.

AARON
Help! Someone help me!

EXT. CANYON CREVICE - LATER
Aaron realizes he's out of water.

AARON
That's it. No more water.

He makes the decision to cut his arm.
"""

def test_fix_1_speed():
    """Test 1: AI Analysis Speed - Should be much faster"""
    print("🧪 Test 1: AI Analysis Speed")
    
    start = time.time()
    scenes = detect_optimal_scene_count(TEST_SCRIPT)
    analysis = fast_ai_analyze_screenplay(TEST_SCRIPT, scenes)
    duration = time.time() - start
    
    # Should complete in under 15 seconds (was taking 30+)
    speed_ok = duration < 15
    has_data = len(analysis.get('characters', {})) > 0 and len(analysis.get('scenes', [])) > 0
    
    print(f"   Duration: {duration:.2f}s (target: <15s)")
    print(f"   Characters: {len(analysis.get('characters', {}))}")
    print(f"   Scenes: {len(analysis.get('scenes', []))}")
    print(f"   ✅ PASS" if speed_ok and has_data else f"   ❌ FAIL")
    
    return speed_ok and has_data, analysis

def test_fix_2_event_loops():
    """Test 2: Event Loop Conflicts - Should not crash"""
    print("\n🧪 Test 2: Event Loop Conflicts")
    
    test_prompts = [
        "Professional storyboard, Aaron in canyon",
        "Black and white line art, boulder falls",
        "Storyboard style, Aaron cuts arm"
    ]
    
    successes = 0
    for i, prompt in enumerate(test_prompts):
        try:
            sanitized, changes, sensitive = sanitize_prompt_for_storyboard(prompt)
            if sanitized:
                successes += 1
                print(f"   Prompt {i+1}: ✅ OK")
            else:
                print(f"   Prompt {i+1}: ❌ Failed")
        except Exception as e:
            print(f"   Prompt {i+1}: ❌ Error: {e}")
    
    all_ok = successes == len(test_prompts)
    print(f"   Result: {successes}/{len(test_prompts)} successful")
    print(f"   ✅ PASS" if all_ok else f"   ❌ FAIL")
    
    return all_ok

def test_fix_3_frame_counts(analysis):
    """Test 3: Frame Count Logic - Should avoid repetitive frames"""
    print("\n🧪 Test 3: Frame Count Logic")
    
    scenes = analysis.get('scenes', [])
    total_frames = sum(scene.get('frames_needed', 1) for scene in scenes)
    avg_frames = total_frames / len(scenes) if scenes else 0
    
    # Check for repetitive scenes (like "realizes he's out of water")
    repetitive_scenes = []
    for scene in scenes:
        desc = scene.get('description', '').lower()
        if any(word in desc for word in ['realizes', 'discovers', 'checks']):
            frames = scene.get('frames_needed', 1)
            repetitive_scenes.append((desc[:50], frames))
    
    # Should average 1.5 frames or less per scene
    avg_ok = avg_frames <= 1.5
    
    print(f"   Total frames: {total_frames}")
    print(f"   Average frames/scene: {avg_frames:.2f} (target: ≤1.5)")
    print(f"   Repetitive scenes: {len(repetitive_scenes)}")
    
    for desc, frames in repetitive_scenes:
        print(f"     '{desc}...': {frames} frames")
    
    print(f"   ✅ PASS" if avg_ok else f"   ❌ FAIL")
    
    return avg_ok

def test_fix_4_style_consistency():
    """Test 4: Style Consistency - Should have consistency keywords"""
    print("\n🧪 Test 4: Style Consistency")
    
    styles = ['classic', 'cinematic']
    consistency_found = 0
    
    for style in styles:
        style_dna = get_style_dna(f"{style} storyboard")
        has_consistency = any(word in style_dna.lower() for word in 
                            ['consistent', 'uniform', 'same', 'throughout'])
        
        if has_consistency:
            consistency_found += 1
            print(f"   {style}: ✅ Has consistency keywords")
        else:
            print(f"   {style}: ❌ Missing consistency keywords")
    
    all_consistent = consistency_found == len(styles)
    print(f"   Result: {consistency_found}/{len(styles)} styles have consistency")
    print(f"   ✅ PASS" if all_consistent else f"   ❌ FAIL")
    
    return all_consistent

def main():
    """Run quick tests to prove fixes work"""
    print("🚀 Quick Performance Fix Tests")
    print("=" * 50)
    
    start_time = time.time()
    
    # Test 1: Speed
    speed_ok, analysis = test_fix_1_speed()
    
    # Test 2: Event loops
    loops_ok = test_fix_2_event_loops()
    
    # Test 3: Frame counts
    frames_ok = test_fix_3_frame_counts(analysis)
    
    # Test 4: Style consistency
    style_ok = test_fix_4_style_consistency()
    
    # Summary
    total_time = time.time() - start_time
    passed = sum([speed_ok, loops_ok, frames_ok, style_ok])
    
    print("\n" + "=" * 50)
    print(f"🏁 Tests Complete ({total_time:.2f}s)")
    print(f"✅ Passed: {passed}/4")
    print(f"❌ Failed: {4-passed}/4")
    
    if passed == 4:
        print("🎉 ALL FIXES WORKING! Ready for production.")
    else:
        print("⚠️  Some fixes need attention.")
    
    return passed == 4

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)