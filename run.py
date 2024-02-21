import os
from app import app

# Set the secret key for the app
# You can replace this with a fixed key or use an environment variable
app.secret_key = os.urandom(16)  # or a fixed key, or use os.environ.get('SECRET_KEY')

if __name__ == "__main__":
    app.run()