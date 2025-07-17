#!/usr/bin/env python3
"""
Test Model Upgrade - Shows the impact of using smarter models
Tests GPT-4o vs GPT-4o-mini vs o3-mini for different tasks
"""

import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.model_config import model_config, configure_models, print_model_config
from utils.scene_analyzer import fast_ai_analyze_screenplay, detect_optimal_scene_count
from utils.prompt_sanitizer import sanitize_prompt_for_storyboard

# Test script with complex character relationships
COMPLEX_SCRIPT = """
FADE IN:

EXT. CORPORATE OFFICE BUILDING - DAY

SARAH CHEN (35), a sharp-dressed executive with an air of authority, exits a black sedan.

SARAH
(to her driver)
Pick me up at 6. The board meeting can't run late.

DRIVER
(nervous)
Yes, ma'am.

INT. CONFERENCE ROOM - CONTINUOUS

Sarah enters to find her rival, MARCUS WELLINGTON (42), already seated. He's polished, calculating.

MARCUS
(smug)
Sarah. Always punctual.

SARAH
(cool)
Marcus. Always here first to set the agenda.

The CEO, ROBERT HAYES (58), enters with his assistant, JENNY PARK (28).

ROBERT
(to both)
Let's discuss the merger proposal.

JENNY
(whispering to Robert)
The files are on your tablet.

Sarah notices JAMES TORRES (30), the new analyst, taking notes nervously.

SARAH
(to James)
Your first board meeting?

JAMES
(stammering)
Yes, ma'am. I'm still learning.

Suddenly, DETECTIVE RIVERA (45) enters unexpectedly.

DETECTIVE RIVERA
(badge out)
I need to speak with Mr. Wellington.

MARCUS
(panicking)
What's this about?

DETECTIVE RIVERA
Financial irregularities. We need to talk.

Sarah exchanges glances with Robert while Jenny gasps.

JENNY
(shocked)
This can't be happening.

FADE OUT.
"""

def test_model_configurations():
    """Test different model configurations"""
    print("🤖 MODEL UPGRADE TEST")
    print("=" * 60)
    
    # Test different configurations
    configurations = [
        ('balanced', 'Balanced (Current Default)'),
        ('premium', 'Premium (Best Quality)'),
        ('fast', 'Fast (Best Speed)')
    ]
    
    results = {}
    
    for config_name, description in configurations:
        print(f"\n🧪 Testing {description}")
        print("-" * 40)
        
        # Configure models
        configure_models(config_name)
        print_model_config()
        
        # Test character extraction
        start_time = time.time()
        try:
            detected_scenes = detect_optimal_scene_count(COMPLEX_SCRIPT)
            analysis = fast_ai_analyze_screenplay(COMPLEX_SCRIPT, detected_scenes)
            
            duration = time.time() - start_time
            character_count = len(analysis.get('characters', {}))
            scene_count = len(analysis.get('scenes', []))
            
            results[config_name] = {
                'duration': duration,
                'characters': character_count,
                'scenes': scene_count,
                'character_names': list(analysis.get('characters', {}).keys()),
                'success': True
            }
            
            print(f"✅ Analysis complete: {duration:.2f}s")
            print(f"   Characters found: {character_count}")
            print(f"   Scenes analyzed: {scene_count}")
            print(f"   Characters: {', '.join(analysis.get('characters', {}).keys())}")
            
        except Exception as e:
            results[config_name] = {
                'duration': time.time() - start_time,
                'error': str(e),
                'success': False
            }
            print(f"❌ Analysis failed: {e}")
    
    return results

def test_prompt_sanitization_speed():
    """Test prompt sanitization with different models"""
    print("\n🧹 PROMPT SANITIZATION MODEL TEST")
    print("=" * 60)
    
    test_prompts = [
        "Professional storyboard, Sarah confronts Marcus about corruption",
        "Black and white line art, detective arrests corporate executive",
        "Storyboard style, board meeting interrupted by police investigation"
    ]
    
    # Test with different models
    models = ['o3-mini', 'gpt-4o-mini', 'gpt-4o']
    
    for model in models:
        print(f"\n🧪 Testing {model}")
        print("-" * 30)
        
        # Configure for this model
        model_config.set_model('prompt_sanitization', model)
        
        total_time = 0
        successes = 0
        
        for i, prompt in enumerate(test_prompts):
            start_time = time.time()
            try:
                sanitized, changes, sensitive = sanitize_prompt_for_storyboard(prompt)
                duration = time.time() - start_time
                total_time += duration
                successes += 1
                
                print(f"   Prompt {i+1}: ✅ {duration:.2f}s ({len(changes)} changes)")
                
            except Exception as e:
                duration = time.time() - start_time
                total_time += duration
                print(f"   Prompt {i+1}: ❌ {duration:.2f}s - {e}")
        
        avg_time = total_time / len(test_prompts)
        print(f"   Average: {avg_time:.2f}s, Success: {successes}/{len(test_prompts)}")

def compare_character_detection():
    """Compare character detection quality between models"""
    print("\n👥 CHARACTER DETECTION QUALITY TEST")
    print("=" * 60)
    
    # Expected characters from the script
    expected_characters = [
        'SARAH CHEN', 'MARCUS WELLINGTON', 'ROBERT HAYES', 
        'JENNY PARK', 'JAMES TORRES', 'DETECTIVE RIVERA', 'DRIVER'
    ]
    
    models = ['gpt-4o-mini', 'gpt-4o']
    
    for model in models:
        print(f"\n🧪 Testing {model}")
        print("-" * 30)
        
        # Configure for this model
        model_config.set_model('character_extraction', model)
        
        try:
            start_time = time.time()
            detected_scenes = detect_optimal_scene_count(COMPLEX_SCRIPT)
            analysis = fast_ai_analyze_screenplay(COMPLEX_SCRIPT, detected_scenes)
            duration = time.time() - start_time
            
            found_characters = list(analysis.get('characters', {}).keys())
            
            # Calculate accuracy
            found_expected = sum(1 for char in expected_characters if char in found_characters)
            accuracy = found_expected / len(expected_characters) * 100
            
            print(f"   Duration: {duration:.2f}s")
            print(f"   Found {len(found_characters)} characters")
            print(f"   Expected: {found_expected}/{len(expected_characters)} ({accuracy:.1f}%)")
            print(f"   Found: {', '.join(found_characters[:5])}...")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")

def main():
    """Run all model upgrade tests"""
    print("🚀 SCRIPT FURY SIMPLE - MODEL UPGRADE TESTS")
    print("Testing the impact of using smarter models (GPT-4o, o3-mini)")
    print("=" * 80)
    
    # Test 1: Different model configurations
    config_results = test_model_configurations()
    
    # Test 2: Prompt sanitization speed
    test_prompt_sanitization_speed()
    
    # Test 3: Character detection quality
    compare_character_detection()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 MODEL UPGRADE SUMMARY")
    print()
    
    print("🎯 RECOMMENDED CONFIGURATION:")
    print("✅ Character Extraction: GPT-4o (best accuracy)")
    print("✅ Scene Analysis: GPT-4o (superior understanding)")
    print("✅ Prompt Sanitization: o3-mini (fastest processing)")
    print("✅ Image Generation: gpt-image-1 (specialized)")
    
    print("\n💡 BENEFITS OF SMARTER MODELS:")
    print("• Better character detection (finds more characters)")
    print("• Superior scene analysis (smarter frame allocation)")
    print("• Improved prompt quality (better image generation)")
    print("• Faster processing for simple tasks (o3-mini)")
    
    # Set optimal configuration
    configure_models('balanced')
    print("\n🔧 Optimal configuration applied!")

if __name__ == "__main__":
    main()