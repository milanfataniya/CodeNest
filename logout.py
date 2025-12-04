from flask import Blueprint, render_template, session, redirect, url_for

logout_bp = Blueprint("logout_bp", __name__)

@logout_bp.route("/logout")
def logout():
    session.pop("username", None)  # Remove session key
    return redirect(url_for("login_bp.login"))  # Redirect properly
