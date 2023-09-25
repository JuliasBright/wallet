# Wallet App

This is a simple wallet application with a Flask backend and a Vue.js frontend.

## Backend

The backend of this wallet application is built using Flask, a Python web framework. It provides the following functionality:

- User registration and login
- Account balance retrieval
- Balance Retrival
- Transaction history retrieval
- Crediting and debiting user accounts
- Redis caching for improved performance

### Installation and Setup

1. Clone this repository:

   ```shell
   git clone https://github.com/yourusername/wallet-app.git
   cd wallet-app
   ```

2. Install Python dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Configure the environment variables in `app.py`.

4. Initialize the database:

   ```shell
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Start the Flask backend:

   ```shell
   flask run
   ```

The backend should now be running on `http://localhost:5000`.

## Frontend

The frontend of this wallet application is built using Vue.js, a JavaScript framework. It provides a user-friendly interface for interacting with the backend API.

### Installation and Setup

1. Navigate to the `frontend` directory:

   ```shell
   cd frontend
   ```

2. Install JavaScript dependencies:

   ```shell
   yarn install
   ```

3. Start the Vue.js frontend:

   ```shell
   yarn run serve
   ```

The frontend should now be running on `http://localhost:8080`.

## Usage

- Access the frontend at `http://localhost:8080` in your web browser.
- Use the provided API endpoints to register, log in, view your balance, and perform transactions.

## Postman Collection

You can find a Postman collection in the `postman` folder, which includes pre-configured requests for testing the API endpoints.

### Postman Setup

1. Install [Postman](https://www.postman.com/).

2. Import the Postman collection from the `postman` folder.

3. Update the collection and environment variables to match your local setup.

4. Use the collection to test the API endpoints.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
