# NAHB Project - Notion Task Board

## 📊 Project Dashboard

| Property | Value |
|----------|-------|
| **Project** | NAHB - Not Another Hero's Book |
| **Deadline** | February 8, 2026 @ 11:55 PM |
| **Target Grade** | Level 18/20 |
| **Team Size** | 2 (or solo) |
| **Status** | 🚀 In Progress |

---

## 🏃 Sprint Board

### Sprint 1: MVP Foundation (Days 1-2) - Level 10

| Task | Priority | Status | Assignee | Est. Hours |
|------|----------|--------|----------|------------|
| **Flask Setup** |
| Initialize Flask project structure | 🔴 High | ⬜ To Do | | 1h |
| Configure SQLAlchemy + migrations | 🔴 High | ⬜ To Do | | 1h |
| Create Story model | 🔴 High | ⬜ To Do | | 1h |
| Create Page model | 🔴 High | ⬜ To Do | | 1h |
| Create Choice model | 🔴 High | ⬜ To Do | | 1h |
| Implement GET /stories endpoint | 🔴 High | ⬜ To Do | | 0.5h |
| Implement GET /stories/<id> endpoint | 🔴 High | ⬜ To Do | | 0.5h |
| Implement POST /stories endpoint | 🔴 High | ⬜ To Do | | 0.5h |
| Implement PUT /stories/<id> endpoint | 🔴 High | ⬜ To Do | | 0.5h |
| Implement DELETE /stories/<id> endpoint | 🔴 High | ⬜ To Do | | 0.5h |
| Implement page endpoints | 🔴 High | ⬜ To Do | | 1h |
| Implement choice endpoints | 🔴 High | ⬜ To Do | | 1h |
| **Django Setup** |
| Initialize Django project | 🔴 High | ⬜ To Do | | 1h |
| Configure settings (dev/prod split) | 🟡 Medium | ⬜ To Do | | 0.5h |
| Create base templates (Bootstrap 5) | 🔴 High | ⬜ To Do | | 1h |
| Implement FlaskAPIClient (Singleton) | 🔴 High | ⬜ To Do | | 2h |
| Create story list view | 🔴 High | ⬜ To Do | | 1h |
| Create story detail view | 🔴 High | ⬜ To Do | | 1h |
| **Author Tools** |
| Implement StoryFactory (Factory pattern) | 🔴 High | ⬜ To Do | | 2h |
| Create author dashboard | 🔴 High | ⬜ To Do | | 1h |
| Create story form (create/edit) | 🔴 High | ⬜ To Do | | 1.5h |
| Create page form | 🔴 High | ⬜ To Do | | 1.5h |
| Create choice form | 🔴 High | ⬜ To Do | | 1h |
| **Gameplay** |
| Implement GameMediator (Mediator pattern) | 🔴 High | ⬜ To Do | | 2h |
| Create gameplay view | 🔴 High | ⬜ To Do | | 2h |
| Create Play model in Django | 🔴 High | ⬜ To Do | | 0.5h |
| Record play on ending | 🔴 High | ⬜ To Do | | 1h |
| Basic statistics page | 🔴 High | ⬜ To Do | | 1h |

**Sprint 1 Total:** ~26 hours | **Checkpoint:** Level 10 ✓

---

### Sprint 2: Advanced Features (Day 3) - Level 13

| Task | Priority | Status | Assignee | Est. Hours |
|------|----------|--------|----------|------------|
| **Search & Filter** |
| Add search by title | 🔴 High | ⬜ To Do | | 1h |
| Add tag filtering | 🟡 Medium | ⬜ To Do | | 1h |
| **Named Endings** |
| Add ending_label to Page model (Flask) | 🔴 High | ⬜ To Do | | 0.5h |
| Display ending label on end screen | 🔴 High | ⬜ To Do | | 0.5h |
| **Statistics** |
| Ending distribution percentages | 🔴 High | ⬜ To Do | | 1h |
| Total plays per story | 🔴 High | ⬜ To Do | | 0.5h |
| **Auto-Save** |
| Implement GameStateMemento (Memento pattern) | 🔴 High | ⬜ To Do | | 2h |
| Create PlaySession model | 🔴 High | ⬜ To Do | | 0.5h |
| Cookie-based session storage | 🔴 High | ⬜ To Do | | 1h |
| Resume game functionality | 🔴 High | ⬜ To Do | | 1h |
| **Draft/Published** |
| Enforce draft visibility | 🔴 High | ⬜ To Do | | 1h |
| Preview mode for drafts | 🟡 Medium | ⬜ To Do | | 1h |
| **UX Improvements** |
| Improved layout | 🟡 Medium | ⬜ To Do | | 1h |
| Confirmation dialogs (delete) | 🟡 Medium | ⬜ To Do | | 0.5h |
| Success/error messages | 🟡 Medium | ⬜ To Do | | 0.5h |

**Sprint 2 Total:** ~12 hours | **Checkpoint:** Level 13 ✓

---

### Sprint 3: Security & Auth (Day 4) - Level 16

| Task | Priority | Status | Assignee | Est. Hours |
|------|----------|--------|----------|------------|
| **Authentication** |
| User registration view | 🔴 High | ⬜ To Do | | 1h |
| Login/logout views | 🔴 High | ⬜ To Do | | 1h |
| Create UserProfile model with role | 🔴 High | ⬜ To Do | | 0.5h |
| Role choices (Reader/Author/Admin) | 🔴 High | ⬜ To Do | | 0.5h |
| **Permissions** |
| Create @role_required decorator | 🔴 High | ⬜ To Do | | 1h |
| Create @author_required decorator | 🔴 High | ⬜ To Do | | 0.5h |
| Create @admin_required decorator | 🔴 High | ⬜ To Do | | 0.5h |
| Create @story_owner_required decorator | 🔴 High | ⬜ To Do | | 1h |
| **Protected Views** |
| Protect author dashboard | 🔴 High | ⬜ To Do | | 0.5h |
| Protect story create/edit/delete | 🔴 High | ⬜ To Do | | 0.5h |
| Enforce story ownership | 🔴 High | ⬜ To Do | | 1h |
| **User Features** |
| Link Play.user (required) | 🔴 High | ⬜ To Do | | 0.5h |
| "My History" view for readers | 🔴 High | ⬜ To Do | | 1h |
| **API Security** |
| X-API-KEY middleware (Flask) | 🔴 High | ⬜ To Do | | 1h |
| Configure Django to send API key | 🔴 High | ⬜ To Do | | 0.5h |
| Reject invalid keys (401) | 🔴 High | ⬜ To Do | | 0.5h |
| **Moderation** |
| Admin story suspension | 🔴 High | ⬜ To Do | | 1h |
| Block playing suspended stories | 🔴 High | ⬜ To Do | | 0.5h |

**Sprint 3 Total:** ~12 hours | **Checkpoint:** Level 16 ✓

---

### Sprint 4: Community & Visualization (Days 5-6) - Level 18

| Task | Priority | Status | Assignee | Est. Hours |
|------|----------|--------|----------|------------|
| **Ratings** |
| Create Rating model | 🔴 High | ⬜ To Do | | 0.5h |
| Rating form (1-5 stars) | 🔴 High | ⬜ To Do | | 1h |
| Display average rating | 🔴 High | ⬜ To Do | | 0.5h |
| Rating count display | 🟡 Medium | ⬜ To Do | | 0.5h |
| **Comments** |
| Create Comment model | 🔴 High | ⬜ To Do | | 0.5h |
| Comment form | 🔴 High | ⬜ To Do | | 1h |
| Display comments list | 🔴 High | ⬜ To Do | | 0.5h |
| **Reports** |
| Create Report model | 🔴 High | ⬜ To Do | | 0.5h |
| Report form with reason | 🔴 High | ⬜ To Do | | 1h |
| Admin reports list | 🔴 High | ⬜ To Do | | 1h |
| Report status management | 🔴 High | ⬜ To Do | | 0.5h |
| **Illustrations** |
| Add illustration_url to Story (Flask) | 🟡 Medium | ⬜ To Do | | 0.5h |
| Add illustration_url to Page (Flask) | 🟡 Medium | ⬜ To Do | | 0.5h |
| Display illustrations in play view | 🟡 Medium | ⬜ To Do | | 1h |
| **Dice Rolls** |
| Add dice_required to Choice (Flask) | 🔴 High | ⬜ To Do | | 0.5h |
| Add min_roll to Choice (Flask) | 🔴 High | ⬜ To Do | | 0.5h |
| Dice roller component (JS) | 🔴 High | ⬜ To Do | | 2h |
| Integrate dice into gameplay | 🔴 High | ⬜ To Do | | 1h |
| **Story Tree Visualization** |
| Create /stories/<id>/tree endpoint | 🔴 High | ⬜ To Do | | 1h |
| D3.js force-directed graph | 🔴 High | ⬜ To Do | | 3h |
| Color nodes (start/regular/ending) | 🟡 Medium | ⬜ To Do | | 0.5h |
| Player path highlighting | 🟡 Medium | ⬜ To Do | | 1h |

**Sprint 4 Total:** ~18 hours | **Checkpoint:** Level 18 ✓

---

### Sprint 5: Polish & Deploy (Day 7)

| Task | Priority | Status | Assignee | Est. Hours |
|------|----------|--------|----------|------------|
| **Testing** |
| Flask API unit tests | 🟡 Medium | ⬜ To Do | | 2h |
| Django view tests | 🟡 Medium | ⬜ To Do | | 2h |
| Integration tests | 🟡 Medium | ⬜ To Do | | 2h |
| **Docker (Bonus)** |
| Dockerfile for Flask | 🟢 Low | ⬜ To Do | | 1h |
| Dockerfile for Django | 🟢 Low | ⬜ To Do | | 1h |
| docker-compose.yml | 🟢 Low | ⬜ To Do | | 1h |
| Test Docker deployment | 🟢 Low | ⬜ To Do | | 1h |
| **Documentation** |
| README (setup, run, endpoints) | 🔴 High | ⬜ To Do | | 2h |
| Document test accounts | 🔴 High | ⬜ To Do | | 0.5h |
| Architecture documentation | 🟡 Medium | ⬜ To Do | | 1h |
| **Screenshots** |
| Story list screenshot | 🔴 High | ⬜ To Do | | 0.5h |
| Gameplay screenshot | 🔴 High | ⬜ To Do | | 0.5h |
| Author dashboard screenshot | 🔴 High | ⬜ To Do | | 0.5h |
| Story tree visualization screenshot | 🔴 High | ⬜ To Do | | 0.5h |
| Admin panel screenshot | 🔴 High | ⬜ To Do | | 0.5h |
| **Final Review** |
| Code cleanup | 🟡 Medium | ⬜ To Do | | 1h |
| Bug fixes | 🔴 High | ⬜ To Do | | 2h |

**Sprint 5 Total:** ~18 hours | **SUBMISSION READY ✓**

---

## 📈 Progress Tracker

| Level | Required Features | Status |
|-------|-------------------|--------|
| Level 10 | MVP - CRUD + Gameplay | ⬜ 0% |
| Level 13 | Search, Auto-save, UX | ⬜ 0% |
| Level 16 | Auth, Roles, API Key | ⬜ 0% |
| Level 18 | Ratings, Reports, Viz | ⬜ 0% |

---

## 🔑 Key Resources

| Resource | Link/Path |
|----------|-----------|
| Project Requirements | Python_for_web_dev_Final_project.docx |
| Architecture Diagram | NAHB_Architecture.drawio |
| Data Flow Diagram | NAHB_DataFlow.drawio |
| GitHub/GitLab Repo | [To be created] |

---

## 📝 Notes

### Design Pattern Locations
- **Singleton:** `django_app/core/services/api_client.py`
- **Factory:** `django_app/core/services/story_factory.py`
- **Mediator:** `django_app/core/services/game_mediator.py`
- **Memento:** `django_app/core/services/game_memento.py`

### Critical Reminders
1. ⚠️ Story content ONLY in Flask DB
2. ⚠️ Gameplay/User data ONLY in Django DB
3. ⚠️ X-API-KEY required for write operations
4. ⚠️ Test all role permissions

### Test Accounts to Create
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | Admin123! |
| Author | author1 | Author123! |
| Author | author2 | Author123! |
| Reader | reader1 | Reader123! |

---

## 📅 Daily Schedule Template

| Time | Activity |
|------|----------|
| 09:00-12:00 | Morning coding session |
| 12:00-13:00 | Lunch break |
| 13:00-17:00 | Afternoon coding session |
| 17:00-18:00 | Review & commit |
| 18:00-20:00 | Evening session (if needed) |

---

*Last Updated: February 2, 2026*
*Copy this to Notion and use the checkboxes to track progress!*
