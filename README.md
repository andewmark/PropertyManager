# Property Manager Web Application
###### Name of application to be updated
> [!NOTE]
> This web application is still currently under development

## Overview
This Property Manager web application is designed to help landlords and property managers efficiently track and manage their real estate portfolio in one centralized system. 

## Tech Stack
- Backend: Flask (Python)
- Database: PostgreSQL
- Frontend: Jinja / HTML / TailwindCSS

## Setting up
This Project uses docker, so it's very simple to setup!

If you don't already have Docker Desktop Installed visit Docker's Installation page [Here](https://docs.docker.com/desktop/) and check out how to setup Docker in [this section](#-docker-desktop-setup)

> [!IMPORTANT]
> This project currently only works on Linux and Linux like machines to get setup. If you are using a Windows machine, [Install and setup WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and check out the [Setup Docker on WSL](#windows-with-wsl-2---reccomended) section.

To start the web app all you need to do is the following:
```bash
./setup.sh
```

### `⚙️ setup.sh`
The `setup.sh` script automates the complete local development environment setup using Docker. Running this script will reset and rebuild the application stack from a clean state.

Specifically, it performs the following steps:
1. Shuts down all running Docker containers and removes associated volumes to ensure a clean database state.
2. Rebuilds and starts all services defined in `docker-compose.yml` in detatched mode.
3. Waits briefly for the containers to fully intialize.
4. Applies all Flask database migrations using flask db upgrade
5. Copies the databases seed file into the PostgreSQL container
6. Seeds the datasbase with intial test data using psql
7. Confirms succesful completetion of the setup process

## 🐳 Docker Environment
This application is fully containerized using Docker and Docker Compose to ensure a consistent and repoducible development environment.

The Docker setup includes the following services:

### Web Service
- Flask application server
- Application dependencies installed via `requirements.txt`
- SQLAlchemy ORM and Alembic for database migrations

### Database Service
- PostgreSQL database
- Persistent storage via Docker volumes
- Preconfigured development credentials and database (`test_db`)
- Supports seeded data for local development - preconfigured test data already within test_db (need to run `./setup.sh`)

## 🐳 Docker Desktop Setup

This project requires **Docker Desktop** to run the application containers locally. Follow the instructions below based on your operating system

### Windows (with WSL 2 - Reccomended)
1. **Instal WSL 2**
    
    If WSL is not already installed, open PowerShell as Administrator and run:
    ```powershell
    wsl --install
    ```
    Restart your machine when prompted.
    You can verify installation with:
    ```powershell
    wsl --status
    ```
---
2. **Install Docker Desktop**
    - Download Docker Desktop from the [official Docker website](https://docs.docker.com/desktop/setup/install/windows-install/)
    - Run the installer and ensure "**Use WSL 2 instead of Hyper-V**" is enabled during setup
---
3. **Enable WSL Integration**:

    After Installation:
    1. Open Docker Desktop
    2. Navigate to **Settings -> Resources -> WSL Integration**
    3. Enable integration for your default WSL distribution
    4. Apply changes and restart Docker Desktop
---
4. **Verify Installation**
From your WSL terminal:
```bash
docker --version
docker-compose --version
```
Both commands should return version information
---
### MacOS
1. Download Docker Desktop from the [official Docker website](https://docs.docker.com/desktop/setup/install/mac-install/)
2. Install and launch Docker Desktop
3. Ensure Docker is running

Verify Installation:
```bash
docker --version 
docker-compose --version
```
---
### Linux
If you are running Linux natively, install Docker Enginer and Docker Compose using your distribution's package manager.

Ensure the Docker daemon is running:
```bash
docker ps
```
###
After Installation
Once Docker Desktop is installed and running, you can initialize the application with:
```bash
./setup.sh
```
> [!IMPORTANT]
> - Docker Desktop must be running before executing any Docker commands
> - On Windows, all project commands should be run inside WSL, not PowerShell
> - If Docker commands fail inside WSL, restart Docker Desktop and your WSL session

## Database Migrations
Database schema changes are managed using **Flask-Migrate (Alembic)** to ensure controlled and versioned updates to the database.

### When to Create a Migration
Create a new migration whenever you:
- Add, remove, or modify a database model
- Change relationshiips between tables
- Update constraints, indexes, or column types

### How to Create a Migration
Run the following command from the project root while the containers are running:
```bash
docker-compose exec web flask db migrate -m "Describe Change here"
```
This will generate a new migration file based on detected model changes.

### How to Apply Migrations
To apply all pending migrations to the database:
```bash
docker-compose exec web flask db upgrade
```
This command is automatically executed as part of `setup.sh` to ensure the dabaase schema is always up to date
> [!NOTE]
> I don't expect we create many schema changes going forward

### Important Notes
- Migrations should always be created **before** running `setup.sh`
- Do **NOT** mnaually modify the database schema outside of migrations
- If a migration fails, the database state should be reset by rerunning `setup.sh`