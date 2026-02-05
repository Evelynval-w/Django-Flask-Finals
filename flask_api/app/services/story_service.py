"""
Story Service - Business logic layer for story operations.
Separates business logic from routes for cleaner code and easier testing.
"""
from app.extensions import db
from app.models import Story, Page, Choice, StoryStatus


class StoryService:
    """Service class for story-related operations"""
    
    @staticmethod
    def get_all_stories(status=None):
        """
        Get all stories, optionally filtered by status.
        
        Args:
            status: Optional status filter ('draft', 'published', 'suspended')
            
        Returns:
            List of Story objects
        """
        query = Story.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Story.created_at.desc()).all()
    
    @staticmethod
    def get_story_by_id(story_id):
        """
        Get a single story by ID.
        
        Args:
            story_id: The story's ID
            
        Returns:
            Story object or None
        """
        return Story.query.get(story_id)
    
    @staticmethod
    def create_story(title, description='', author_id=0, illustration_url=None):
        """
        Create a new story.
        
        Args:
            title: Story title (required)
            description: Story description
            author_id: ID of the author
            illustration_url: Optional cover image URL
            
        Returns:
            Created Story object
        """
        story = Story(
            title=title,
            description=description,
            author_id=author_id,
            status=StoryStatus.DRAFT.value,
            illustration_url=illustration_url
        )
        db.session.add(story)
        db.session.commit()
        return story
    
    @staticmethod
    def update_story(story_id, data):
        """
        Update an existing story.
        
        Args:
            story_id: The story's ID
            data: Dictionary of fields to update
            
        Returns:
            Updated Story object or None if not found
        """
        story = Story.query.get(story_id)
        if not story:
            return None
        
        if 'title' in data:
            story.title = data['title']
        if 'description' in data:
            story.description = data['description']
        if 'status' in data:
            story.status = data['status']
        if 'start_page_id' in data:
            story.start_page_id = data['start_page_id']
        if 'illustration_url' in data:
            story.illustration_url = data['illustration_url']
        
        db.session.commit()
        return story
    
    @staticmethod
    def delete_story(story_id):
        """
        Delete a story and all its pages/choices (cascade).
        
        Args:
            story_id: The story's ID
            
        Returns:
            True if deleted, False if not found
        """
        story = Story.query.get(story_id)
        if not story:
            return False
        
        db.session.delete(story)
        db.session.commit()
        return True
    
    @staticmethod
    def publish_story(story_id):
        """
        Publish a story (change status from draft to published).
        
        Args:
            story_id: The story's ID
            
        Returns:
            Updated Story object or None
        """
        return StoryService.update_story(story_id, {'status': StoryStatus.PUBLISHED.value})
    
    @staticmethod
    def suspend_story(story_id):
        """
        Suspend a story (admin action).
        
        Args:
            story_id: The story's ID
            
        Returns:
            Updated Story object or None
        """
        return StoryService.update_story(story_id, {'status': StoryStatus.SUSPENDED.value})
    
    @staticmethod
    def get_story_tree(story_id):
        """
        Get the story structure for visualization.
        
        Args:
            story_id: The story's ID
            
        Returns:
            Dictionary with nodes and edges for graph visualization
        """
        story = Story.query.get(story_id)
        if not story:
            return None
        
        pages = Page.query.filter_by(story_id=story_id).all()
        
        nodes = []
        edges = []
        
        for page in pages:
            nodes.append({
                'id': page.id,
                'label': f'Page {page.id}',
                'is_start': page.id == story.start_page_id,
                'is_ending': page.is_ending,
                'ending_label': page.ending_label
            })
            
            for choice in page.choices:
                if choice.next_page_id:
                    edges.append({
                        'source': page.id,
                        'target': choice.next_page_id,
                        'label': choice.text[:30] + '...' if len(choice.text) > 30 else choice.text
                    })
        
        return {'nodes': nodes, 'edges': edges}
    
    @staticmethod
    def validate_story_for_publish(story_id):
        """
        Validate that a story is ready for publication.
        
        Args:
            story_id: The story's ID
            
        Returns:
            Tuple of (is_valid, list of errors)
        """
        story = Story.query.get(story_id)
        if not story:
            return False, ['Story not found']
        
        errors = []
        
        # Check for pages
        pages = Page.query.filter_by(story_id=story_id).all()
        if len(pages) < 2:
            errors.append('Story must have at least 2 pages')
        
        # Check for start page
        if not story.start_page_id:
            errors.append('Story must have a start page set')
        
        # Check for at least one ending
        endings = [p for p in pages if p.is_ending]
        if not endings:
            errors.append('Story must have at least one ending page')
        
        # Check that all non-ending pages have choices
        for page in pages:
            if not page.is_ending and len(page.choices) == 0:
                errors.append(f'Page {page.id} has no choices and is not an ending')
        
        return len(errors) == 0, errors


class PageService:
    """Service class for page-related operations"""
    
    @staticmethod
    def get_page_by_id(page_id):
        """Get a single page by ID"""
        return Page.query.get(page_id)
    
    @staticmethod
    def create_page(story_id, text, is_ending=False, ending_label=None, illustration_url=None):
        """
        Create a new page in a story.
        
        Args:
            story_id: The parent story's ID
            text: Page content
            is_ending: Whether this is an ending page
            ending_label: Label for the ending
            illustration_url: Optional illustration URL
            
        Returns:
            Created Page object
        """
        page = Page(
            story_id=story_id,
            text=text,
            is_ending=is_ending,
            ending_label=ending_label,
            illustration_url=illustration_url
        )
        db.session.add(page)
        db.session.commit()
        
        # If this is the first page, set it as start page
        story = Story.query.get(story_id)
        if story and story.pages.count() == 1:
            story.start_page_id = page.id
            db.session.commit()
        
        return page
    
    @staticmethod
    def update_page(page_id, data):
        """Update an existing page"""
        page = Page.query.get(page_id)
        if not page:
            return None
        
        if 'text' in data:
            page.text = data['text']
        if 'is_ending' in data:
            page.is_ending = data['is_ending']
        if 'ending_label' in data:
            page.ending_label = data['ending_label']
        if 'illustration_url' in data:
            page.illustration_url = data['illustration_url']
        
        db.session.commit()
        return page
    
    @staticmethod
    def delete_page(page_id):
        """Delete a page"""
        page = Page.query.get(page_id)
        if not page:
            return False
        
        db.session.delete(page)
        db.session.commit()
        return True
    
    @staticmethod
    def get_start_page(story_id):
        """Get the starting page of a story"""
        story = Story.query.get(story_id)
        if not story:
            return None
        
        if story.start_page_id:
            return Page.query.get(story.start_page_id)
        
        # Fallback to first page
        return Page.query.filter_by(story_id=story_id).first()


class ChoiceService:
    """Service class for choice-related operations"""
    
    @staticmethod
    def get_choice_by_id(choice_id):
        """Get a single choice by ID"""
        return Choice.query.get(choice_id)
    
    @staticmethod
    def create_choice(page_id, text, next_page_id=None, dice_required=False, min_roll=1):
        """
        Create a new choice on a page.
        
        Args:
            page_id: The parent page's ID
            text: Choice text
            next_page_id: ID of the target page
            dice_required: Whether a dice roll is needed
            min_roll: Minimum roll required (1-6)
            
        Returns:
            Created Choice object
        """
        choice = Choice(
            page_id=page_id,
            text=text,
            next_page_id=next_page_id,
            dice_required=dice_required,
            min_roll=min_roll if dice_required else 1
        )
        db.session.add(choice)
        db.session.commit()
        return choice
    
    @staticmethod
    def update_choice(choice_id, data):
        """Update an existing choice"""
        choice = Choice.query.get(choice_id)
        if not choice:
            return None
        
        if 'text' in data:
            choice.text = data['text']
        if 'next_page_id' in data:
            choice.next_page_id = data['next_page_id']
        if 'dice_required' in data:
            choice.dice_required = data['dice_required']
        if 'min_roll' in data:
            choice.min_roll = data['min_roll']
        
        db.session.commit()
        return choice
    
    @staticmethod
    def delete_choice(choice_id):
        """Delete a choice"""
        choice = Choice.query.get(choice_id)
        if not choice:
            return False
        
        db.session.delete(choice)
        db.session.commit()
        return True
