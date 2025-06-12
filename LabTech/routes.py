from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from Models.base_model import db
from Models.users import Staff, Role

lab_tech = Blueprint("lab_tech", __name__)