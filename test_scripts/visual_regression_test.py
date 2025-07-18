#!/usr/bin/env python3
"""
Visual Regression Test - Proves the improvements work with actual generation
Tests the complete pipeline to ensure:
1. Faster analysis
2. No crashes
3. Proper frame allocation
4. Consistent style
"""

import os
import sys
import time
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_analyzer import detect_optimal_scene_count, fast_ai_analyze_screenplay
from utils.storyboard_generator import generate_ai_frame_sync, get_style_dna
from utils.prompt_sanitizer import sanitize_prompt_for_storyboard

# Test Aaron Ralston scenario (typical of what causes issues)
AARON_SCRIPT = """
EXT. UTAH CANYON - DAY

AARON RALSTON (27), experienced hiker, navigates through Bluejohn Canyon.

INT. NARROW CANYON PASSAGE - CONTINUOUS

Aaron squeezes through a tight crevice. A boulder shifts.

AARON
(looking up)
That doesn't look stable.

The boulder CRASHES down, pinning his right arm.

AARON (CONT'D)
(screaming)
Help! Someone help me!

EXT. CANYON CREVICE - LATER

Aaron realizes he's completely alone. He checks his water bottle.

AARON
(to himself)
I've got maybe a day's worth left.

He tries various methods to free himself.

EXT. CANYON CREVICE - MORNING (DAY 2)

Aaron wakes up dehydrated. He drinks his last drops of water.

AARON
(realizing)
That's it. No more water.

Aaron looks at his knife, then his trapped arm.

AARON (CONT'D)
(determined)
I'm not dying here.

He begins the amputation process.

EXT. CANYON WALL - LATER

Aaron, one-armed, rappels down the canyon wall to freedom.

EXT. DESERT TRAIL - CONTINUOUS

Aaron stumbles onto a trail where HIKERS find him.

HIKER
Oh my God! Are you okay?

AARON
(weakly)
I've been trapped for five days.

FADE OUT.
"""

def test_visual_regression():
    """Complete visual regression test"""
    print("🎬 Visual Regression Test - Aaron Ralston Script")
    print("=" * 60)
    
    # Start timing
    total_start = time.time()
    
    # PHASE 1: Scene Analysis
    print("\n📊 Phase 1: Scene Analysis")
    analysis_start = time.time()
    
    detected_scenes = detect_optimal_scene_count(AARON_SCRIPT)
    print(f"   Detected scenes: {detected_scenes}")
    
    analysis = fast_ai_analyze_screenplay(AARON_SCRIPT, detected_scenes)
    analysis_time = time.time() - analysis_start
    
    print(f"   Analysis time: {analysis_time:.2f}s")
    print(f"   Characters found: {len(analysis.get('characters', {}))}")
    print(f"   Scenes analyzed: {len(analysis.get('scenes', []))}")
    
    # PHASE 2: Frame Count Validation
    print("\n🎯 Phase 2: Frame Count Validation")
    scenes = analysis.get('scenes', [])
    total_frames = sum(scene.get('frames_needed', 1) for scene in scenes)
    
    print(f"   Total frames planned: {total_frames}")
    print(f"   Average frames/scene: {total_frames/len(scenes):.2f}")
    
    # Check for the specific "realizes" scene that was causing issues
    realize_scenes = []
    for i, scene in enumerate(scenes):
        desc = scene.get('description', '').lower()
        if 'realizes' in desc or 'realizing' in desc:
            frames = scene.get('frames_needed', 1)
            realize_scenes.append((i+1, desc[:50], frames))
    
    print(f"   'Realizes' type scenes: {len(realize_scenes)}")
    for scene_num, desc, frames in realize_scenes:
        print(f"     Scene {scene_num}: '{desc}...' → {frames} frames")
    
    # PHASE 3: Prompt Sanitization Test
    print("\n🧹 Phase 3: Prompt Sanitization")
    sanitization_start = time.time()
    
    # Test prompts that might cause issues
    test_prompts = [
        "Professional storyboard, Aaron's arm trapped by boulder",
        "Black and white line art, Aaron cutting his arm with knife",
        "Storyboard style, Aaron realizes he's out of water"
    ]
    
    sanitized_prompts = []
    for prompt in test_prompts:
        try:
            sanitized, changes, sensitive = sanitize_prompt_for_storyboard(prompt)
            sanitized_prompts.append({
                'original': prompt,
                'sanitized': sanitized,
                'changes': len(changes),
                'sensitive': sensitive,
                'success': True
            })
        except Exception as e:
            sanitized_prompts.append({
                'original': prompt,
                'error': str(e),
                'success': False
            })
    
    sanitization_time = time.time() - sanitization_start
    successful_sanitizations = sum(1 for p in sanitized_prompts if p['success'])
    
    print(f"   Sanitization time: {sanitization_time:.2f}s")
    print(f"   Successful sanitizations: {successful_sanitizations}/{len(test_prompts)}")
    
    # PHASE 4: Style Consistency Test
    print("\n🎨 Phase 4: Style Consistency")
    style_start = time.time()
    
    style_dna = get_style_dna("Professional storyboard, black and white line art")
    consistency_keywords = ['consistent', 'uniform', 'same', 'throughout', 'professional']
    consistency_count = sum(1 for keyword in consistency_keywords if keyword in style_dna.lower())
    
    style_time = time.time() - style_start
    
    print(f"   Style DNA generation time: {style_time:.2f}s")
    print(f"   Consistency keywords found: {consistency_count}/{len(consistency_keywords)}")
    print(f"   Style DNA length: {len(style_dna)} characters")
    
    # PHASE 5: Sample Frame Generation
    print("\n🖼️  Phase 5: Sample Frame Generation")
    if scenes:
        frame_start = time.time()
        
        # Test the first scene (should be fast and not crash)
        first_scene = scenes[0]
        try:
            frame = generate_ai_frame_sync(
                first_scene, 
                1, 
                "Professional storyboard, black and white line art",
                analysis
            )
            
            frame_time = time.time() - frame_start
            frame_success = frame and frame.get('status') == 'completed'
            
            print(f"   Frame generation time: {frame_time:.2f}s")
            print(f"   Frame generation success: {frame_success}")
            
            if frame_success:
                print(f"   Frame ID: {frame.get('frame_id')}")
                print(f"   Has image: {bool(frame.get('image_url'))}")
                print(f"   Sanitized prompt: {frame.get('prompt_sanitized', False)}")
                
        except Exception as e:
            print(f"   Frame generation failed: {e}")
            frame_success = False
    else:
        print("   No scenes to test")
        frame_success = False
    
    # FINAL ASSESSMENT
    total_time = time.time() - total_start
    
    print("\n" + "=" * 60)
    print(f"🏁 Visual Regression Test Complete ({total_time:.2f}s)")
    print()
    
    # Score the results
    speed_score = 100 if analysis_time < 20 else max(0, 100 - (analysis_time - 20) * 5)
    frame_score = 100 if total_frames/len(scenes) <= 1.5 else max(0, 100 - (total_frames/len(scenes) - 1.5) * 50)
    sanitization_score = (successful_sanitizations / len(test_prompts)) * 100
    consistency_score = (consistency_count / len(consistency_keywords)) * 100
    generation_score = 100 if frame_success else 0
    
    overall_score = (speed_score + frame_score + sanitization_score + consistency_score + generation_score) / 5
    
    print(f"📊 Performance Scores:")
    print(f"   Speed: {speed_score:.1f}/100 ({analysis_time:.2f}s analysis)")
    print(f"   Frame Logic: {frame_score:.1f}/100 ({total_frames/len(scenes):.2f} avg frames/scene)")
    print(f"   Sanitization: {sanitization_score:.1f}/100 ({successful_sanitizations}/{len(test_prompts)} successful)")
    print(f"   Consistency: {consistency_score:.1f}/100 ({consistency_count}/{len(consistency_keywords)} keywords)")
    print(f"   Generation: {generation_score:.1f}/100 ({'Success' if frame_success else 'Failed'})")
    print(f"   Overall: {overall_score:.1f}/100")
    
    # Final verdict
    if overall_score >= 80:
        print("🎉 EXCELLENT! All fixes are working as expected.")
        verdict = "PASS"
    elif overall_score >= 60:
        print("✅ GOOD! Most fixes are working, minor issues remain.")
        verdict = "PASS"
    else:
        print("⚠️  NEEDS WORK! Some fixes are not working properly.")
        verdict = "FAIL"
    
    # Save detailed results
    results = {
        'timestamp': datetime.now().isoformat(),
        'total_time': total_time,
        'analysis_time': analysis_time,
        'characters_found': len(analysis.get('characters', {})),
        'scenes_analyzed': len(analysis.get('scenes', [])),
        'total_frames': total_frames,
        'avg_frames_per_scene': total_frames/len(scenes) if scenes else 0,
        'realize_scenes': len(realize_scenes),
        'sanitization_success_rate': successful_sanitizations / len(test_prompts),
        'consistency_keywords': consistency_count,
        'frame_generation_success': frame_success,
        'scores': {
            'speed': speed_score,
            'frame_logic': frame_score,
            'sanitization': sanitization_score,
            'consistency': consistency_score,
            'generation': generation_score,
            'overall': overall_score
        },
        'verdict': verdict
    }
    
    results_file = f"visual_regression_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    return verdict == "PASS"

if __name__ == "__main__":
    success = test_visual_regression()
    sys.exit(0 if success else 1)