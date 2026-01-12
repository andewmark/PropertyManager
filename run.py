import os
import subprocess
from app import create_app
from urllib.parse import urlparse, urlunparse

# Load existing DATABASE_URL from .env
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Get current WSL IP dynamically
    try:
        wsl_ip = subprocess.check_output(
            "hostname -I | awk '{print $1}'", shell=True
        ).decode().strip()
        print(f"Detected WSL IP: {wsl_ip}")
    except Exception as e:
        print("Failed to fetch WSL IP:", e)
        wsl_ip = None

    if wsl_ip:
        # Parse URL and replace the host with current WSL IP
        parsed = urlparse(database_url)
        new_netloc = f"{parsed.username}:{parsed.password}@{wsl_ip}:{parsed.port}"
        database_url = urlunparse((
            parsed.scheme,
            new_netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        # Override environment variable at runtime
        os.environ["DATABASE_URL"] = database_url
        print(f"Dynamically updated DATABASE_URL: {database_url}")

# 4️⃣ Now create the app
app = create_app()

print("DB Loaded:", bool(os.getenv("DATABASE_URL")))

if __name__ == "__main__":
    app.run(debug=True)
