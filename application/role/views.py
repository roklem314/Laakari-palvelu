from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from application import app
from application.registration.models import Users
