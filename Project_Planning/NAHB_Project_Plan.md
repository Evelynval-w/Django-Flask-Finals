# NAHB - Not Another Hero's Book
## Complete Project Plan & Architecture Documentation

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Analysis Phase](#2-analysis-phase)
3. [Design Phase](#3-design-phase)
4. [Tech Stack Justification](#4-tech-stack-justification)
5. [Design Patterns Justification](#5-design-patterns-justification)
6. [File Structure](#6-file-structure)
7. [Development Timeline](#7-development-timeline)
8. [Implementation Details](#8-implementation-details)

---

## 1. Project Overview

### 1.1 Problem Statement
Create a web application inspired by "Choose Your Own Adventure" books where:
- **Authors** create interactive stories with branching narratives
- **Readers** play through stories by making choices
- The system tracks gameplay statistics and provides save functionality

### 1.2 Target Grade:
This implementation targets the highest standard with full authentication, ratings/comments/reports, story tree visualization, random events (dice rolls), and illustrations support.

### 1.3 Deadline
**February 8, 2026 at 11:55 PM**

---

## 2. Analysis Phase

### 2.1 Requirements Analysis

#### Functional Requirements by Level

| Category | Requirement | Level |
|----------|-------------|-------|
| **Story Management** | Create/Edit/Delete stories | 10 |
| **Story Management** | Draft vs Published status | 13 |
| **Story Management** | Suspend stories (admin) | 16 |
| **Page Management** | Create pages with text | 10 |
| **Page Management** | Mark pages as endings | 10 |
| **Page Management** | Named ending labels | 13 |
| **Choice Management** | Create choices linking pages | 10 |
| **Choice Management** | Random events (dice rolls) | 18 |
| **Gameplay** | Navigate story via choices | 10 |
| **Gameplay** | Record play completions | 10 |
| **Gameplay** | Auto-save progression | 13 |
| **Statistics** | Plays per story | 10 |
| **Statistics** | Ending distribution | 13 |
| **Authentication** | User registration/login | 16 |
| **Permissions** | Role-based access | 16 |
| **Community** | Ratings (1-5 stars) | 18 |
| **Community** | Comments on stories | 18 |
| **Community** | Report inappropriate content | 18 |
| **Visualization** | Story tree graph | 18 |

### 2.2 User Roles Analysis

| Role | Permissions |
|------|-------------|
| **Reader** | Browse stories, play, view history, rate, comment, report |
| **Author** | All Reader + Create/Edit/Delete OWN stories, preview drafts |
| **Admin** | All Author + View ALL stories, suspend any story, manage reports |

---

## 3. Design Phase

### 3.1 System Architecture

The system follows a **two-tier microservices architecture**:

```
CLIENT LAYER (Browser)
        │
        ▼ HTTP/HTML
DJANGO APPLICATION (Game Engine + UI + Auth)
├── Views Layer (Controllers)
├── Template Engine (UI Rendering)
├── Authentication System
├── Session Manager
└── Service Layer (Design Patterns)
    ├── FlaskAPIClient (Singleton)
    ├── StoryFactory (Factory)
    ├── GameMediator (Mediator)
    └── GameStateMemento (Memento)
        │
        ▼ HTTP/JSON REST API
FLASK REST API (Story Storage)
├── Story Endpoints (/stories/*)
├── Page Endpoints (/pages/*)
├── Choice Endpoints (/choices/*)
└── API Key Authentication Middleware
        │
        ▼
DATABASE LAYER
├── Django DB: Users, Plays, Sessions, Ratings, Reports
└── Flask DB: Stories, Pages, Choices
```

### 3.2 Why Two Separate Applications?

| Flask (Content) | Django (User Experience) |
|-----------------|--------------------------|
| Story data is static | User sessions are dynamic |
| Read-heavy workload | Write-heavy for gameplay |
| Can be cached aggressively | Requires real-time updates |
| Simple CRUD operations | Complex business logic |
| Stateless API | Stateful sessions |

**Benefits:**
- Independent scaling
- Technology flexibility
- Clear data ownership
- Easier testing
- Security isolation

---

## 4. Tech Stack Justification

| Component | Technology | Justification |
|-----------|------------|---------------|
| **Backend API** | Flask 3.x | Lightweight, perfect for REST APIs |
| **Web App** | Django 5.x | Full-featured with built-in auth |
| **Database** | SQLite/PostgreSQL | SQLite for dev, PostgreSQL for prod |
| **ORM (Flask)** | SQLAlchemy | Industry standard, migration support |
| **HTTP Client** | Requests | Simple, reliable HTTP library |
| **Frontend** | Bootstrap 5 | Rapid UI development |
| **Visualization** | D3.js | Powerful graph visualization |

---

## 5. Design Patterns Justification

### 5.1 Singleton - FlaskAPIClient

**Problem:** Multiple views need Flask API communication. Creating new connections is inefficient.

**Solution:** Single instance shared across all Django views.

**Benefits:**
- Reuses HTTP connection pool (performance)
- Centralizes API key configuration (security)
- Consistent error handling
- Easy to mock for testing

### 5.2 Factory - StoryFactory

**Problem:** Creating stories involves complex validation. Different story types need different setups.

**Solution:** Factory encapsulates creation logic and ensures valid objects.

**Benefits:**
- Encapsulates validation logic (DRY)
- Consistent object structure
- Easy to add new story types
- Centralized business rules

### 5.3 Mediator - GameMediator

**Problem:** Gameplay involves multiple components (page display, choices, statistics, dice, auto-save) that need to communicate.

**Solution:** Mediator coordinates all components without direct references.

**Benefits:**
- Decouples components
- Single point of control
- Easy to add new features
- Simplifies testing

### 5.4 Memento - GameStateMemento

**Problem:** Players need to save progress. Game state includes current page, path taken, dice results. Exposing internal state violates encapsulation.

**Solution:** Memento captures and restores state without exposing internals.

**Benefits:**
- Preserves encapsulation
- Enables undo/restore
- Serializable for storage
- Path history enables visualization

---

## 6. File Structure

### 6.1 Flask Application

```
flask_api/
├── app/
│   ├── __init__.py              # App factory
│   ├── config.py                # Configuration
│   ├── extensions.py            # SQLAlchemy init
│   ├── models/
│   │   ├── story.py
│   │   ├── page.py
│   │   └── choice.py
│   ├── routes/
│   │   ├── stories.py
│   │   ├── pages.py
│   │   └── choices.py
│   ├── schemas/
│   │   └── *.py
│   ├── services/
│   │   └── story_service.py
│   └── middleware/
│       └── api_key_auth.py
├── migrations/
├── tests/
├── requirements.txt
├── run.py
└── README.md
```

### 6.2 Django Application

```
django_app/
├── nahb/                        # Project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   └── urls.py
├── accounts/                    # User management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/accounts/
├── stories/                     # Story browsing
│   ├── views.py
│   └── templates/stories/
├── author/                      # Author tools
│   ├── views.py
│   ├── forms.py
│   └── templates/author/
├── gameplay/                    # Gameplay tracking
│   ├── models.py
│   ├── views.py
│   └── templates/gameplay/
├── community/                   # Ratings, Comments
│   ├── models.py
│   └── templates/community/
├── moderation/                  # Admin tools
│   └── templates/moderation/
├── core/                        # Shared components
│   └── services/
│       ├── api_client.py        # Singleton
│       ├── story_factory.py     # Factory
│       ├── game_mediator.py     # Mediator
│       └── game_memento.py      # Memento
├── static/
│   ├── css/
│   └── js/
│       ├── story_tree.js        # D3.js visualization
│       └── dice_roller.js
├── templates/
├── tests/
├── manage.py
└── requirements.txt
```

---

## 7. Development Timeline

### Sprint Overview

| Sprint | Days | Focus | Target |
|--------|------|-------|--------|
| Sprint 1 | 1-2 | Setup & MVP | Level 10 |
| Sprint 2 | 3 | Advanced Features | Level 13 |
| Sprint 3 | 4 | Security | Level 16 |
| Sprint 4 | 5-6 | Community & Viz | Level 18 |
| Sprint 5 | 7 | Polish & Deploy | Final |

### Detailed Tasks

#### Sprint 1 (Days 1-2) - Level 10 MVP

**Day 1 Morning:**
- [ ] Initialize Flask project
- [ ] Story/Page/Choice models
- [ ] CRUD endpoints

**Day 1 Afternoon:**
- [ ] Initialize Django project
- [ ] FlaskAPIClient (Singleton)
- [ ] Story list view

**Day 2 Morning:**
- [ ] StoryFactory (Factory)
- [ ] Author dashboard
- [ ] Story/Page forms

**Day 2 Afternoon:**
- [ ] GameMediator (Mediator)
- [ ] Gameplay view
- [ ] Play recording

#### Sprint 2 (Day 3) - Level 13

**Morning:**
- [ ] Search/filter stories
- [ ] Named endings
- [ ] Ending distribution stats

**Afternoon:**
- [ ] GameStateMemento (Memento)
- [ ] Auto-save (session-based)
- [ ] Resume functionality

**Evening:**
- [ ] UI improvements
- [ ] Confirmation dialogs

#### Sprint 3 (Day 4) - Level 16

**Morning:**
- [ ] User registration/login
- [ ] UserProfile with roles
- [ ] Permission decorators

**Afternoon:**
- [ ] Protected author views
- [ ] Story ownership
- [ ] User play history

**Evening:**
- [ ] X-API-KEY middleware
- [ ] Admin story suspension

#### Sprint 4 (Days 5-6) - Level 18

**Day 5:**
- [ ] Rating model & form
- [ ] Comment model & form
- [ ] Report model & admin view

**Day 6:**
- [ ] Illustrations support
- [ ] Dice roll mechanics
- [ ] Story tree visualization (D3.js)
- [ ] Player path visualization

#### Sprint 5 (Day 7) - Polish

- [ ] Unit/integration tests
- [ ] Docker configuration
- [ ] README documentation
- [ ] Screenshots

---

## 8. Implementation Details

### 8.1 Flask Story Model

```python
class StoryStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    SUSPENDED = 'suspended'

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(StoryStatus), default=StoryStatus.DRAFT)
    author_id = db.Column(db.Integer, nullable=False)
    start_page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    illustration_url = db.Column(db.String(500))
```

### 8.2 Django Play Model

```python
class Play(models.Model):
    story_id = models.IntegerField()  # External FK to Flask
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ending_page_id = models.IntegerField()
    path = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 8.3 API Key Middleware (Flask)

```python
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key or api_key != current_app.config['API_KEY']:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated
```

### 8.4 Role Decorator (Django)

```python
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            if request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "Permission denied")
            return redirect('stories:list')
        return wrapped
    return decorator
```

---

## 9. Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | Admin123! |
| Author | author1 | Author123! |
| Reader | reader1 | Reader123! |

---

## 10. API Endpoints Summary

### Read (Public)
- `GET /stories?status=published`
- `GET /stories/<id>`
- `GET /stories/<id>/start`
- `GET /pages/<id>`
- `GET /stories/<id>/tree`

### Write (X-API-KEY Required)
- `POST /stories`
- `PUT /stories/<id>`
- `DELETE /stories/<id>`
- `POST /stories/<id>/pages`
- `POST /pages/<id>/choices`
- `PUT /stories/<id>/suspend`

---

*Document Version: 1.0*
*Last Updated: February 2, 2026*
