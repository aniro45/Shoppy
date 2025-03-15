# ShopEase

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ShopEase.git
    cd ShopEase
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Project

1. Set the environment variables:
    ```sh
    export FLASK_APP=run.py
    export FLASK_ENV=development
    ```

2. Initialize the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

3. Run the Flask application:
    ```sh
    flask run
    ```

## Usage

- Access the application at `http://127.0.0.1:5000/`
- Use the provided RESTful API endpoints to interact with the application

## License

This project is licensed under the MIT License.
