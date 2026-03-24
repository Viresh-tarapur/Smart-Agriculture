import serial
import pynmea2
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from project import app, db
from project.models import User
from project.forms import RegisterForm, LoginForm

serial_port = 'COM3'

def read_gps():
    try:
        ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None, None

    while True:
        try:
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                return msg.latitude, msg.longitude
        except Exception as e:
            print(f"Error reading GPS data: {e}")
            return None, None

def get_bin_counts():
    # Mock data for example purposes. Replace with actual logic to fetch data.
    total_bins = 20
    half_filled_bins = 10
    empty_bins = 20
    return total_bins, half_filled_bins, empty_bins

@app.route('/location', methods=['GET'])
def get_location():
    latitude, longitude = read_gps()
    if latitude is None or longitude is None:
        return jsonify({'error': 'Unable to read GPS data'}), 500
    return jsonify({'latitude': latitude, 'longitude': longitude})

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def DashBoard():
    latitude, longitude = read_gps()
    if latitude is None or longitude is None:
        flash('Unable to read GPS data', 'danger')
        latitude, longitude = 0.0, 0.0  # Default values or handle as necessary
    total_bins, half_filled_bins, empty_bins = get_bin_counts()
    return render_template('dashboard.html', latitude=latitude, longitude=longitude,
                           total_bins=total_bins, half_filled_bins=half_filled_bins,
                           empty_bins=empty_bins)

@app.route('/about')
def About_page():
    return render_template('About.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Account created successfully!', 'success')
        return redirect(url_for('DashBoard'))
    if form.errors != {}:  # if there are no errors from the validation
        for err_msg in form.errors.values():
            flash(f'There was an error when creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password_correction(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('DashBoard'))
        else:
            flash('Invalid username or password. Please try again.', category="danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('login_page'))

@app.route('/disease_monitor')
@app.route('/main index.html')
def disease_monitor():
    return render_template('main_index.html')

@app.route('/monitor_dashboard')
@app.route('/monitor_dashboard.html')
def monitor_dashboard():
    return render_template('monitor_dashboard.html')

@app.route('/grade')
@app.route('/grade.html')
def grade():
    return render_template('grade.html')

@app.route('/marketplace')
@app.route('/Marketplace_dashboard.html')
def marketplace():
    return render_template('marketplace_dashboard.html')

@app.route('/predictions')
@app.route('/predictions.html')
def predictions():
    return render_template('predictions.html')

@app.route('/history')
@app.route('/history.html')
def history():
    return render_template('history.html')

@app.route('/what_to_grow')
@app.route('/what_to_grow.html')
def what_to_grow():
    return render_template('what_to_grow.html')

@app.route('/chatbot')
@app.route('/Chat Bot.html')
def chatbot():
    return render_template('Chat Bot.html')

@app.route('/gemini_info')
@app.route('/index for gemini.html')
def gemini_info():
    return render_template('index for gemini.html')
