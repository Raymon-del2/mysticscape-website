# Mysticscape Deployment Guide

## Prerequisites
1. PythonAnywhere account (www.pythonanywhere.com)
2. Your software installers ready for Windows, Mac, and Linux
3. PayPal business account for payment processing
4. Domain name (optional but recommended)

## Deployment Steps

### 1. Prepare Your Software Files
1. Place your software installers in the following locations:
   - `website/static/downloads/mysticscape_windows.exe`
   - `website/static/downloads/mysticscape_mac.dmg`
   - `website/static/downloads/mysticscape_linux.AppImage`

### 2. PythonAnywhere Setup
1. Create a PythonAnywhere account
2. Go to Web tab and create a new web app
3. Choose Manual Configuration -> Python 3.10
4. Set up your virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 mysticscape
   pip install -r requirements.txt
   ```

### 3. Database Setup
1. Go to Databases tab
2. Initialize MySQL database:
   - Create a new database named 'mysticscape'
   - Note down the database credentials
3. Update the database URI in wsgi.py with your credentials

### 4. File Upload
1. Upload your project files to PythonAnywhere:
   ```bash
   git clone https://github.com/yourusername/mysticscape.git
   # OR use the Files tab to upload manually
   ```

### 5. Configure Web App
1. Go to Web tab
2. Set your working directory to: `/home/yourusername/mysticscape/website`
3. Set WSGI configuration file path
4. Add environment variables:
   - SECRET_KEY
   - DATABASE_URL
   - PAYPAL_CLIENT_ID
   - PAYPAL_CLIENT_SECRET

### 6. SSL/HTTPS Setup
1. Enable HTTPS if you have a custom domain
2. Use Let's Encrypt for free SSL certificate

### 7. Final Steps
1. Reload your web app
2. Test all functionality:
   - User registration
   - Payment processing
   - File downloads
   - Admin access

## Maintenance

### Regular Tasks
1. Monitor server logs daily
2. Update software installers as needed
3. Check payment processing status
4. Monitor disk space usage

### Backup Strategy
1. Database: Daily automated backups
2. Files: Weekly backups of uploaded content
3. Configuration: Keep backup of all config files

## Troubleshooting

### Common Issues
1. 502 Bad Gateway
   - Check error logs
   - Verify WSGI file configuration
   - Restart web app

2. Database Connection Issues
   - Verify database credentials
   - Check connection pool settings
   - Ensure database service is running

3. File Download Issues
   - Verify file permissions
   - Check file paths
   - Monitor disk space

## Support Contacts
- Technical Support: wambuiraymond03@gmail.com
- Payment Issues: wambuiraymond03@gmail.com

## Security Notes
1. Keep all credentials secure
2. Regularly update dependencies
3. Monitor for suspicious activities
4. Implement rate limiting for downloads
