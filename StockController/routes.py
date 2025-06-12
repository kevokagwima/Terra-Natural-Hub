from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from Models.base_model import db
from Models.users import Staff, Role

stock_controller = Blueprint("stock_controller", __name__)