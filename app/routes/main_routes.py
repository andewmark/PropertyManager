from flask import Blueprint, render_template

from app.extensions import db
from sqlalchemy import text

main = Blueprint("main", __name__)


@main.route("/")
def dashboard():
    return render_template("dashboard.html", page_title="Dashboard")


@main.route("/health/db")
def db_health():
    db.session.execute(text("SELECT 1"))
    return {"status": "connected"}


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@main.route("/payments")
def payments():
    return render_template("payments.html", page_title="Payments")


@main.route("/tenants")
def tenants():
    return render_template("tenants.html", page_title="Tenants")


@main.route("/maintenance")
def maintenance():
    return render_template("maintenance.html", page_title="Maintenance")


@main.route("/financials")
def financials():
    return render_template("financials.html", page_title="Financials")


@main.route("/documents")
def documents():
    return render_template("documents.html", page_title="Documents")


@main.route("/reports")
def reports():
    return render_template("reports.html", page_title="Reports")


@main.route("/settings")
def settings():
    return render_template("settings.html", page_title="Settings")


@main.route("/Security")
def security():
    return render_template("security.html", page_title="Security")
