# Flask Wallet Application

**Project Overview:**

Welcome to the Flask Wallet Application—a sophisticated financial tool designed to empower users with the ability to create accounts, perform secure transactions, and gain insights into their financial history. This application harnesses the power of Flask, PostgreSQL, JWT-based authentication, and meticulous code linting to deliver a robust and user-friendly financial experience.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
   - [Database Setup](#database-setup)
   - [Application Launch](#application-launch)
3. [Code Linting](#code-linting)
4. [Authentication](#authentication)
5. [Dockerization](#dockerization)
6. [API Documentation](#api-documentation)
7. [Contributing](#contributing)

## Prerequisites

Before diving into the setup, make sure you have the following prerequisites in place:

- **Python (3.7+)**: The project is Python-based, so ensure you have a compatible Python version installed.

- **PostgreSQL**: We rely on PostgreSQL as our trusty database system for this project. Be sure to have it set up and running.

- **Docker (optional)**: If you opt for containerization, Docker is your go-to tool.

## Getting Started

### Database Setup

1. **Database Creation**:

   Initialize your PostgreSQL database by running the following command:

   ```bash
   createdb wallet
   ```

2. **Migrations**:

   The database schema is managed via migrations. Get started with these commands:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

### Application Launch

1. **Dependency Installation**:

   Let's kick off by installing our project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Flask Application**:

   The Flask application is our financial powerhouse. Launch it with:

   ```bash
   python app.py
   ```

   Access the application locally at `http://localhost:5000`.

## Code Linting

Maintaining code quality is non-negotiable. We use Flake8 for this purpose. To initiate the linting process, simply execute:

```bash
flake8
```

Fine-tune linting rules according to project-specific coding standards in the `.flake8` configuration file.

## Authentication

You will need to create account using /creat-account endpoint.

Our robust authentication system is powered by JWT (JSON Web Tokens). Accessing the system is a breeze—simply send a POST request to `/login` with valid credentials to obtain a JWT token.

## Dockerization

If containerization aligns with your preferences, Docker offers a streamlined solution:

1. **Building the Docker Image**:

   Create a Docker image for the application:

   ```bash
   docker build -t flask-wallet-app .
   ```

2. **Running the Docker Container**:

   Initialize a Docker container, exposing it on port 8000:

   ```bash
   docker run -p 5000:5000 flask-wallet-app
   ```

   The application can now be accessed within the Docker container at `http://localhost:5000`.

3. **Testing the app***:
   Locate src/tests

   ```bash
   pytest app.py
   ```

   This should run all the tests

## API Documentation

Our API documentation shines through Swagger. To access the Swagger UI and explore the API, point your browser to `http://localhost:8000/api/spec.html` when the application is running.
