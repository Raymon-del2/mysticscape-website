# Deploying Mysticscape to Render.com

## Step-by-Step Deployment Guide

### 1. Prepare Your GitHub Repository
1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/mysticscape.git
git push -u origin main
```

### 2. Sign Up for Render.com
1. Go to [Render.com](https://render.com)
2. Sign up using your GitHub account
3. Choose the free tier

### 3. Deploy Your Web Service
1. Click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: mysticscape
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
   - Free Instance Type (512 MB)

### 4. Set Environment Variables
Add these in Render Dashboard:
- SECRET_KEY (Render will generate this)
- PESAPAL_CONSUMER_KEY (Your PesaPal key)
- PESAPAL_CONSUMER_SECRET (Your PesaPal secret)
- FLASK_ENV=production

### 5. Database Setup
1. Use SQLite for free tier
2. Database file will be in the project directory
3. Ensure write permissions are set correctly

### 6. Upload Software Files
1. Create a GitHub release
2. Upload your software installers as release assets:
   - mysticscape_windows.exe
   - mysticscape_mac.dmg
   - mysticscape_linux.AppImage

### 7. Test Your Deployment
1. Visit your app at: https://mysticscape.onrender.com
2. Test user registration
3. Test admin access (wambuiraymond03@gmail.com)
4. Test PesaPal payments
5. Test file downloads

### 8. Free Tier Limitations
- 512 MB RAM
- Shared CPU
- Spins down after 15 minutes of inactivity
- 750 hours/month free usage
- 100 GB/month bandwidth

### 9. Monitoring
1. Use Render's built-in logs
2. Monitor the /health endpoint
3. Set up free monitoring with UptimeRobot

### 10. Troubleshooting
Common issues and solutions:
1. Application Errors:
   - Check Render logs
   - Verify environment variables
   - Check build logs

2. Slow Performance:
   - Free tier limitations
   - Service may need to spin up

3. Database Issues:
   - Check SQLite file permissions
   - Verify database path

### 11. Maintenance
Regular tasks:
1. Monitor disk usage
2. Update software installers
3. Check error logs
4. Update dependencies

### 12. Security Notes
1. Never commit sensitive data
2. Use environment variables
3. Keep dependencies updated
4. Monitor GitHub security alerts

### Support
For issues contact:
- Technical Support: wambuiraymond03@gmail.com
- Payment Issues: wambuiraymond03@gmail.com
