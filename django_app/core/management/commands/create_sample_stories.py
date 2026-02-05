from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = 'Create sample stories with pages and choices'

    def handle(self, *args, **options):
        base_url = 'http://localhost:5000'
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': 'your-super-secret-api-key-change-in-production'
        }
        
        stories_data = [
            # Author 1 (author1) stories
            {
                "title": "The Space Station",
                "description": "You wake up on an abandoned space station. Alarms are blaring.",
                "author_id": 2,
                "illustration_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800",
                "pages": [
                    {
                        "text": "Red lights flash as you open your eyes. You're floating in zero gravity. The alarm screams: 'HULL BREACH DETECTED'. You see two doors - one leads to the bridge, one to the escape pods.",
                        "is_start": True,
                        "illustration_url": "https://images.unsplash.com/photo-1454789548928-9efd52dc4031?w=800"
                    },
                    {
                        "text": "You rush to the escape pods. One pod remains. You climb in and launch into space. Through the window, you watch the station explode. You're safe... for now.",
                        "is_ending": True,
                        "ending_label": "Escaped",
                        "illustration_url": "https://images.unsplash.com/photo-1517976487492-5750f3195933?w=800"
                    },
                    {
                        "text": "You float to the bridge. The captain lies unconscious. The controls show the breach can be sealed manually. Do you try to save the station?",
                        "illustration_url": "https://images.unsplash.com/photo-1581822261290-991b38693d1b?w=800"
                    },
                    {
                        "text": "You seal the breach and save the station! The captain wakes and thanks you. You're a hero.",
                        "is_ending": True,
                        "ending_label": "Hero",
                        "illustration_url": "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=800"
                    },
                ],
                "choices": [
                    {"from_page": 0, "to_page": 1, "text": "Head to the escape pods"},
                    {"from_page": 0, "to_page": 2, "text": "Go to the bridge"},
                    {"from_page": 2, "to_page": 3, "text": "Seal the breach"},
                    {"from_page": 2, "to_page": 1, "text": "Abandon ship"},
                ]
            },
            {
                "title": "The Haunted Mansion",
                "description": "You inherit an old mansion from a distant relative. Strange things happen at night.",
                "author_id": 2,
                "illustration_url": "https://images.unsplash.com/photo-1520350094754-f0fdcac35c1c?w=800",
                "pages": [
                    {
                        "text": "The mansion looms before you, dark and foreboding. The lawyer hands you the rusty key. 'Your uncle left everything to you,' he says nervously. You step inside...",
                        "is_start": True,
                        "illustration_url": "https://images.unsplash.com/photo-1464618663641-bbdd760ae84a?w=800"
                    },
                    {
                        "text": "You explore the library and find your uncle's journal. It speaks of a friendly ghost who protects the house. You call out and a warm presence surrounds you. You've made a friend.",
                        "is_ending": True,
                        "ending_label": "Friendly Ghost",
                        "illustration_url": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800"
                    },
                    {
                        "text": "You hear footsteps upstairs. Do you investigate or hide?",
                        "illustration_url": "https://images.unsplash.com/photo-1445546636032-e578a075a0ac?w=800"
                    },
                    {
                        "text": "You hide in a closet. The footsteps pass. When you emerge, you find a note: 'LEAVE NOW'. You run and never return.",
                        "is_ending": True,
                        "ending_label": "Fled",
                        "illustration_url": "https://images.unsplash.com/photo-1509248961229-6523e1eb9f98?w=800"
                    },
                ],
                "choices": [
                    {"from_page": 0, "to_page": 1, "text": "Explore the library"},
                    {"from_page": 0, "to_page": 2, "text": "Go upstairs"},
                    {"from_page": 2, "to_page": 3, "text": "Hide"},
                    {"from_page": 2, "to_page": 1, "text": "Call out 'Hello?'"},
                ]
            },
            {
                "title": "Dragon Quest",
                "description": "The village elder asks you to slay the dragon terrorizing the kingdom.",
                "author_id": 2,
                "illustration_url": "https://images.unsplash.com/photo-1514539079130-25950c84af65?w=800",
                "pages": [
                    {
                        "text": "The elder places a worn sword in your hands. 'The dragon lives in the mountain cave. Many have tried, none have returned.' You set off at dawn.",
                        "is_start": True,
                        "illustration_url": "https://images.unsplash.com/photo-1560419015-7c427e8ae5ba?w=800"
                    },
                    {
                        "text": "You befriend the dragon! It was only attacking because villagers stole its eggs. You return the eggs and broker peace.",
                        "is_ending": True,
                        "ending_label": "Peacemaker",
                        "illustration_url": "https://images.unsplash.com/photo-1577493340887-b7bfff550145?w=800"
                    },
                    {
                        "text": "Inside the cave, you find the dragon sleeping on a pile of gold. Its eye opens. 'A visitor? How... interesting.'",
                        "illustration_url": "https://images.unsplash.com/photo-1560419015-7c427e8ae5ba?w=800"
                    },
                    {
                        "text": "You charge and slay the dragon in epic combat! The kingdom celebrates you as a hero.",
                        "is_ending": True,
                        "ending_label": "Dragon Slayer",
                        "illustration_url": "https://images.unsplash.com/photo-1531065208531-4036c0dba3ca?w=800"
                    },
                ],
                "choices": [
                    {"from_page": 0, "to_page": 2, "text": "Enter the cave boldly"},
                    {"from_page": 0, "to_page": 1, "text": "Search for dragon eggs first"},
                    {"from_page": 2, "to_page": 3, "text": "Attack the dragon!"},
                    {"from_page": 2, "to_page": 1, "text": "Try to talk to the dragon"},
                ]
            },
            # Author 2 (author2) stories
            {
                "title": "Cyber Heist",
                "description": "In 2087, you're the best hacker in Neo Tokyo. Tonight's job: break into MegaCorp.",
                "author_id": 3,
                "illustration_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
                "pages": [
                    {
                        "text": "You plug into the MegaCorp network. Firewalls everywhere. You spot two entry points: the CEO's personal server or the security mainframe.",
                        "is_start": True,
                        "illustration_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800"
                    },
                    {
                        "text": "You crack the CEO's server and find evidence of illegal experiments. You leak it all. MegaCorp falls. You're a legend.",
                        "is_ending": True,
                        "ending_label": "Whistleblower",
                        "illustration_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800"
                    },
                    {
                        "text": "You're in the security mainframe. Alarms trigger! You have seconds to decide: fight the AI or jack out?",
                        "illustration_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800"
                    },
                    {
                        "text": "You jack out just in time. Your brain is safe, but the job failed. There's always next time...",
                        "is_ending": True,
                        "ending_label": "Escaped",
                        "illustration_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800"
                    },
                ],
                "choices": [
                    {"from_page": 0, "to_page": 1, "text": "Hack the CEO's server"},
                    {"from_page": 0, "to_page": 2, "text": "Attack the security mainframe"},
                    {"from_page": 2, "to_page": 3, "text": "Jack out now!"},
                    {"from_page": 2, "to_page": 1, "text": "Fight the AI"},
                ]
            },
            {
                "title": "Lost in the Jungle",
                "description": "Your plane crashed in the Amazon. Survival is your only goal.",
                "author_id": 3,
                "illustration_url": "https://images.unsplash.com/photo-1440342359743-84fcb8c21f21?w=800",
                "pages": [
                    {
                        "text": "You wake among the wreckage. The jungle is alive with sounds. You see smoke in the distance and a river nearby.",
                        "is_start": True,
                        "illustration_url": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800"
                    },
                    {
                        "text": "You follow the river for days until you reach a village. The locals help you contact rescue. You're saved!",
                        "is_ending": True,
                        "ending_label": "Rescued",
                        "illustration_url": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800"
                    },
                    {
                        "text": "You head toward the smoke and find other survivors! Together you build a shelter.",
                        "illustration_url": "https://images.unsplash.com/photo-1509660933844-6910e12765a0?w=800"
                    },
                    {
                        "text": "Weeks later, a helicopter spots your signal fire. You and the other survivors are rescued together!",
                        "is_ending": True,
                        "ending_label": "Group Rescue",
                        "illustration_url": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?w=800"
                    },
                ],
                "choices": [
                    {"from_page": 0, "to_page": 1, "text": "Follow the river"},
                    {"from_page": 0, "to_page": 2, "text": "Head toward the smoke"},
                    {"from_page": 2, "to_page": 3, "text": "Build a signal fire"},
                    {"from_page": 2, "to_page": 1, "text": "Search for the river"},
                ]
            },
            {
                "title": "The Time Machine",
                "description": "You discover a time machine in your grandfather's attic. Where will you go?",
                "author_id": 3,
                "illustration_url": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
                "pages": [
                    {
                        "text": "The machine hums to life. The dial shows two options: Ancient Rome or Year 3000. Your finger hovers over the buttons...",
                        "is_start": True,
                        "illustration_url": "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?w=800"
                    },
                    {
                        "text": "You arrive in Rome during a gladiator fight! The crowd cheers. You become a legend of the arena.",
                        "is_ending": True,
                        "ending_label": "Gladiator",
                        "illustration_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800"
                    },
                    {
                        "text": "Year 3000: Flying cars, robot servants, and... humans living on Mars! A guide offers you a tour.",
                        "illustration_url": "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800"
                    },
                    {
                        "text": "You decide to stay in the future. With your 'ancient' knowledge, you become a famous historian!",
                        "is_ending": True,
                        "ending_label": "Future Historian",
                        "illustration_url": "https://images.unsplash.com/photo-1581822261290-991b38693d1b?w=800"
                    },
                ],
                "choices": [
                    {"from_page": 0, "to_page": 1, "text": "Travel to Ancient Rome"},
                    {"from_page": 0, "to_page": 2, "text": "Travel to Year 3000"},
                    {"from_page": 2, "to_page": 3, "text": "Stay in the future"},
                    {"from_page": 2, "to_page": 1, "text": "Go back further in time"},
                ]
            },
        ]

        for story_data in stories_data:
            self.stdout.write(f"\nCreating: {story_data['title']}")
            
            # Create story
            response = requests.post(
                f'{base_url}/stories',
                headers=headers,
                json={
                    'title': story_data['title'],
                    'description': story_data['description'],
                    'author_id': story_data['author_id'],
                    'illustration_url': story_data['illustration_url']
                }
            )
            
            if response.status_code != 201:
                self.stdout.write(self.style.ERROR(f"  Failed to create story: {response.text}"))
                continue
                
            story = response.json()
            story_id = story['id']
            self.stdout.write(f"  Story ID: {story_id}")
            
            # Create pages
            page_ids = []
            for i, page_data in enumerate(story_data['pages']):
                page_response = requests.post(
                    f'{base_url}/stories/{story_id}/pages',
                    headers=headers,
                    json={
                        'text': page_data['text'],
                        'is_ending': page_data.get('is_ending', False),
                        'ending_label': page_data.get('ending_label', ''),
                        'illustration_url': page_data.get('illustration_url', '')
                    }
                )
                
                if page_response.status_code == 201:
                    page = page_response.json()
                    page_ids.append(page['id'])
                    self.stdout.write(f"  Page {i+1}: ID {page['id']}")
                else:
                    self.stdout.write(self.style.ERROR(f"  Failed to create page: {page_response.text}"))
            
            # Create choices
            for choice_data in story_data['choices']:
                from_page_id = page_ids[choice_data['from_page']]
                to_page_id = page_ids[choice_data['to_page']]
                
                choice_response = requests.post(
                    f'{base_url}/pages/{from_page_id}/choices',
                    headers=headers,
                    json={
                        'text': choice_data['text'],
                        'next_page_id': to_page_id
                    }
                )
                
                if choice_response.status_code == 201:
                    self.stdout.write(f"  Choice: {choice_data['text'][:30]}...")
                else:
                    self.stdout.write(self.style.ERROR(f"  Failed: {choice_response.text}"))
            
            # Publish story
            requests.put(
                f'{base_url}/stories/{story_id}',
                headers=headers,
                json={'status': 'published'}
            )
            self.stdout.write(self.style.SUCCESS(f"  Published!"))

        self.stdout.write(self.style.SUCCESS('\n\nDone! Created 6 sample stories (3 for author1, 3 for author2).'))