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
