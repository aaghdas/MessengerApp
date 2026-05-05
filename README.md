# MessengerApp
This project is a secure, scalable real-time messaging application built with a microservices architecture.
It leverages Python's FastAPI framework for backend services, PostgreSQL for data storage, JWT for authentication, and React.js for a responsive frontend, designed as a Progressive Web App (PWA).
The system is divided into distinct microservices:  

Auth Service: Manages user registration, login, password resets, and JWT token issuance.  
User Service: Handles user profiles, contacts, and related data management.  
Messaging Service: Facilitates real-time chat using WebSockets, enabling users to send and receive messages instantly.

Key features include secure password hashing, password reset via email tokens, JWT-based stateless authentication, and WebSocket support for live messaging. The frontend provides a seamless user experience across devices, with registration, login, messaging, and notification capabilities—all within a PWA that can be installed on any device.
Designed entirely with free and open-source tools, this architecture ensures easy deployment on free hosting platforms such as Render, Railway, Vercel, or Netlify, making it ideal for learning, prototyping, or personal projects.
This project emphasizes security, modularity, and cross-platform compatibility, allowing users to communicate privately without requiring phone numbers.
It demonstrates how to build a modern messaging app with a clean separation of concerns, scalable backend services, and a user-friendly React interface.
Perfect for developers interested in microservices, real-time WebSocket communication, JWT security, and progressive web app development—all using entirely free resources.

## Technologies

- **Backend:** Python with FastAPI
- **Database:** PostgreSQL
- **Authentication:** JWT (JSON Web Tokens)
- **Frontend:** React.js as a Progressive Web App (PWA)
- **WebSocket:** For real-time chat communication
- **Deployment:** Free hosting services (e.g., Railway, Vercel, Render)

## Features

- User registration & login
- JWT-based secure authentication
- Real-time messaging via WebSocket
- Secure password reset through email tokens
- Cross-platform compatibility with a PWA
- Fully open-source, free, and customizable

## Project Structure
messenger-project/
│
├── auth_service/        # Authentifizierung & Nutzerverwaltung
├── user_service/        # Nutzerprofile & Kontakte
├── messaging_service/   # Chat & Messaging
├── shared/              # Gemeinsame Hilfsfunktionen
├── frontend/            # React PWA
└── README.md





