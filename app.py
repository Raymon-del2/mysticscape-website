from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_oauthlib.client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
import uuid
import hmac
import hashlib
import logging
from datetime import datetime, timedelta
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mysticscape.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-replace-in-production'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mysticscape.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
oauth = OAuth(app)

# OAuth Configuration
google = oauth.remote_app(
    'google',
    consumer_key='your-google-client-id',
    consumer_secret='your-google-client-secret',
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)

github = oauth.remote_app(
    'github',
    consumer_key='your-github-client-id',
    consumer_secret='your-github-client-secret',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

# PesaPal Configuration
PESAPAL_CONSUMER_KEY = os.getenv('PESAPAL_CONSUMER_KEY', 'your-consumer-key')
PESAPAL_CONSUMER_SECRET = os.getenv('PESAPAL_CONSUMER_SECRET', 'your-consumer-secret')
PESAPAL_TESTING = True  # Set to False in production

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    oauth_provider = db.Column(db.String(20))
    oauth_id = db.Column(db.String(100))
    has_paid = db.Column(db.Boolean, default=False)
    payment_status = db.Column(db.String(20), default='pending')
    payment_date = db.Column(db.DateTime)
    payment_expiry = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(100))
    subscription_type = db.Column(db.String(20), default='monthly')  # monthly, yearly
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    terms_accepted = db.Column(db.Boolean, default=False)
    terms_accepted_date = db.Column(db.DateTime)

    def check_subscription(self):
        if self.is_admin or self.email == 'wambuiraymond03@gmail.com':
            return True
        if not self.payment_expiry:
            return False
        return datetime.utcnow() < self.payment_expiry

    def renew_subscription(self, months=1):
        if self.email == 'wambuiraymond03@gmail.com':
            self.has_paid = True
            self.is_admin = True
            db.session.commit()
            return
            
        if self.payment_expiry and self.payment_expiry > datetime.utcnow():
            self.payment_expiry = self.payment_expiry + timedelta(days=30 * months)
        else:
            self.payment_expiry = datetime.utcnow() + timedelta(days=30 * months)
        self.has_paid = True
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def check_payment_status():
    if current_user.is_authenticated:
        if current_user.payment_expiry and current_user.payment_expiry < datetime.utcnow():
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/login/github')
def github_login():
    return github.authorize(callback=url_for('github_authorized', _external=True))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))
            
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('payment'))
    return render_template('signup.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(email=email)
        user.password_hash = generate_password_hash(password)
        
        # Set special privileges for admin email
        if email == 'wambuiraymond03@gmail.com':
            user.is_admin = True
            user.has_paid = True
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('download'))
    
    return render_template('register.html')

def process_payment(user, subscription_type):
    try:
        amount = 50 if subscription_type == 'monthly' else 1000
        
        # Create PesaPal payment request
        payment_data = {
            'Amount': amount,
            'Description': f'Mysticscape {subscription_type} subscription',
            'Type': 'MERCHANT',
            'Reference': f'MSC-{user.id}-{int(time.time())}',
            'Email': user.email
        }
        
        # Generate iframe URL (you'll need to implement this based on PesaPal's API)
        iframe_url = generate_pesapal_iframe(payment_data)
        
        return True, iframe_url
    except Exception as e:
        logger.error(f"Payment processing error: {str(e)}")
        return False, None

def generate_pesapal_iframe(payment_data):
    # Implement PesaPal iframe generation here
    base_url = 'https://demo.pesapal.com/api/PostPesapalDirectOrderV4' if PESAPAL_TESTING else 'https://www.pesapal.com/api/PostPesapalDirectOrderV4'
    
    # Add your PesaPal iframe generation logic here
    return base_url

@app.route('/payment')
@login_required
def payment():
    subscription_type = request.args.get('type', 'monthly')
    success, iframe_url = process_payment(current_user, subscription_type)
    
    if success:
        return render_template('payment.html', iframe_url=iframe_url)
    else:
        flash('Error processing payment. Please try again.')
        return redirect(url_for('download'))

@app.route('/pesapal-ipn', methods=['POST'])
def pesapal_ipn():
    try:
        # Verify PesaPal IPN
        reference = request.form.get('pesapal_merchant_reference')
        transaction_id = request.form.get('pesapal_transaction_tracking_id')
        status = request.form.get('pesapal_notification_type')
        
        if status == 'COMPLETED':
            # Update user subscription
            user_id = int(reference.split('-')[1])
            user = User.query.get(user_id)
            if user:
                subscription_type = 'monthly'  # You'll need to store this with the payment
                months = 1 if subscription_type == 'monthly' else 12
                user.renew_subscription(months)
                
        return 'ok', 200
    except Exception as e:
        logger.error(f"PesaPal IPN error: {str(e)}")
        return 'error', 500

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/accept-terms', methods=['POST'])
@login_required
def accept_terms():
    current_user.terms_accepted = True
    current_user.terms_accepted_date = datetime.utcnow()
    db.session.commit()
    flash('Terms and Conditions accepted')
    return redirect(url_for('download'))

@app.route('/download')
@login_required
def download():
    if not current_user.terms_accepted and current_user.email != 'wambuiraymond03@gmail.com':
        flash('Please accept the Terms and Conditions first')
        return redirect(url_for('terms'))
        
    if current_user.email == 'wambuiraymond03@gmail.com':
        return render_template('download.html')
        
    if not current_user.has_paid:
        flash('Please complete payment to access downloads')
        return redirect(url_for('payment'))
    if not check_payment_status():
        flash('Your subscription has expired. Please renew to continue.')
        return redirect(url_for('payment'))
    return render_template('download.html')

DOWNLOAD_URLS = {
    'windows': 'https://github.com/yourusername/mysticscape/releases/latest/download/mysticscape_windows.exe',
    'mac': 'https://github.com/yourusername/mysticscape/releases/latest/download/mysticscape_mac.dmg',
    'linux': 'https://github.com/yourusername/mysticscape/releases/latest/download/mysticscape_linux.AppImage'
}

@app.route('/download/<os>')
@login_required
def download_file(os):
    if current_user.email != 'wambuiraymond03@gmail.com':
        if not current_user.has_paid:
            flash('Please complete payment to access downloads')
            return redirect(url_for('payment'))
        if not check_payment_status():
            flash('Your subscription has expired. Please renew to continue.')
            return redirect(url_for('payment'))
    
    if os not in DOWNLOAD_URLS:
        flash('Invalid operating system selected')
        return redirect(url_for('download'))
    
    return redirect(DOWNLOAD_URLS[os])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/check-subscription')
@login_required
def check_subscription():
    days_left = 0
    if current_user.payment_expiry:
        delta = current_user.payment_expiry - datetime.utcnow()
        days_left = max(0, delta.days)
    
    return jsonify({
        'active': current_user.check_subscription(),
        'days_left': days_left,
        'expiry_date': current_user.payment_expiry.strftime('%Y-%m-%d') if current_user.payment_expiry else None
    })

@app.route('/renew-subscription', methods=['POST'])
@login_required
def renew_subscription():
    try:
        data = request.get_json()
        subscription_type = data.get('type', 'monthly')
        months = 12 if subscription_type == 'yearly' else 1
        
        # Process payment here (using PesaPal)
        payment_successful = process_payment(current_user, subscription_type)
        
        if payment_successful:
            current_user.subscription_type = subscription_type
            current_user.renew_subscription(months)
            
            return jsonify({
                'success': True,
                'message': f'Successfully renewed {subscription_type} subscription',
                'expiry_date': current_user.payment_expiry.strftime('%Y-%m-%d')
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Payment processing failed'
            }), 400
            
    except Exception as e:
        logger.error(f"Subscription renewal error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during renewal'
        }), 500

@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        # Check file system
        for os_type in ['windows', 'mac', 'linux']:
            file_path = os.path.join('static', 'downloads', f'mysticscape_{os_type}')
            if not os.path.exists(file_path):
                raise FileNotFoundError(f'Missing installer for {os_type}')
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
