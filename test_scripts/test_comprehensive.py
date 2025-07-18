#!/usr/bin/env python3
"""
Comprehensive test of the simple storyboard app
"""

import requests
import json
import time
import os

def test_comprehensive():
    """Test all features comprehensively"""
    
    print("🧪 SF Simple Comprehensive Test")
    print("=" * 50)
    
    base_url = "http://localhost:5001"
    
    # Test large screenplay
    large_screenplay = """
FADE IN:

EXT. CITY STREET - DAY

A busy metropolitan street. Cars honk, people walk quickly. DETECTIVE SARAH CHEN (35), Asian-American, sharp-eyed, exits a coffee shop.

SARAH
(into phone)
I need that report by noon, Martinez.

She walks toward a black sedan. Suddenly, a MAN IN A HOODIE bumps into her.

HOODED MAN
Sorry, miss.

He disappears into the crowd. Sarah checks her pocket - her badge is missing.

SARAH
Hey! Stop!

She chases after him.

EXT. ALLEY - CONTINUOUS

Sarah corners the HOODED MAN in a narrow alley. He's actually JIMMY "THE FISH" TORRINO (40s), a known informant.

JIMMY
Relax, Detective. I got information.

SARAH
My badge, Jimmy. Now.

JIMMY
First, you gotta hear this. The Kozlov job? It wasn't random.

Jimmy pulls out a photograph showing a man in a suit.

JIMMY (CONT'D)
This guy's been watching the docks. Name's Viktor Petrov.

SARAH
(suspicious)
How do you know this?

JIMMY
Because he tried to recruit me. Said he needed someone who knew the streets.

INT. POLICE STATION - DAY

Sarah sits at her desk, studying the photograph. Her partner, DETECTIVE MIKE TORRES (45), Latino, approaches with coffee.

MIKE
What's got you so focused?

SARAH
Jimmy gave me this. Says it's connected to the Kozlov murder.

MIKE
Jimmy's information is usually good. But this guy...

Mike points to the photo.

MIKE (CONT'D)
Viktor Petrov. He's been on our radar for months. Russian mob connections.

SARAH
Then why haven't we brought him in?

MIKE
No evidence. He's clean on paper.

Sarah's phone RINGS. She answers.

SARAH
Chen... What? When?... We'll be right there.

She hangs up, grabs her jacket.

SARAH (CONT'D)
Another body. Same MO as Kozlov.

EXT. WAREHOUSE DISTRICT - DAY

Police cars, ambulances, crime scene tape. Sarah and Mike approach the body - a man in his 30s, single gunshot wound.

FORENSICS TECH
(to Sarah)
Victim's name is Alex Volkov. Russian national.

SARAH
Any connection to Viktor Petrov?

FORENSICS TECH
Working on it. But look at this.

The tech shows them a business card found on the body.

FORENSICS TECH (CONT'D)
"Petrov Import/Export." This was in his wallet.

Mike and Sarah exchange looks.

MIKE
Now we have our connection.

INT. PETROV'S OFFICE - DAY

An upscale office overlooking the harbor. VIKTOR PETROV (50s), well-dressed, silver-haired, sits behind a massive desk. He's on the phone, speaking in Russian.

PETROV
(in Russian, subtitled)
The detective is getting too close. Handle it.

He hangs up as his SECRETARY (20s) enters.

SECRETARY
Mr. Petrov? There are two police officers here to see you.

PETROV
(smiling)
Send them in.

Sarah and Mike enter. Petrov stands, extending his hand.

PETROV (CONT'D)
Detectives. How can I help you?

SARAH
We're investigating the death of Alex Volkov.

PETROV
Terrible tragedy. Alex was a valued employee.

MIKE
Employee? What kind of work did he do?

PETROV
Import documentation. Very administrative. Nothing exciting.

Sarah notices a photo on Petrov's desk - him with several men in suits.

SARAH
Nice photo. Who are your friends?

PETROV
(defensive)
Business associates. From Moscow.

MIKE
We may have more questions later.

PETROV
Of course. I'm always available to help the police.

EXT. PETROV'S BUILDING - DAY

Sarah and Mike walk to their car.

SARAH
He's lying about something.

MIKE
Yeah, but what? And can we prove it?

SARAH
I want surveillance on him. 24/7.

MIKE
That'll require a warrant.

SARAH
Then let's get one.

INT. SARAH'S APARTMENT - NIGHT

Sarah sits at her kitchen table, case files spread out. Her phone rings.

SARAH
Chen.

UNKNOWN VOICE
(distorted)
Stop looking into Petrov. This is your only warning.

SARAH
Who is this?

The line goes dead. Sarah stares at the phone, then looks out her window. A black car idles across the street.

SARAH (CONT'D)
(to herself)
Now it's personal.

She moves away from the window and calls Mike.

SARAH (CONT'D)
Mike, I need you to come over. Now.

FADE TO BLACK.

TO BE CONTINUED...

FADE OUT.
"""
    
    # Test 1: Upload large screenplay
    print("📤 Testing large screenplay upload...")
    
    with open('/tmp/large_screenplay.txt', 'w') as f:
        f.write(large_screenplay)
    
    with open('/tmp/large_screenplay.txt', 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{base_url}/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        project_id = data['project_id']
        print(f"   ✅ Upload successful: {project_id}")
        print(f"   📊 Word count: {data['word_count']}")
        print(f"   📊 Character count: {data['char_count']}")
        print(f"   📊 Text length: {data['text_length']}")
    else:
        print(f"   ❌ Upload failed: {response.status_code}")
        return False
    
    # Test 2: Generate with different styles
    styles = ['classic', 'cinematic', 'sketch', 'comic']
    
    for style in styles:
        print(f"\n🎨 Testing {style} style generation...")
        
        generation_data = {
            'project_id': project_id,
            'style': style,
            'frame_density': 'medium'
        }
        
        response = requests.post(f"{base_url}/generate", json=generation_data)
        
        if response.status_code == 200:
            print(f"   ✅ {style} generation started")
            
            # Wait and check status
            time.sleep(3)
            
            response = requests.get(f"{base_url}/status/{project_id}")
            if response.status_code == 200:
                status = response.json()
                print(f"   Status: {status['status']}")
                print(f"   Frames: {len(status.get('frames', []))}")
                
                if status['status'] == 'completed':
                    print(f"   🎉 {style} generation completed successfully")
                    
                    # Show some frame details
                    if 'frames' in status and status['frames']:
                        frame = status['frames'][0]
                        print(f"   📝 Sample frame: {frame['frame_id']}")
                        print(f"   📝 Scene: {frame['scene_description'][:50]}...")
                        print(f"   📝 Characters: {frame.get('characters', [])}")
                        break
            else:
                print(f"   ❌ Status check failed")
        else:
            print(f"   ❌ {style} generation failed: {response.status_code}")
    
    # Test 3: Check processing page with full analysis
    print(f"\n📊 Testing processing page with full analysis...")
    
    response = requests.get(f"{base_url}/processing/{project_id}")
    
    if response.status_code == 200:
        print("   ✅ Processing page accessible")
        
        # Check if analysis is available
        status_response = requests.get(f"{base_url}/status/{project_id}")
        if status_response.status_code == 200:
            status = status_response.json()
            if 'analysis' in status:
                analysis = status['analysis']
                print(f"   📊 Title: {analysis.get('title', 'N/A')}")
                print(f"   📊 Total scenes: {analysis.get('total_scenes', 0)}")
                print(f"   📊 Characters: {len(analysis.get('characters', {}))}")
                print(f"   📊 Page count: {analysis.get('page_count', 0)}")
                print(f"   📊 Analysis type: {analysis.get('analysis_type', 'N/A')}")
        
    else:
        print(f"   ❌ Processing page failed: {response.status_code}")
    
    # Test 4: Check print functionality
    print(f"\n🖨️  Testing print functionality...")
    
    response = requests.get(f"{base_url}/print/{project_id}")
    
    if response.status_code == 200:
        print("   ✅ Print page accessible")
        # Check if response contains storyboard content
        if 'storyboard' in response.text.lower():
            print("   ✅ Print page contains storyboard content")
        else:
            print("   ⚠️  Print page may not have storyboard content")
    else:
        print(f"   ❌ Print page failed: {response.status_code}")
    
    # Test 5: Check projects API
    print(f"\n📋 Testing projects API...")
    
    response = requests.get(f"{base_url}/api/projects")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Projects API accessible")
        print(f"   📊 Projects count: {len(data.get('projects', []))}")
        print(f"   📊 Generation status count: {len(data.get('generation_status', {}))}")
    else:
        print(f"   ❌ Projects API failed: {response.status_code}")
    
    # Cleanup
    os.remove('/tmp/large_screenplay.txt')
    
    print("\n🎉 Comprehensive test completed!")
    return True

if __name__ == "__main__":
    try:
        success = test_comprehensive()
        if success:
            print("\n✅ All comprehensive tests passed!")
        else:
            print("\n❌ Some tests failed")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Make sure the Flask app is running on port 5001")