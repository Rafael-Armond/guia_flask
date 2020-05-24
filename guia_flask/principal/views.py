from flask import Blueprint, render_template, redirect, flash, request, url_for

# Blueprint
principal = Blueprint('principal',__name__,template_folder='templates')

# Index
@principal.route("/")
def index():
    return render_template("index.html")