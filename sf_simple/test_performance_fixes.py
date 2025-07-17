#!/usr/bin/env python3
"""
Performance and Quality Test Suite for Script Fury Simple
Tests the fixes for:
1. AI analysis speed optimization
2. Event loop conflict resolution  
3. Frame count logic improvements
4. Style consistency enhancements
"""

import os
import sys
import time
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_analyzer import fast_ai_analyze_screenplay, detect_optimal_scene_count
from utils.storyboard_generator import generate_ai_frame_sync, get_style_dna
from utils.prompt_sanitizer import sanitize_prompt_for_storyboard

# Test screenplay content
TEST_SCREENPLAY = """
FADE IN:

EXT. DESERT CANYON - DAY

AARON RALSTON (27), athletic and confident, hikes alone through the narrow canyon. His backpack is loaded with climbing gear.

AARON
(to himself)
Just another day in paradise.

He navigates between towering rock walls, his movements fluid and experienced.

INT. CANYON CREVICE - CONTINUOUS

Aaron squeezes through a tight passage. A loose boulder shifts above him.

AARON
(looking up)
That doesn't look stable.

The boulder CRASHES down, trapping his right arm against the canyon wall.

AARON (CONT'D)
(screaming)
Help! Someone help me!

His voice echoes uselessly through the empty canyon.

EXT. CANYON ENTRANCE - LATER

Aaron realizes no one knows where he is. He checks his water supply - nearly empty.

AARON
(to himself)
I have maybe a day's worth of water left.

He begins to assess his situation, trying different methods to free himself.

EXT. CANYON CREVICE - NIGHT

Aaron shivers in the cold. He uses his knife to try to chip away at the boulder.

AARON
(determined)
I'm not dying here.

EXT. CANYON CREVICE - MORNING (DAY 2)

Aaron wakes up, dehydrated and exhausted. He drinks the last of his water.

AARON
(realizing)
That's it. No more water.

He looks at his trapped arm, then at his knife, a terrible realization dawning.

EXT. CANYON CREVICE - AFTERNOON

Aaron makes the ultimate decision. He begins to cut his arm to free himself.

AARON
(to himself)
I'm sorry, arm. But I choose life.

After the amputation, he rappels down the canyon wall with his remaining arm.

EXT. DESERT TRAIL - LATER

Aaron stumbles onto a trail where HIKERS find him.

HIKER
Oh my God! What happened to you?

AARON
(weakly)
I've been trapped for five days.

FADE OUT.
"""

class PerformanceTestSuite:
    """Test suite for performance and quality improvements"""
    
    def __init__(self):
        self.results = {
            'speed_tests': {},
            'quality_tests': {},
            'consistency_tests': {},
            'error_tests': {}
        }
        
    def log_test(self, test_name: str, result: Any, duration: float = None):
        """Log test result with timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'result': result,
            'duration_seconds': duration
        }
        
        category = 'speed_tests' if 'speed' in test_name.lower() else \
                  'quality_tests' if 'quality' in test_name.lower() else \
                  'consistency_tests' if 'consistency' in test_name.lower() else \
                  'error_tests'
        
        self.results[category][test_name] = log_entry
        
        status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
        duration_str = f" ({duration:.2f}s)" if duration else ""
        print(f"{status} {test_name}{duration_str}")
        
        if not result.get('success', False):
            print(f"   Error: {result.get('error', 'Unknown error')}")
        elif result.get('details'):
            print(f"   Details: {result.get('details')}")
    
    def test_ai_analysis_speed(self) -> bool:
        """Test 1: AI analysis speed optimization"""
        print("\n🔬 Testing AI Analysis Speed Optimization...")
        
        try:
            start_time = time.time()
            
            # Test scene detection speed
            detected_scenes = detect_optimal_scene_count(TEST_SCREENPLAY)
            scene_detection_time = time.time() - start_time
            
            # Test character extraction speed
            start_time = time.time()
            analysis = fast_ai_analyze_screenplay(TEST_SCREENPLAY, detected_scenes)
            analysis_time = time.time() - start_time
            
            total_time = scene_detection_time + analysis_time
            
            # Speed benchmarks (should be much faster now)
            speed_ok = total_time < 30  # Should complete in under 30 seconds
            has_characters = len(analysis.get('characters', {})) > 0
            has_scenes = len(analysis.get('scenes', [])) > 0
            
            result = {
                'success': speed_ok and has_characters and has_scenes,
                'details': f"Total: {total_time:.2f}s, Characters: {len(analysis.get('characters', {}))}, Scenes: {len(analysis.get('scenes', []))}"
            }
            
            self.log_test("AI_Analysis_Speed", result, total_time)
            return result['success']
            
        except Exception as e:
            result = {'success': False, 'error': str(e)}
            self.log_test("AI_Analysis_Speed", result)
            return False
    
    def test_event_loop_conflicts(self) -> bool:
        """Test 2: Event loop conflict resolution"""
        print("\n🔬 Testing Event Loop Conflict Resolution...")
        
        try:
            # Test multiple sanitization calls in sequence (this used to cause conflicts)
            test_prompts = [
                "Professional storyboard, Aaron trapped in canyon",
                "Black and white line art, Aaron cutting his arm",
                "Storyboard style, Aaron being rescued by hikers"
            ]
            
            start_time = time.time()
            sanitization_results = []
            
            for i, prompt in enumerate(test_prompts):
                try:
                    sanitized, changes, is_sensitive = sanitize_prompt_for_storyboard(prompt)
                    sanitization_results.append({
                        'prompt': prompt,
                        'sanitized': sanitized,
                        'changes': changes,
                        'success': True
                    })
                except Exception as e:
                    sanitization_results.append({
                        'prompt': prompt,
                        'error': str(e),
                        'success': False
                    })
            
            duration = time.time() - start_time
            
            # Check if all sanitizations succeeded
            all_successful = all(r['success'] for r in sanitization_results)
            no_event_loop_errors = not any('event loop' in str(r.get('error', '')) for r in sanitization_results)
            
            result = {
                'success': all_successful and no_event_loop_errors,
                'details': f"Sanitized {len(sanitization_results)} prompts, {sum(1 for r in sanitization_results if r['success'])} successful"
            }
            
            self.log_test("Event_Loop_Conflicts", result, duration)
            return result['success']
            
        except Exception as e:
            result = {'success': False, 'error': str(e)}
            self.log_test("Event_Loop_Conflicts", result)
            return False
    
    def test_frame_count_logic(self) -> bool:
        """Test 3: Frame count logic improvements"""
        print("\n🔬 Testing Frame Count Logic Improvements...")
        
        try:
            start_time = time.time()
            
            # Get analysis
            detected_scenes = detect_optimal_scene_count(TEST_SCREENPLAY)
            analysis = fast_ai_analyze_screenplay(TEST_SCREENPLAY, detected_scenes)
            
            # Check frame allocation
            total_frames = 0
            repetitive_scenes = 0
            reasonable_frame_counts = 0
            
            for scene in analysis.get('scenes', []):
                frames_needed = scene.get('frames_needed', 1)
                total_frames += frames_needed
                
                # Check for reasonable frame counts (should be 1-2, not 3-4)
                if frames_needed <= 2:
                    reasonable_frame_counts += 1
                
                # Check for scenes that should only have 1 frame
                scene_desc = scene.get('description', '').lower()
                if any(keyword in scene_desc for keyword in ['realizes', 'discovers', 'checks', 'looks at']):
                    if frames_needed == 1:
                        repetitive_scenes += 1
            
            duration = time.time() - start_time
            
            # Validate results
            avg_frames_per_scene = total_frames / len(analysis.get('scenes', [1]))
            frame_count_reasonable = avg_frames_per_scene <= 1.5  # Should average 1.5 or less
            most_scenes_reasonable = reasonable_frame_counts >= len(analysis.get('scenes', [])) * 0.8
            
            result = {
                'success': frame_count_reasonable and most_scenes_reasonable,
                'details': f"Avg frames/scene: {avg_frames_per_scene:.2f}, Total frames: {total_frames}, Reasonable: {reasonable_frame_counts}/{len(analysis.get('scenes', []))}"
            }
            
            self.log_test("Frame_Count_Logic", result, duration)
            return result['success']
            
        except Exception as e:
            result = {'success': False, 'error': str(e)}
            self.log_test("Frame_Count_Logic", result)
            return False
    
    def test_style_consistency(self) -> bool:
        """Test 4: Style consistency enhancements"""
        print("\n🔬 Testing Style Consistency Enhancements...")
        
        try:
            start_time = time.time()
            
            # Test style DNA generation
            styles = ['classic', 'cinematic', 'sketch', 'comic']
            style_dnas = {}
            
            for style in styles:
                style_prompt = f"{style} storyboard style"
                style_dna = get_style_dna(style_prompt)
                style_dnas[style] = style_dna
                
                # Check for consistency keywords
                consistency_keywords = ['consistent', 'uniform', 'professional', 'quality']
                has_consistency = any(keyword in style_dna.lower() for keyword in consistency_keywords)
                
                if not has_consistency:
                    result = {
                        'success': False,
                        'error': f"Style DNA for {style} lacks consistency keywords"
                    }
                    self.log_test("Style_Consistency", result)
                    return False
            
            duration = time.time() - start_time
            
            # Check that all styles have the base DNA elements
            base_elements = ['professional storyboard', 'black and white', 'line art']
            all_have_base = all(
                all(element in dna.lower() for element in base_elements)
                for dna in style_dnas.values()
            )
            
            result = {
                'success': all_have_base,
                'details': f"Generated {len(style_dnas)} style DNAs with consistency enhancements"
            }
            
            self.log_test("Style_Consistency", result, duration)
            return result['success']
            
        except Exception as e:
            result = {'success': False, 'error': str(e)}
            self.log_test("Style_Consistency", result)
            return False
    
    def test_full_generation_pipeline(self) -> bool:
        """Test 5: Full generation pipeline integration"""
        print("\n🔬 Testing Full Generation Pipeline...")
        
        try:
            start_time = time.time()
            
            # Run full pipeline
            detected_scenes = detect_optimal_scene_count(TEST_SCREENPLAY)
            analysis = fast_ai_analyze_screenplay(TEST_SCREENPLAY, detected_scenes)
            
            # Test frame generation (just first scene to avoid long wait)
            first_scene = analysis.get('scenes', [{}])[0]
            if first_scene:
                try:
                    frame = generate_ai_frame_sync(
                        first_scene, 
                        1, 
                        'Professional storyboard, black and white line art',
                        analysis
                    )
                    generation_successful = frame and frame.get('status') == 'completed'
                except Exception as gen_error:
                    generation_successful = False
                    print(f"   Frame generation error: {gen_error}")
            else:
                generation_successful = False
            
            duration = time.time() - start_time
            
            # Validate pipeline
            has_analysis = bool(analysis.get('scenes'))
            has_characters = bool(analysis.get('characters'))
            pipeline_complete = has_analysis and has_characters
            
            result = {
                'success': pipeline_complete and generation_successful,
                'details': f"Analysis: {has_analysis}, Characters: {has_characters}, Generation: {generation_successful}"
            }
            
            self.log_test("Full_Generation_Pipeline", result, duration)
            return result['success']
            
        except Exception as e:
            result = {'success': False, 'error': str(e)}
            self.log_test("Full_Generation_Pipeline", result)
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        print("🚀 Starting Performance Test Suite...")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        tests = [
            self.test_ai_analysis_speed,
            self.test_event_loop_conflicts,
            self.test_frame_count_logic,
            self.test_style_consistency,
            self.test_full_generation_pipeline
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed += 1
        
        total_duration = time.time() - start_time
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🏁 Test Suite Complete ({total_duration:.2f}s)")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Success Rate: {passed/(passed+failed)*100:.1f}%")
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED! Fixes are working correctly.")
        else:
            print("⚠️  Some tests failed. Check the details above.")
        
        return {
            'total_tests': passed + failed,
            'passed': passed,
            'failed': failed,
            'success_rate': passed/(passed+failed)*100 if (passed+failed) > 0 else 0,
            'total_duration': total_duration,
            'results': self.results
        }

def main():
    """Run the performance test suite"""
    print("🧪 Script Fury Simple - Performance Test Suite")
    print("Testing fixes for speed, stability, and quality improvements")
    print()
    
    # Create test suite
    suite = PerformanceTestSuite()
    
    # Run tests
    summary = suite.run_all_tests()
    
    # Save results
    results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    # Exit with appropriate code
    exit_code = 0 if summary['failed'] == 0 else 1
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)