# Aura

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Introduction
This is an Instagram clone built using Django and Django REST Framework. The API supports features such as user authentication, post creation with multiple media types (images and videos), user mentions, hashtags, likes, comments, notifications, and follow/unfollow functionality. The project follows a modular approach with robust handling for user privacy, post visibility, and media file management.

## Features
- **User Authentication**: JWT (JSON Web Token) based authentication system.
- **User Registration & Activation**: Users can register and activate their accounts via email.
- **Change Password & Account Management**: Users can change passwords, manage account settings, and deactivate accounts.
- **Media Support**: Users can upload multiple media types (images and videos) to their posts.
- **Social Interactions**:
  - Posts can be liked, commented on, and saved.
  - Users can follow or unfollow other users.
  - Blocked accounts and removed followers are handled efficiently.
  - Hashtags & Mentions: Posts can include hashtags and user mentions, automatically detected.
- **Notifications**: Real-time notifications for:
  1. Likes
  2. Comments
  3. Replies
  4. Mentions
  5. Follows
  6. Unfollows
  7. Follow Requests
  8. Accepting Follow Requests
  9. Post Saves
- **Saved Posts**: Users can save posts and remove saved posts.
     Account Privacy: Public and private accounts are supported.
     Commenting System: Users can comment on posts they follow or own, and comments can be replied to.
- **Search**: Users can search for other users, posts, tags, etc.
- **User Activity**: Users can view a list of blocked accounts and track their activities like comments, likes, and saves.
- **Pagination**: Pagination for efficient browsing.
- **Throttling**: The API uses rate limiting to ensure fair usage

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/d3m1s4m/Aura.git
   cd aura
   ```
   
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
    ```
   
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Configure environment variables: Create a local_settings.py file in the project directory and add your sensitive information. This file is ignored by Git using .gitignore.
    ```python
    SECRET_KEY = '<your-secret-key>'
    DEBUG = True
    
    DB = {
        'NAME': '<db-name>',
        'HOST': '<db-host>',
        'USER': '<db-user>',
        'PASSWORD': '<db-password>',
        'PORT': 5432
    }
    
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = '<your-email>'
    EMAIL_HOST_PASSWORD = '<your-email-password>'
    EMAIL_PORT = 587
    ```
5. Set up the database:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser account for the admin panel:
    ```bash
    python manage.py createsuperuser
    ```
   
7. Run the Celery worker:
    ```bash
    celery -A your_project worker -l info
    ```
   
8. Run the development server:

    ```bash
    python manage.py runserver
    ```
   
## Usage
The API is documented using Swagger and Redoc. You can access the API documentation through the following URLs after running the server:

    Swagger UI: /api/schema/swagger-ui/
    Redoc: /api/schema/redoc/

These will provide detailed information on all available endpoints and allow you to interact with the API.

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery, Redis
- **Authentication**: JWT (JSON Web Token), Djoser
- **Frontend**: N/A (API-only)
- **Notifications**: Real-time notifications using Django signals

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch (git checkout -b feature/your-feature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature).
5. Open a pull request, describing your changes in detail.
