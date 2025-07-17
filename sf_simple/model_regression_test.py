#!/usr/bin/env python3
"""
Comprehensive GPT Model Regression Test for Script Fury Simple
Tests different models for SPEED vs QUALITY vs ACCURACY
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_analyzer import fast_ai_analyze_screenplay, detect_optimal_scene_count
from utils.model_config import get_model_for_task

# Test screenplay samples
TEST_SCRIPTS = {
    "short_action": """
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

FADE OUT.
""",
    
    "character_heavy": """
FADE IN:

INT. CONFERENCE ROOM - DAY

SARAH MARTINEZ, the lead detective, addresses her team.

SARAH
We have five suspects.

DETECTIVE BROWN nods. OFFICER JOHNSON takes notes. CAPTAIN WILLIAMS observes.

SARAH
First, TOMMY GARCIA, the ex-boyfriend.

TOMMY enters, nervous and sweating.

TOMMY
I didn't do anything wrong.

SARAH
Second, MARIA RODRIGUEZ, the roommate.

MARIA sits down, defensive.

MARIA
She was my best friend.

SARAH
Third, DAVID CHEN, the coworker.

DAVID adjusts his glasses nervously.

DAVID
We only worked together.

SARAH
Fourth, REBECCA SMITH, the neighbor.

REBECCA crosses her arms.

REBECCA
I barely knew her.

SARAH
Finally, JAMES PETERSON, the landlord.

JAMES enters reluctantly.

JAMES
I just collect rent.

SARAH
One of you is lying.

FADE OUT.
""",
    
    "complex_scenes": """
FADE IN:

EXT. ABANDONED WAREHOUSE - NIGHT

Rain pours down. Lightning illuminates the scene.

INT. WAREHOUSE - CONTINUOUS

ALEX HUNTER creeps through the shadows. Footsteps echo.

ALEX
(whispering)
Where are you?

FLASHBACK - EXT. PARK - DAY (EARLIER)

ALEX meets INFORMANT, a nervous man in a coat.

INFORMANT
They're planning something big tonight.

ALEX
Where?

INFORMANT
The old warehouse on Fifth Street.

BACK TO PRESENT - INT. WAREHOUSE - NIGHT

Alex discovers a room full of COMPUTER EQUIPMENT.

ALEX
(amazed)
This is it.

Suddenly, FOOTSTEPS approach. Alex hides.

VOICE (O.S.)
The upload is complete.

ALEX
(to himself)
Upload of what?

A FIGURE emerges from the shadows - it's DETECTIVE KANE.

KANE
(into phone)
Phase one is complete. Initiate phase two.

Alex's eyes widen in shock.

ALEX
(whispered)
Kane... you're the mole.

FADE OUT.
"""
}

# Model configurations to test
MODEL_CONFIGS = {
    "FAST": {
        "character_extraction": "o3-mini",
        "scene_analysis": "o3-mini", 
        "basic_info_extraction": "o3-mini",
        "prompt_sanitization": "o3-mini"
    },
    "BALANCED": {
        "character_extraction": "gpt-4o",
        "scene_analysis": "gpt-4o",
        "basic_info_extraction": "gpt-4o-mini",
        "prompt_sanitization": "o3-mini"
    },
    "SMART": {
        "character_extraction": "gpt-4o",
        "scene_analysis": "gpt-4o",
        "basic_info_extraction": "gpt-4o",
        "prompt_sanitization": "gpt-4o"
    },
    "PREMIUM": {
        "character_extraction": "gpt-4o",
        "scene_analysis": "gpt-4o",
        "basic_info_extraction": "gpt-4o",
        "prompt_sanitization": "gpt-4o"
    }
}

class ModelRegressionTester:
    """Comprehensive model testing system"""
    
    def __init__(self):
        self.results = {}
        self.original_env = {}
        
    def backup_env(self):
        """Backup original environment variables"""
        model_vars = [
            'CHARACTER_MODEL', 'SCENE_MODEL', 'INFO_MODEL', 
            'SANITIZATION_MODEL', 'MODEL_MODE'
        ]
        for var in model_vars:
            self.original_env[var] = os.getenv(var)
            
    def restore_env(self):
        """Restore original environment variables"""
        for var, value in self.original_env.items():
            if value:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]
                
    def set_model_config(self, config_name: str, config: Dict[str, str]):
        """Set environment variables for model configuration"""
        os.environ['CHARACTER_MODEL'] = config['character_extraction']
        os.environ['SCENE_MODEL'] = config['scene_analysis']
        os.environ['INFO_MODEL'] = config['basic_info_extraction']
        os.environ['SANITIZATION_MODEL'] = config['prompt_sanitization']
        os.environ['MODEL_MODE'] = config_name.lower()
        
    def test_model_config(self, config_name: str, config: Dict[str, str], 
                         script_name: str, script_text: str) -> Dict[str, Any]:
        """Test a specific model configuration"""
        print(f"\n🧪 Testing {config_name} model config on {script_name}")
        print(f"   Models: {config}")
        
        # Set model configuration
        self.set_model_config(config_name, config)
        
        # Run timing test
        start_time = time.time()
        
        try:
            # Detect optimal scene count
            detected_scenes = detect_optimal_scene_count(script_text)
            
            # Run analysis
            analysis = fast_ai_analyze_screenplay(script_text, detected_scenes)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Calculate metrics
            total_scenes = analysis.get('total_scenes', 0)
            total_frames = sum(scene.get('frames_needed', 1) for scene in analysis.get('scenes', []))
            characters = analysis.get('characters', {})
            
            # Validate scene/frame accuracy
            scenes_with_frames = analysis.get('scenes', [])
            actual_frame_count = 0
            for scene in scenes_with_frames:
                frames_needed = scene.get('frames_needed', 1)
                actual_frame_count += frames_needed
                
            # Character quality assessment
            character_quality = self.assess_character_quality(characters)
            scene_quality = self.assess_scene_quality(scenes_with_frames)
            
            result = {
                'config_name': config_name,
                'script_name': script_name,
                'models': config,
                'duration': duration,
                'detected_scenes': detected_scenes,
                'total_scenes': total_scenes,
                'total_frames': total_frames,
                'actual_frame_count': actual_frame_count,
                'character_count': len(characters),
                'character_quality': character_quality,
                'scene_quality': scene_quality,
                'success': True,
                'error': None,
                'analysis': analysis
            }
            
            print(f"   ✅ Success: {duration:.2f}s, {len(characters)} chars, {total_scenes} scenes, {actual_frame_count} frames")
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            result = {
                'config_name': config_name,
                'script_name': script_name,
                'models': config,
                'duration': duration,
                'success': False,
                'error': str(e),
                'total_scenes': 0,
                'total_frames': 0,
                'character_count': 0,
                'character_quality': 0,
                'scene_quality': 0
            }
            
            print(f"   ❌ Failed: {e}")
            return result
            
    def assess_character_quality(self, characters: Dict[str, Any]) -> float:
        """Assess character extraction quality (0-10)"""
        if not characters:
            return 0
            
        score = 0
        total_chars = len(characters)
        
        for char_name, char_info in characters.items():
            char_score = 0
            
            # Name quality (proper names, not garbage)
            if (len(char_name) > 1 and 
                not char_name.endswith('!') and 
                not char_name.endswith('.') and
                not char_name.startswith('AAAA') and
                char_name not in ['LAPD', 'SWAT', 'FBI', 'OUT', 'STOP']):
                char_score += 3
                
            # Description quality
            description = char_info.get('description', '')
            if description and len(description) > 10:
                char_score += 2
                
            # Distinctive features
            features = char_info.get('distinctive_features', '')
            if features and len(features) > 5:
                char_score += 2
                
            # Role classification
            role = char_info.get('role', '')
            if role and role in ['protagonist', 'antagonist', 'supporting']:
                char_score += 3
                
            score += char_score
            
        return min(10, (score / total_chars) if total_chars > 0 else 0)
        
    def assess_scene_quality(self, scenes: List[Dict[str, Any]]) -> float:
        """Assess scene analysis quality (0-10)"""
        if not scenes:
            return 0
            
        score = 0
        total_scenes = len(scenes)
        
        for scene in scenes:
            scene_score = 0
            
            # Scene structure completeness
            required_fields = ['scene_number', 'location', 'description', 'characters']
            present_fields = sum(1 for field in required_fields if scene.get(field))
            scene_score += (present_fields / len(required_fields)) * 3
            
            # Frame logic
            frames_needed = scene.get('frames_needed', 1)
            if 1 <= frames_needed <= 3:
                scene_score += 2
                
            # Scene type classification
            scene_type = scene.get('scene_type', '')
            if scene_type in ['action', 'dialogue', 'establishing', 'emotional', 'climax']:
                scene_score += 2
                
            # Importance scoring
            importance = scene.get('importance', 0)
            if 1 <= importance <= 10:
                scene_score += 1
                
            # Visual complexity
            complexity = scene.get('visual_complexity', '')
            if complexity in ['simple', 'medium', 'complex']:
                scene_score += 1
                
            # Story beat identification
            story_beat = scene.get('story_beat', '')
            if story_beat:
                scene_score += 1
                
            score += scene_score
            
        return min(10, (score / total_scenes) if total_scenes > 0 else 0)
        
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test across all model configurations"""
        print("🚀 COMPREHENSIVE MODEL REGRESSION TEST")
        print("=" * 80)
        
        # Backup original environment
        self.backup_env()
        
        try:
            all_results = []
            
            # Test each model configuration
            for config_name, config in MODEL_CONFIGS.items():
                print(f"\n📊 TESTING {config_name} CONFIGURATION")
                print("-" * 50)
                
                config_results = []
                
                # Test on each script
                for script_name, script_text in TEST_SCRIPTS.items():
                    result = self.test_model_config(config_name, config, script_name, script_text)
                    config_results.append(result)
                    all_results.append(result)
                    
                # Calculate config averages
                successful_results = [r for r in config_results if r['success']]
                if successful_results:
                    avg_duration = sum(r['duration'] for r in successful_results) / len(successful_results)
                    avg_character_quality = sum(r['character_quality'] for r in successful_results) / len(successful_results)
                    avg_scene_quality = sum(r['scene_quality'] for r in successful_results) / len(successful_results)
                    
                    print(f"\n📈 {config_name} AVERAGES:")
                    print(f"   Duration: {avg_duration:.2f}s")
                    print(f"   Character Quality: {avg_character_quality:.1f}/10")
                    print(f"   Scene Quality: {avg_scene_quality:.1f}/10")
                    print(f"   Success Rate: {len(successful_results)}/{len(config_results)}")
                    
            # Generate final report
            return self.generate_final_report(all_results)
            
        finally:
            # Restore original environment
            self.restore_env()
            
    def generate_final_report(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        print("\n" + "=" * 80)
        print("📊 FINAL MODEL REGRESSION REPORT")
        print("=" * 80)
        
        # Group results by configuration
        config_groups = {}
        for result in all_results:
            config_name = result['config_name']
            if config_name not in config_groups:
                config_groups[config_name] = []
            config_groups[config_name].append(result)
            
        # Calculate comprehensive metrics
        final_rankings = {}
        
        for config_name, results in config_groups.items():
            successful_results = [r for r in results if r['success']]
            
            if successful_results:
                avg_duration = sum(r['duration'] for r in successful_results) / len(successful_results)
                avg_character_quality = sum(r['character_quality'] for r in successful_results) / len(successful_results)
                avg_scene_quality = sum(r['scene_quality'] for r in successful_results) / len(successful_results)
                avg_character_count = sum(r['character_count'] for r in successful_results) / len(successful_results)
                success_rate = len(successful_results) / len(results)
                
                # Calculate composite score
                speed_score = max(0, 10 - avg_duration)  # Faster = better
                quality_score = (avg_character_quality + avg_scene_quality) / 2
                reliability_score = success_rate * 10
                
                composite_score = (speed_score * 0.3 + quality_score * 0.5 + reliability_score * 0.2)
                
                final_rankings[config_name] = {
                    'avg_duration': avg_duration,
                    'avg_character_quality': avg_character_quality,
                    'avg_scene_quality': avg_scene_quality,
                    'avg_character_count': avg_character_count,
                    'success_rate': success_rate,
                    'composite_score': composite_score,
                    'speed_score': speed_score,
                    'quality_score': quality_score,
                    'reliability_score': reliability_score
                }
            else:
                final_rankings[config_name] = {
                    'avg_duration': 999,
                    'avg_character_quality': 0,
                    'avg_scene_quality': 0,
                    'avg_character_count': 0,
                    'success_rate': 0,
                    'composite_score': 0,
                    'speed_score': 0,
                    'quality_score': 0,
                    'reliability_score': 0
                }
                
        # Sort by composite score
        sorted_configs = sorted(final_rankings.items(), key=lambda x: x[1]['composite_score'], reverse=True)
        
        print("\n🏆 FINAL RANKINGS (by composite score):")
        print("-" * 50)
        
        for i, (config_name, metrics) in enumerate(sorted_configs, 1):
            print(f"{i}. {config_name}")
            print(f"   Composite Score: {metrics['composite_score']:.1f}/10")
            print(f"   Speed: {metrics['avg_duration']:.2f}s (score: {metrics['speed_score']:.1f})")
            print(f"   Quality: {metrics['quality_score']:.1f}/10")
            print(f"   Reliability: {metrics['success_rate']:.1%}")
            print(f"   Character Quality: {metrics['avg_character_quality']:.1f}/10")
            print(f"   Scene Quality: {metrics['avg_scene_quality']:.1f}/10")
            print()
            
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        print("-" * 50)
        
        winner = sorted_configs[0]
        print(f"🥇 BEST OVERALL: {winner[0]}")
        print(f"   Use this for production - best balance of speed, quality, and reliability")
        
        # Find fastest
        fastest = min(final_rankings.items(), key=lambda x: x[1]['avg_duration'])
        print(f"⚡ FASTEST: {fastest[0]} ({fastest[1]['avg_duration']:.2f}s)")
        
        # Find highest quality
        highest_quality = max(final_rankings.items(), key=lambda x: x[1]['quality_score'])
        print(f"🎯 HIGHEST QUALITY: {highest_quality[0]} ({highest_quality[1]['quality_score']:.1f}/10)")
        
        # Save detailed report
        report_data = {
            'test_timestamp': datetime.now().isoformat(),
            'rankings': final_rankings,
            'all_results': all_results,
            'winner': winner[0],
            'fastest': fastest[0],
            'highest_quality': highest_quality[0]
        }
        
        # Save to file
        with open('model_regression_report.json', 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"\n📄 Detailed report saved to: model_regression_report.json")
        
        return report_data

def main():
    """Run the comprehensive model regression test"""
    tester = ModelRegressionTester()
    report = tester.run_comprehensive_test()
    
    print("\n🎉 MODEL REGRESSION TEST COMPLETE!")
    print(f"Winner: {report['winner']}")
    print(f"Recommendation: Use {report['winner']} for optimal balance of speed and quality")

if __name__ == "__main__":
    main()