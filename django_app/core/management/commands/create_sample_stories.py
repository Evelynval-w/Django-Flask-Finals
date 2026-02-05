from django.core.management.base import BaseCommand
from core.services.api_client import get_api_client


class Command(BaseCommand):
    help = 'Create sample stories with pages and choices'

    def handle(self, *args, **options):
        client = get_api_client()
        
        stories_data = [
            {
                "title": "The Space Station",
                "description": "You wake up on an abandoned space station. Alarms are blaring.",
                "author_id": 2,
                "illustration_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800",
                "pages": [
                    {"text": "Red lights flash as you open your eyes. You're floating in zero gravity. The alarm screams: 'HULL BREACH DETECTED'. You see two doors - one leads to the bridge, one to the escape pods.", "is_start": True},
                    {"text": "You rush to the escape pods. One pod remains. You climb in and launch into space. Through the window, you watch the station explode. You're safe... for now.", "is_ending": True, "ending_label": "Escaped"},
                    {"text": "You float to the bridge. The captain lies unconscious. The controls show the breach can be sealed manually. Do you try to save the station?", "is_start": False},
                    {"text": "You seal the breach and save the station! The captain wakes and thanks you. You're a hero.", "is_ending": True, "ending_label": "Hero"},
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
                    {"text": "The mansion looms before you, dark and foreboding. The lawyer hands you the rusty key. 'Your uncle left everything to you,' he says nervously. You step inside...", "is_start": True},
                    {"text": "You explore the library and find your uncle's journal. It speaks of a friendly ghost who protects the house. You call out and a warm presence surrounds you. You've made a friend.", "is_ending": True, "ending_label": "Friendly Ghost"},
                    {"text": "You hear footsteps upstairs. Do you investigate or hide?", "is_start": False},
                    {"text": "You hide in a closet. The footsteps pass. When you emerge, you find a note: 'LEAVE NOW'. You run and never return.", "is_ending": True, "ending_label": "Fled"},
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
                    {"text": "The elder places a worn sword in your hands. 'The dragon lives in the mountain cave. Many have tried, none have returned.' You set off at dawn.", "is_start": True},
                    {"text": "You befriend the dragon! It was only attacking because villagers stole its eggs. You return the eggs and broker peace.", "is_ending": True, "ending_label": "Peacemaker"},
                    {"text": "Inside the cave, you find the dragon sleeping on a pile of gold. Its eye opens. 'A visitor? How... interesting.'", "is_start": False},
                    {"text": "You charge and slay the dragon in epic combat! The kingdom celebrates you as a hero.", "is_ending": True, "ending_label": "Dragon Slayer"},
                ],
                "choices": [
                    {"from_page": 0, "to_page": 2, "text": "Enter the cave boldly"},
                    {"from_page": 0, "to_page": 1, "text": "Search for dragon eggs first"},
                    {"from_page": 2, "to_page": 3, "text": "Attack the dragon!"},
                    {"from_page": 2, "to_page": 1, "text": "Try to talk to the dragon"},
                ]
            },
        ]

        for story_data in stories_data:
            self.stdout.write(f"Creating: {story_data['title']}")
            
            # Create story
            story = client.create_story(
                title=story_data['title'],
                description=story_data['description'],
                author_id=story_data['author_id']
            )
            
            if not story:
                self.stdout.write(self.style.ERROR(f"  Failed to create story"))
                continue
                
            story_id = story['id']
            self.stdout.write(f"  Story ID: {story_id}")
            
            # Create pages
            page_ids = []
            for i, page_data in enumerate(story_data['pages']):
                page = client.create_page(
                    story_id=story_id,
                    content=page_data['text'],
                    is_start=page_data.get('is_start', False),
                    is_ending=page_data.get('is_ending', False),
                    ending_label=page_data.get('ending_label', '')
                )
                if page:
                    page_ids.append(page['id'])
                    self.stdout.write(f"  Page {i+1}: {page['id']}")
            
            # Create choices
            for choice_data in story_data['choices']:
                from_page_id = page_ids[choice_data['from_page']]
                to_page_id = page_ids[choice_data['to_page']]
                choice = client.create_choice(
                    page_id=from_page_id,
                    text=choice_data['text'],
                    next_page_id=to_page_id
                )
                if choice:
                    self.stdout.write(f"  Choice: {choice_data['text'][:30]}...")
            
            # Publish story
            client.update_story(story_id, {'status': 'published'})
            self.stdout.write(self.style.SUCCESS(f"  Published!"))

        self.stdout.write(self.style.SUCCESS('\nDone! Created 3 sample stories.'))