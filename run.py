import os
from app import create_app

app = create_app()

print("DB Loaded:", bool(os.getenv("DATABASE_URL")))

if __name__ == "__main__":
    app.run(debug=True)