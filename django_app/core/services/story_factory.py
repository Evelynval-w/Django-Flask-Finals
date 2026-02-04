"""
Factory Pattern - StoryFactory

Why Factory?
- Encapsulates complex object creation logic
- Validates data before sending to API
- Ensures consistent object structure
- Easy to extend for new content types
- Centralizes business rules
"""
from django.core.exceptions import ValidationError


class StoryFactory:
    """
    Factory for creating story-related objects.
    
    Usage:
        story_data = StoryFactory.create_story("My Title", "Description", user.id)
        page_data = StoryFactory.create_page(story_id, "Page text", is_ending=True)
    """
    
    @staticmethod
    def create_story(title, description, author_id, illustration_url=None):
        """
        Create a properly structured story object.
        
        Args:
            title: Story title (min 3 characters)
            description: Story description
            author_id: ID of the author user
            illustration_url: Optional cover image URL
            
        Returns:
            dict: Validated story data ready for API
            
        Raises:
            ValidationError: If validation fails
        """
        # Validation
        if not title or len(title.strip()) < 3:
            raise ValidationError("Title must be at least 3 characters")
        
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")
        
        return {
            'title': title.strip(),
            'description': (description or '').strip(),
            'author_id': author_id,
            'status': 'draft',
            'illustration_url': illustration_url
        }
    
    @staticmethod
    def create_page(story_id, text, is_ending=False, ending_label=None, illustration_url=None):
        """
        Create a properly structured page object.
        
        Args:
            story_id: ID of the parent story
            text: Page content
            is_ending: Whether this is an ending page
            ending_label: Label for the ending (required if is_ending)
            illustration_url: Optional illustration URL
            
        Returns:
            dict: Validated page data ready for API
        """
        if not text or len(text.strip()) < 10:
            raise ValidationError("Page text must be at least 10 characters")
        
        # Auto-set ending label if ending but no label provided
        if is_ending and not ending_label:
            ending_label = "The End"
        
        return {
            'story_id': story_id,
            'text': text.strip(),
            'is_ending': is_ending,
            'ending_label': ending_label,
            'illustration_url': illustration_url
        }
    
    @staticmethod
    def create_choice(page_id, text, next_page_id=None, dice_required=False, min_roll=None):
        """
        Create a properly structured choice object.
        
        Args:
            page_id: ID of the parent page
            text: Choice text shown to player
            next_page_id: ID of the page this choice leads to
            dice_required: Whether a dice roll is needed
            min_roll: Minimum roll required (1-6)
            
        Returns:
            dict: Validated choice data ready for API
        """
        if not text or len(text.strip()) < 2:
            raise ValidationError("Choice text must be at least 2 characters")
        
        if len(text) > 500:
            raise ValidationError("Choice text cannot exceed 500 characters")
        
        choice = {
            'page_id': page_id,
            'text': text.strip(),
            'next_page_id': next_page_id
        }
        
        if dice_required:
            choice['dice_required'] = True
            choice['min_roll'] = min_roll if min_roll and 1 <= min_roll <= 6 else 4
        
        return choice
    
    @staticmethod
    def create_ending_page(story_id, text, ending_label, illustration_url=None):
        """
        Convenience method for creating an ending page.
        """
        return StoryFactory.create_page(
            story_id=story_id,
            text=text,
            is_ending=True,
            ending_label=ending_label,
            illustration_url=illustration_url
        )
    
    @staticmethod
    def create_dice_choice(page_id, text, next_page_id, min_roll=4):
        """
        Convenience method for creating a dice-based choice.
        """
        return StoryFactory.create_choice(
            page_id=page_id,
            text=text,
            next_page_id=next_page_id,
            dice_required=True,
            min_roll=min_roll
        )
