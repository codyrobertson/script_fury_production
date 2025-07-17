#!/usr/bin/env python3
"""
Test scene/frame counting accuracy with 21 Jump Street script
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_analyzer import fast_ai_analyze_screenplay, detect_optimal_scene_count

# Sample from 21 Jump Street script
JUMP_STREET_SAMPLE = """
FADE IN:

EXT. GHETTO STREET - DAY

Two 21-year-old bike patrol officers, JENKO and SCHMIDT, 
cruise down the street. Jenko is tough looking but actually 
pretty dumb. Schmidt is the smart one but insecure about it.

JENKO
(into radio)
21 Jump Street, this is Unit 414.

SCHMIDT
(nervous)
Should we really be doing this?

A DRUG DEALER on the corner spots them.

DRUG DEALER
(shouting)
LAPD! LAPD! Run!

The dealer runs. Various GANG MEMBERS scatter.

GANG MEMBER #1
(yelling)
AAAAAH! The cops!

GANG MEMBER #2
(screaming)
AAAAARGH! Let's go!

JENKO
(to Schmidt)
Come on, let's get them!

They chase the dealer into an alley.

INT. POLICE STATION - LATER

CAPTAIN DICKS, a gruff 50-year-old, addresses the two officers.

CAPTAIN DICKS
You two screwed up big time.

SCHMIDT
(defensive)
We were just trying to help.

JENKO
(confused)
What did we do wrong?

CAPTAIN DICKS
You let the dealer get away because you can't 
work as a team.

A CONCERNED GIRL enters the station.

CONCERNED GIRL
Excuse me, officers. I have information about 
the drug activity.

BLAKEY, a desk sergeant, looks up.

BLAKEY
What kind of information?

CONCERNED GIRL
I saw everything. The dealer was selling to 
high school kids.

INT. HIGH SCHOOL - CONTINUOUS

JENKO and SCHMIDT walk through the hallways undercover.

JENKO
(whispering)
This place looks exactly like our old school.

SCHMIDT
(nervous)
Just act natural.

They approach a group of STUDENTS.

STUDENT #1
(suspicious)
Who are you guys?

JENKO
(trying to be cool)
We're... new students.

STUDENT #2
(laughing)
You look like cops.

SCHMIDT
(panicking)
What? No! We're totally not cops!

The students walk away laughing.

JENKO
(frustrated)
This isn't working.

SCHMIDT
We need to blend in better.

They spot the POPULAR GIRL, MOLLY, at her locker.

MOLLY
(to her friends)
Did you see those weird new guys?

FRIEND #1
They definitely don't belong here.

FRIEND #2
Something's off about them.

JENKO
(to Schmidt)
We need to get invited to parties.

SCHMIDT
How do we do that?

MOLLY approaches them.

MOLLY
(curious)
Are you guys really students here?

JENKO
(lying badly)
Yeah, totally. We're... transfer students.

MOLLY
From where?

SCHMIDT
(quickly)
Canada.

MOLLY
(suspiciously)
Canada? Which part?

JENKO
(panicking)
The... Canadian part.

MOLLY walks away, clearly not convinced.

FADE OUT.
"""

def test_scene_frame_accuracy():
    """Test scene and frame counting accuracy"""
    print("🎬 SCENE/FRAME ACCURACY TEST")
    print("=" * 60)
    
    print("📝 Testing 21 Jump Street sample...")
    print(f"   Script length: {len(JUMP_STREET_SAMPLE.split())} words")
    
    # Detect optimal scene count
    detected_scenes = detect_optimal_scene_count(JUMP_STREET_SAMPLE)
    print(f"   Detected optimal scenes: {detected_scenes}")
    
    # Run analysis
    analysis = fast_ai_analyze_screenplay(JUMP_STREET_SAMPLE, detected_scenes)
    
    # Extract metrics
    characters = analysis.get('characters', {})
    scenes = analysis.get('scenes', [])
    total_scenes = analysis.get('total_scenes', 0)
    total_frames = analysis.get('total_frames', 0)
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   Title: {analysis.get('title', 'Unknown')}")
    print(f"   Total scenes: {total_scenes}")
    print(f"   Total frames: {total_frames}")
    print(f"   Characters: {len(characters)}")
    
    # Validate frame counting
    manual_frame_count = 0
    print(f"\n🎬 SCENE BREAKDOWN:")
    for i, scene in enumerate(scenes, 1):
        scene_number = scene.get('scene_number', i)
        location = scene.get('location', 'Unknown')
        frames_needed = scene.get('frames_needed', 1)
        scene_type = scene.get('scene_type', 'unknown')
        importance = scene.get('importance', 5)
        
        print(f"   Scene {scene_number}: {location}")
        print(f"      Type: {scene_type}")
        print(f"      Frames needed: {frames_needed}")
        print(f"      Importance: {importance}/10")
        
        manual_frame_count += frames_needed
        
    print(f"\n🧮 FRAME COUNT VERIFICATION:")
    print(f"   Reported total frames: {total_frames}")
    print(f"   Manual count: {manual_frame_count}")
    print(f"   Frame accuracy: {'✅' if total_frames == manual_frame_count else '❌'}")
    
    # Character validation
    print(f"\n👥 CHARACTER VALIDATION:")
    expected_chars = ['JENKO', 'SCHMIDT', 'CAPTAIN DICKS', 'CONCERNED GIRL', 'BLAKEY', 'MOLLY']
    garbage_chars = ['AAAAAH', 'AAAAARGH', 'LAPD', 'DRUG DEALER']
    
    found_expected = 0
    found_garbage = 0
    
    for char_name in characters.keys():
        if any(expected in char_name.upper() for expected in expected_chars):
            found_expected += 1
        if any(garbage in char_name.upper() for garbage in garbage_chars):
            found_garbage += 1
            
    print(f"   Expected characters found: {found_expected}/{len(expected_chars)}")
    print(f"   Garbage characters found: {found_garbage}")
    print(f"   Character quality: {'✅' if found_garbage == 0 else '❌'}")
    
    # Detailed character list
    print(f"\n📋 CHARACTER LIST:")
    for char_name, char_info in characters.items():
        role = char_info.get('role', 'unknown')
        description = char_info.get('description', 'No description')
        print(f"   {char_name} ({role}): {description}")
    
    # Scene-to-frame ratio analysis
    print(f"\n📈 SCENE-TO-FRAME ANALYSIS:")
    scene_types = {}
    for scene in scenes:
        scene_type = scene.get('scene_type', 'unknown')
        frames = scene.get('frames_needed', 1)
        if scene_type not in scene_types:
            scene_types[scene_type] = []
        scene_types[scene_type].append(frames)
        
    for scene_type, frame_counts in scene_types.items():
        avg_frames = sum(frame_counts) / len(frame_counts)
        print(f"   {scene_type}: {len(frame_counts)} scenes, {avg_frames:.1f} avg frames")
    
    # Final validation
    print(f"\n🎯 FINAL VALIDATION:")
    all_valid = (
        total_frames == manual_frame_count and
        found_garbage == 0 and
        total_scenes == len(scenes) and
        total_scenes > 0 and
        len(characters) > 0
    )
    
    print(f"   Scene count consistency: {'✅' if total_scenes == len(scenes) else '❌'}")
    print(f"   Frame count accuracy: {'✅' if total_frames == manual_frame_count else '❌'}")
    print(f"   Character quality: {'✅' if found_garbage == 0 else '❌'}")
    print(f"   Data completeness: {'✅' if total_scenes > 0 and len(characters) > 0 else '❌'}")
    
    if all_valid:
        print(f"\n🎉 ALL TESTS PASSED - Scene/Frame counting is accurate!")
        return True
    else:
        print(f"\n❌ Some tests failed - needs improvement")
        return False

if __name__ == "__main__":
    success = test_scene_frame_accuracy()
    exit(0 if success else 1)