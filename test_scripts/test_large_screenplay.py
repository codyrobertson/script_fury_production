#!/usr/bin/env python3
"""
Test large screenplay scene detection
"""

import os
from utils.scene_analyzer import detect_optimal_scene_count

# Create a more substantial screenplay for testing
LARGE_SCREENPLAY = """
FADE IN:

EXT. MANHATTAN STREET - DAY

The bustling streets of New York City. People rush past each other, yellow cabs honk, and the energy is palpable. DETECTIVE SARAH CHEN (35), sharp-eyed and determined, emerges from a coffee shop.

SARAH
(into phone)
I need that forensics report by noon, Martinez.

A HOODED MAN (20s) bumps into her, causing her to spill coffee.

HOODED MAN
Sorry, lady.

He melts into the crowd. Sarah feels for her badge - it's gone.

SARAH
(shouting)
Hey! Stop!

She chases after him through the crowd.

EXT. CHINATOWN ALLEY - CONTINUOUS

Sarah corners the HOODED MAN in a narrow alley. He's JIMMY "THE FISH" TORRINO (40s), a street-smart informant.

JIMMY
Relax, Detective. I got something for you.

SARAH
My badge, Jimmy. Now.

JIMMY
(pulling out a photograph)
This is bigger than your badge. The Kozlov murder? It wasn't random.

The photo shows a well-dressed man in a suit.

JIMMY (CONT'D)
Viktor Petrov. Russian mob. He's been watching the docks.

SARAH
How do you know this?

JIMMY
Because he tried to recruit me. Said he needed street connections.

INT. POLICE STATION - BULLPEN - DAY

Sarah sits at her cluttered desk, studying the photograph. Her partner, DETECTIVE MIKE TORRES (45), approaches with two cups of coffee.

MIKE
What's got you so intense?

SARAH
Jimmy gave me this. Says it's connected to the Kozlov case.

MIKE
(recognizing the photo)
Viktor Petrov. We've been tracking him for months. Russian mob connections.

SARAH
Then why haven't we brought him in?

MIKE
No concrete evidence. He's clean on paper. Legitimate import business.

Sarah's phone RINGS. She answers quickly.

SARAH
Chen... What? When did this happen?... We'll be right there.

She hangs up, grabs her jacket and gun.

SARAH (CONT'D)
Another body. Same MO as Kozlov.

EXT. WAREHOUSE DISTRICT - DAY

Police cars line the street. Crime scene tape flutters in the wind. Sarah and Mike approach the scene where FORENSICS TECH JENNY WONG (30s) is processing evidence.

JENNY
Victim's name is Alex Volkov. Russian national, single gunshot to the head.

SARAH
Any connection to Viktor Petrov?

JENNY
(holding up a business card)
This was in his wallet. "Petrov Import/Export."

Mike and Sarah exchange meaningful looks.

MIKE
Now we have our connection.

Sarah notices something glinting in a nearby dumpster.

SARAH
Jenny, check that dumpster.

Jenny pulls out a silver watch with Cyrillic inscriptions.

JENNY
Russian writing. Expensive. This wasn't a robbery.

INT. VIKTOR PETROV'S OFFICE - DAY

An elegant office overlooking the harbor. Floor-to-ceiling windows reveal cargo ships in the distance. VIKTOR PETROV (50s), silver-haired and immaculately dressed, speaks in Russian on his phone.

PETROV
(in Russian, subtitled)
The detective is getting too close. Take care of it.

He hangs up as his SECRETARY (20s) enters.

SECRETARY
Mr. Petrov? There are two police officers here to see you.

PETROV
(smiling coldly)
Send them in.

Sarah and Mike enter. Petrov stands, extending his hand in a gesture of false warmth.

PETROV (CONT'D)
Detectives. How may I assist you?

SARAH
We're investigating the death of Alex Volkov.

PETROV
Tragic. Alex was a valued employee. Very dedicated.

MIKE
What kind of work did he do for you?

PETROV
Import documentation. Customs paperwork. Nothing glamorous.

Sarah notices a framed photo on Petrov's desk - him with several tough-looking men.

SARAH
Interesting photo. Business associates?

PETROV
(defensive)
From Moscow. We occasionally do business together.

MIKE
We may have more questions later, Mr. Petrov.

PETROV
Of course. I'm always available to help New York's finest.

As they leave, Petrov's smile fades.

EXT. PETROV'S BUILDING - DAY

Sarah and Mike walk to their unmarked car.

SARAH
He's lying about something. Did you see how he reacted to the photo question?

MIKE
Yeah, but what can we prove? We need more than instinct.

SARAH
I want surveillance on him. 24/7.

MIKE
That'll require a warrant. And probable cause.

SARAH
Then let's find some.

INT. SARAH'S APARTMENT - NIGHT

A modest one-bedroom apartment. Sarah sits at her kitchen table, case files spread out, Chinese takeout containers scattered about. Her phone rings.

SARAH
Chen.

DISTORTED VOICE
Stop investigating Viktor Petrov. This is your only warning.

SARAH
Who is this? How did you get this number?

The line goes dead. Sarah looks out her window and sees a black sedan parked across the street.

SARAH (CONT'D)
(to herself)
Now it's personal.

She calls Mike.

SARAH (CONT'D)
Mike, I need you to come over. Now. And bring your gun.

EXT. SARAH'S APARTMENT BUILDING - NIGHT

Mike arrives to find Sarah waiting in the lobby, clearly shaken.

MIKE
What happened?

SARAH
Threatening phone call. There's a car outside that's been there for an hour.

MIKE
(looking out the window)
I don't see any car.

SARAH
They must have moved when you arrived.

MIKE
Sarah, maybe you should consider asking for protection.

SARAH
I'm not backing down from this case, Mike.

INT. UNDERGROUND PARKING GARAGE - NIGHT

Sarah and Mike walk to their cars. The garage is dimly lit, full of shadows.

MIKE
I'll follow you home tomorrow. Just to be safe.

SARAH
Thanks, partner.

As Sarah reaches her car, she notices something tucked under her windshield wiper - a photo of her entering the police station.

SARAH (CONT'D)
Mike... look at this.

Mike examines the photo.

MIKE
This was taken yesterday. They're watching you.

SARAH
We need to end this. Tomorrow, we're going after Petrov.

MIKE
With what evidence?

SARAH
We'll find it. We have to.

A car engine starts somewhere in the garage. They look around nervously.

MIKE
Let's get out of here.

They quickly get in their cars and leave.

INT. POLICE STATION - CAPTAIN'S OFFICE - DAY

CAPTAIN REEVES (50s), a no-nonsense veteran cop, sits behind his desk. Sarah and Mike stand before him.

CAPTAIN REEVES
You want surveillance on Viktor Petrov based on a business card and a photograph?

SARAH
Captain, there's a pattern here. Two Russian nationals, both connected to Petrov, both murdered.

CAPTAIN REEVES
Correlation isn't causation, Detective Chen.

MIKE
What about the threatening phone call?

CAPTAIN REEVES
Could be anyone. You've made enemies in this job.

SARAH
Captain, with respect, my instincts have been right before.

CAPTAIN REEVES
Your instincts don't hold up in court. Get me real evidence, then we'll talk.

Sarah storms out. Mike follows.

EXT. POLICE STATION - DAY

Sarah lights a cigarette, frustrated.

MIKE
He's not wrong, Sarah. We need more.

SARAH
Then let's get more. Tonight, we're going to stake out Petrov's office.

MIKE
That's off the books. If we get caught...

SARAH
Then we better not get caught.

EXT. PETROV'S BUILDING - NIGHT

Sarah and Mike sit in their car across the street from Petrov's office building. Lights are on in his office.

MIKE
Been here three hours. Nothing.

SARAH
Wait. Look.

A black limousine pulls up. Three men in expensive suits get out and enter the building.

SARAH (CONT'D)
Run those plates.

Mike calls it in.

MIKE
(after a pause)
Registered to a shell company. But the driver has a record - Anton Volkov.

SARAH
Volkov... like Alex Volkov?

MIKE
Could be related. Let's find out.

INT. PETROV'S OFFICE - NIGHT

Petrov meets with the three men: DIMITRI (40s), ANTON (30s), and BORIS (35s). They speak in Russian.

DIMITRI
(in Russian, subtitled)
The detective is asking too many questions.

PETROV
(in Russian, subtitled)
I told you to handle it.

ANTON
(in Russian, subtitled)
She's under police protection now. It's more complicated.

PETROV
(in Russian, subtitled)
Then make it look like an accident.

They shake hands. The meeting ends.

EXT. PETROV'S BUILDING - NIGHT

Sarah and Mike watch as the three men leave the building.

SARAH
Follow them. I'll stay here.

MIKE
Sarah, that's not safe.

SARAH
Just go. I'll be fine.

Mike reluctantly follows the limousine. Sarah remains, watching Petrov's office.

INT. PETROV'S OFFICE - NIGHT

Petrov makes a phone call.

PETROV
(in English)
It's done. The detective won't be a problem much longer.

He hangs up and looks out the window - directly at Sarah's car.

PETROV (CONT'D)
(smiling)
Detective Chen. So predictable.

EXT. PETROV'S BUILDING - NIGHT

Sarah sees Petrov looking at her through the window. Their eyes meet. She starts her car engine.

SARAH
(to herself)
Time to go.

As she pulls away, she doesn't notice another car beginning to follow her.

TO BE CONTINUED...

FADE OUT.
"""

def test_large_screenplay_detection():
    """Test scene detection with large screenplay"""
    print("🎬 Testing Large Screenplay Scene Detection")
    print("=" * 50)
    
    # Test scene detection
    scene_count = detect_optimal_scene_count(LARGE_SCREENPLAY)
    
    print(f"Screenplay length: {len(LARGE_SCREENPLAY)} characters")
    print(f"Word count: {len(LARGE_SCREENPLAY.split())} words") 
    print(f"Detected scene count: {scene_count}")
    
    # Count actual scene headers
    lines = LARGE_SCREENPLAY.split('\n')
    scene_headers = 0
    for line in lines:
        if line.strip().upper().startswith(('INT.', 'EXT.')):
            scene_headers += 1
            print(f"  Scene header: {line.strip()}")
    
    print(f"Actual scene headers found: {scene_headers}")
    
    # Estimate pages
    pages = len(LARGE_SCREENPLAY.split('\n')) // 25
    print(f"Estimated pages: {pages}")
    
    return scene_count

if __name__ == "__main__":
    test_large_screenplay_detection()