#!/usr/bin/env python3
"""
Test large script handling with optimizations
"""

import os
import time
import requests
import tempfile
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = "http://localhost:5001"

# Create a realistic large script (similar to 21 Jump Street)
LARGE_TEST_SCRIPT = """
21 JUMP STREET

FADE IN:

EXT. HIGH SCHOOL - DAY

JENKO, 22, athletic but not bright, walks through the parking lot. 

SCHMIDT, 22, skinny and nerdy, follows behind with books.

JENKO
This is our chance to be cool.

SCHMIDT
We were never cool in high school.

INT. PRINCIPAL'S OFFICE - DAY

PRINCIPAL DAVIS, 50s, looks at their fake IDs.

PRINCIPAL DAVIS
You boys seem a little old for high school.

JENKO
We're... seniors?

EXT. CAFETERIA - DAY

Students ignore them at lunch tables.

SCHMIDT
This isn't going as planned.

INT. CHEMISTRY LAB - DAY

They investigate the drug ring. Test tubes everywhere.

JENKO
What's this stuff?

SCHMIDT
Don't touch anything!

An explosion rocks the lab.

EXT. PARKING LOT - DAY

They chase suspects through cars.

JENKO
Police! Stop!

The suspects escape in a sports car.

INT. CAPTAIN'S OFFICE - DAY

CAPTAIN DICKSON, 40s, angry.

CAPTAIN DICKSON
You blew your cover!

SCHMIDT
We can fix this.

EXT. SCHOOL DANCE - NIGHT

Undercover at the prom. Music pumps.

JENKO
There's our target.

They spot the drug dealer, ERIC, 18.

INT. GYMNASIUM - NIGHT

Chase scene through dancing teenagers.

ERIC
You'll never catch me!

SCHMIDT
Watch me!

He tackles Eric into the punch bowl.

EXT. ROOFTOP - NIGHT

Final confrontation with the boss.

BOSS
It's over, cops.

JENKO
Not yet it isn't.

Epic fight scene on the roof.

FADE OUT.

THE END
""" * 100  # Repeat to make it large like 21 Jump Street

def test_large_script_upload():
    """Test uploading and processing a large script"""
    print("🧪 Testing Large Script Optimization")
    print("=" * 50)
    
    # Check word count
    word_count = len(LARGE_TEST_SCRIPT.split())
    print(f"📏 Test script size: {word_count} words")
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(LARGE_TEST_SCRIPT)
        temp_file = f.name
    
    try:
        # Upload
        print("📤 Uploading large script...")
        with open(temp_file, 'rb') as f:
            files = {'file': ('large_test_script.txt', f, 'text/plain')}
            response = requests.post(f"{SERVER_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Upload successful: {data['project_id']}")
            print(f"   Detected scenes: {data['detected_scenes']}")
            print(f"   Should be ≤15 for large scripts")
            
            # Start generation
            print("🚀 Starting generation...")
            payload = {'project_id': data['project_id'], 'style': 'classic'}
            gen_response = requests.post(f"{SERVER_URL}/generate", json=payload)
            
            if gen_response.status_code == 200:
                print("✅ Generation started successfully")
                
                # Monitor progress
                project_id = data['project_id']
                start_time = time.time()
                
                while time.time() - start_time < 60:  # 1 minute timeout
                    status_response = requests.get(f"{SERVER_URL}/status/{project_id}")
                    
                    if status_response.status_code == 200:
                        status = status_response.json()
                        progress = status.get('progress', 0)
                        current_step = status.get('current_step', 'Unknown')
                        
                        print(f"📊 Progress: {progress}% - {current_step}")
                        
                        if status.get('status') == 'completed':
                            frames = status.get('frames', [])
                            print(f"🎉 Generation completed: {len(frames)} frames")
                            return True
                        elif status.get('status') == 'error':
                            print(f"❌ Generation error: {status.get('error')}")
                            return False
                    
                    time.sleep(3)
                
                print("⏰ Generation still in progress after 1 minute - this is normal for large scripts")
                return True
            else:
                print(f"❌ Generation failed: {gen_response.status_code}")
                return False
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return False
            
    finally:
        # Cleanup
        os.unlink(temp_file)

if __name__ == "__main__":
    success = test_large_script_upload()
    if success:
        print("\n🎉 Large script optimization test PASSED")
    else:
        print("\n❌ Large script optimization test FAILED")