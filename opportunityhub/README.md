# 🚀 OpportunityHub Kenya

> *Connecting Kenyan Youth with Opportunities Through Intelligent Matching*

A Django REST Framework-based platform that bridges the gap between Kenyan youth seeking opportunities and employers offering jobs, gigs, and internships. Features comprehensive profile management, opportunity listings, application tracking, and email notifications.

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
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

OpportunityHub Kenya addresses youth unemployment by:

- **Youth**: Create profiles with skills, experience, and preferences
- **Employers**: Post opportunities and find qualified candidates
- **Application Management**: Streamlined application and hiring workflow
- **Email Notifications**: Automated alerts for new opportunities and application updates
- **Advanced Filtering**: Search by skills, location, category, and more

---

## ✨ Features

### For Youth
- ✅ Comprehensive profile management (skills, experience, education)
- ✅ Browse and search opportunities
- ✅ One-click job applications
- ✅ Email notifications for application updates
- ✅ Application status tracking
- ✅ Profile visibility settings

### For Employers
- ✅ Post unlimited opportunities
- ✅ Review and manage applications
- ✅ Company profile and verification system
- ✅ Application status management
- ✅ Candidate filtering and search

### Platform Features
- ✅ JWT-based authentication
- ✅ Role-based access control (Youth/Employer)
- ✅ Advanced filtering (skills, location, category)
- ✅ Email notifications via Resend
- ✅ RESTful API with comprehensive documentation
- ✅ Secure password management
- ✅ Token-based authentication

---

## 🛠️ Tech Stack

| Category           | Technology                                    |
| ------------------ | --------------------------------------------- |
| **Backend**        | Django 4.2+, Django REST Framework            |
| **Database**       | PostgreSQL (Production), SQLite (Development) |
| **Authentication** | JWT / Token Authentication                    |
| **Caching**        | Redis (Optional)                              |
| **Email Service**  | Resend                                        |
| **Documentation**  | drf-yasg / Swagger                            |
| **Testing**        | pytest, pytest-django                         |
| **Deployment**     | Render / Railway / Heroku                     |

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
├── applications/          # Application management system
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── notifications/         # Email notification system
│   ├── models.py
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
git clone https://github.com/Brhyancodes/opportunityhub-kenya.git
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
# Edit .env with your configuration:
# - SECRET_KEY
# - DATABASE_URL (for production)
# - RESEND_API_KEY
# - Email settings
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

| Endpoint              | Method | Description                    |
| --------------------- | ------ | ------------------------------ |
| `/api/auth/register/` | POST   | Register new user              |
| `/api/auth/login/`    | POST   | User login (returns JWT token) |
| `/api/auth/logout/`   | POST   | User logout                    |
| `/api/auth/profile/`  | GET    | Get current user profile       |

### Youth Profile Endpoints

| Endpoint                 | Method                 | Description               |
| ------------------------ | ---------------------- | ------------------------- |
| `/api/youth/profile/`    | GET, PUT               | View/update youth profile |
| `/api/youth/skills/`     | POST, DELETE           | Add/remove skills         |
| `/api/youth/experience/` | GET, POST, PUT, DELETE | Manage work experience    |
| `/api/youth/education/`  | GET, POST, PUT, DELETE | Manage education history  |

### Employer Endpoints

| Endpoint                            | Method    | Description                  |
| ----------------------------------- | --------- | ---------------------------- |
| `/api/employers/profile/`           | GET, PUT  | View/update employer profile |
| `/api/employers/opportunities/`     | GET, POST | List/create opportunities    |
| `/api/employers/applications/`      | GET       | View received applications   |
| `/api/employers/applications/<id>/` | PUT       | Update application status    |

### Opportunity Endpoints

| Endpoint                     | Method | Description              |
| ---------------------------- | ------ | ------------------------ |
| `/api/opportunities/`        | GET    | List all opportunities   |
| `/api/opportunities/<id>/`   | GET    | View opportunity details |
| `/api/opportunities/search/` | GET    | Search with filters      |
| `/api/opportunities/apply/`  | POST   | Apply for opportunity    |

### Application Endpoints

| Endpoint                           | Method | Description              |
| ---------------------------------- | ------ | ------------------------ |
| `/api/applications/`               | GET    | View user's applications |
| `/api/applications/<id>/`          | GET    | View application details |
| `/api/applications/<id>/withdraw/` | POST   | Withdraw application     |

### Notification Endpoints

| Endpoint                          | Method   | Description                     |
| --------------------------------- | -------- | ------------------------------- |
| `/api/notifications/`             | GET      | View notifications              |
| `/api/notifications/<id>/read/`   | POST     | Mark notification as read       |
| `/api/notifications/preferences/` | GET, PUT | Manage notification preferences |

**Full interactive documentation available at:** `/api/docs/` (Swagger UI)

---

## 📅 Development Timeline

### ✅ Week 1: Foundation & Authentication (COMPLETED)
- [x] Project setup
- [x] Custom User model
- [x] Basic app structure
- [x] JWT authentication endpoints
- [x] User registration and login

### ✅ Week 2: Profiles & Skills (COMPLETED)
- [x] Youth profile models
- [x] Employer profile models
- [x] Skills and experience management
- [x] Serializers
- [x] Profile CRUD endpoints

### ✅ Week 3: Opportunities & Applications (COMPLETED)
- [x] Opportunity models
- [x] Application system
- [x] Filtering & search
- [x] Application status workflow
- [x] Email notifications via Resend

---

## 🔮 Future Enhancements

### Phase 2: Smart Matching (Planned)
- [ ] AI-based matching algorithm
- [ ] Skill-based recommendation engine
- [ ] Match scoring system
- [ ] Personalized opportunity suggestions

### Phase 3: Advanced Communications (Planned)
- [ ] SMS notifications via Africa's Talking API
- [ ] In-app messaging system
- [ ] Real-time chat between employers and candidates
- [ ] Push notifications for mobile apps

### Phase 4: Advanced Features (Planned)
- [ ] Resume/CV builder
- [ ] Interview scheduling system
- [ ] Video interview integration
- [ ] Analytics dashboard for employers
- [ ] Mobile applications (iOS & Android)
- [ ] Payment integration for premium features

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific app tests
pytest accounts/tests/
pytest opportunities/tests/
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

**Brian Wakhale**
- GitHub: [@Brhyancodes](https://github.com/Brhyancodes)
- LinkedIn: [Brian Wakhale](https://www.linkedin.com/in/brian-wakhale/)

---

## 🙏 Acknowledgments

- Built as a Capstone Project for ALX BackEnd Engineering Program
- Inspired by the need to reduce youth unemployment in Kenya
- Special thanks to the Django and DRF communities
- Email service powered by [Resend](https://resend.com)

---

## 📞 Contact & Support

For questions or support:
- Reach out via [LinkedIn](https://www.linkedin.com/in/brian-wakhale/)
- 🐛 Issues: [GitHub Issues](https://github.com/Brhyancodes/opportunityhub-kenya/issues)

---

**⭐ If you find this project useful, please consider giving it a star!**