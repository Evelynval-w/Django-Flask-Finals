# NAHB - Not Another Hero's Book

An interactive storytelling platform inspired by
"Choose Your Own Adventure" books.

## 🎯 Features

- **Authors** create branching narrative stories
- **Readers** play through stories making choices
- Auto-save progress with resume functionality
- Statistics tracking (plays, endings distribution)
- Community features (ratings, comments, reports)
- Story tree visualization

## 🏗️ Architecture

Two-application architecture:
- **Flask API** (Port 5000): Story content stor
- **Django App** (Port 8000): Game engine, UI, 
authentication

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/
nahb-project.git
cd nahb-project

# Setup Flask API
cd flask_api
python -m venv venv
source venv/bin/activate  # Windows: 
venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade
flask run &

# Setup Django App (new terminal)
cd ../django_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Docker Setup

```bash
docker-compose up --build
```

## 📚 Documentation

See the [Wiki](../../wiki) for complete 
documentation:
- [Requirements Analysis](../../wiki/
Requirements-Analysis)
- [System Architecture](../../wiki/
System-Architecture)
- [Design Patterns](../../wiki/Design-Patterns)
- [API Documentation](../../wiki/API-Documentation)

## 🧪 Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | Admin123! |
| Author | author1 | Author123! |
| Reader | reader1 | Reader123! |

## 📁 Project Structure

```
nahb-project/
├── flask_api/          # REST API for story content
├── django_app/         # Web application
├── docs/               # Additional documentation
├── docker-compose.yml  # Docker orchestration
└── README.md
```

## 🎨 Design Patterns Used

1. **Singleton** - FlaskAPIClient
2. **Factory** - StoryFactory
3. **Mediator** - GameMediator
4. **Memento** - GameStateMemento

## 📝 License

MIT License
