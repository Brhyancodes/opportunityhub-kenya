# 🚀 OpportunityHub Kenya

> *Connecting Kenyan Youth with Opportunities Through Intelligent Matching*

A Django REST Framework-based platform that bridges the gap between Kenyan youth seeking opportunities and employers offering jobs, gigs, and internships. Features smart skill-based matching, SMS notifications via Africa's Talking, and location-aware recommendations.

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Development Timeline](#-development-timeline)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

OpportunityHub Kenya addresses youth unemployment by:

- **Youth**: Create profiles with skills, experience, and preferences
- **Employers**: Post opportunities and find qualified candidates
- **Smart Matching**: Algorithm-based recommendations using skills, location, and experience
- **Real-time Notifications**: SMS and email alerts for new opportunities
- **Application Tracking**: Streamlined application and hiring workflow

---

## ✨ Features

### For Youth
- ✅ Comprehensive profile management (skills, experience, education)
- ✅ Smart opportunity recommendations based on profile
- ✅ One-click job applications
- ✅ SMS/Email notifications for matching opportunities
- ✅ Application status tracking

### For Employers
- ✅ Post unlimited opportunities
- ✅ Receive matched candidate recommendations
- ✅ Review and manage applications
- ✅ Company profile and verification system

### Platform Features
- ✅ JWT-based authentication
- ✅ Role-based access control (Youth/Employer)
- ✅ Advanced filtering (skills, location, category)
- ✅ SMS integration via Africa's Talking API
- ✅ Email notifications via SendGrid/Mailgun
- ✅ RESTful API with comprehensive documentation

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Django 4.2+, Django REST Framework |
| **Database** | PostgreSQL (Production), SQLite (Development) |
| **Authentication** | JWT / Token Authentication |
| **Caching** | Redis |
| **SMS Service** | Africa's Talking API |
| **Email Service** | SendGrid / Mailgun |
| **Documentation** | drf-yasg / Swagger |
| **Testing** | pytest, pytest-django |
| **Deployment** | Render / Railway / Heroku |

---

## 📁 Project Structure

```
opportunityhub/
├── accounts/              # User authentication & custom user model
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── youth_profiles/        # Youth profiles, skills, experience
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── employers/             # Employer profiles & company info
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── opportunities/         # Job/gig/internship postings
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── matching/              # Smart matching algorithm
│   ├── algorithm.py
│   ├── models.py
│   └── views.py
├── notifications/         # SMS & email notification system
│   ├── models.py
│   ├── sms_service.py
│   └── email_service.py
├── core/                  # Shared utilities & mixins
│   ├── utils.py
│   ├── mixins.py
│   └── permissions.py
├── api/                   # Main API routing
│   └── urls.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- Virtual environment tool (venv/virtualenv)
- PostgreSQL (for production)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/opportunityhub-kenya.git
cd opportunityhub-kenya
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the API!

---

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register new user |
| `/api/auth/login/` | POST | User login |
| `/api/auth/logout/` | POST | User logout |

### Youth Profile Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/youth/profile/` | GET, PUT | View/update youth profile |
| `/api/youth/skills/` | POST | Add skills |
| `/api/youth/experience/` | GET, POST, PUT, DELETE | Manage experience |

### Employer Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/employers/profile/` | GET, PUT | View/update employer profile |
| `/api/employers/opportunities/` | POST | Create opportunity |
| `/api/employers/applications/` | GET | View applications |

### Opportunity Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/opportunities/` | GET, POST | List/create opportunities |
| `/api/opportunities/<id>/` | GET, PUT, DELETE | Manage specific opportunity |
| `/api/opportunities/apply/` | POST | Apply for opportunity |

### Matching Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/matching/recommendations/` | GET | Get personalized recommendations |
| `/api/matching/generate/` | POST | Generate matches |

### Notification Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/notifications/` | GET | View notifications |
| `/api/notifications/preferences/` | POST | Update notification preferences |

**Full interactive documentation available at:** `/api/docs/` (Swagger UI)

---

## 📅 Development Timeline

### ✅ Week 1: Foundation & Authentication
- [x] Project setup
- [x] Custom User model
- [x] Basic app structure
- [ ] JWT authentication endpoints

### 🚧 Week 2: Profiles & Skills (Current)
- [x] Youth profile models
- [x] Employer profile models
- [ ] Serializers
- [ ] Profile CRUD endpoints

### 📝 Week 3: Opportunities & Applications
- [ ] Opportunity models
- [ ] Application system
- [ ] Filtering & search

### 🧠 Week 4: Smart Matching
- [ ] Matching algorithm
- [ ] Recommendation engine
- [ ] Match scoring system

### 🔔 Week 5: Notifications & Deployment
- [ ] SMS integration (Africa's Talking)
- [ ] Email notifications
- [ ] Testing & bug fixes
- [ ] Deployment

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific app tests
pytest accounts/tests/
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [Brhyancodes](https://github.com/Brhyancodes)
- LinkedIn: [Brian Wakhale](https://www.linkedin.com/in/brian-wakhale/)

---

## 🙏 Acknowledgments

- Built as a Capstone Project for ALX BackEnd Engineering Program
- Inspired by the need to reduce youth unemployment in Kenya
- Special thanks to the Django and DRF communities

---

## 📞 Contact & Support

For questions or support:
- Reach out via [LinkedIn](https://www.linkedin.com/in/brian-wakhale/)

- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/opportunityhub-kenya/issues)

---

**⭐ If you find this project useful, please consider giving it a star!**