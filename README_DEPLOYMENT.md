# 🚀 Deployment Guide - Indian Stock Market AI Agent

## Option 1: Streamlit Cloud (Recommended - Free)

### Step 1: Prepare Your Repository
1. Push your code to GitHub
2. Make sure all files are in the repository
3. Ensure `requirements.txt` is in the root directory

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Choose the main file: `main.py`
6. Click "Deploy!"

### Step 3: Configure Environment Variables (Optional)
In Streamlit Cloud settings, add:
```
ALPHA_VANTAGE_API_KEY=your_key_here
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## Option 2: Heroku (Paid)

### Step 1: Create Heroku Files
```bash
# Create Procfile
echo "web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt
```

### Step 2: Deploy
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Option 3: Railway (Free Tier Available)

### Step 1: Connect Repository
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will auto-detect it's a Python app

### Step 2: Configure
- Port: 8501
- Command: `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0`

## Option 4: Render (Free Tier Available)

### Step 1: Create render.yaml
```yaml
services:
  - type: web
    name: stock-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 2: Deploy
1. Connect GitHub repository
2. Render will auto-deploy

## Option 5: VPS/Cloud Server

### Using DigitalOcean, AWS, or Google Cloud
1. Create a virtual machine
2. Install Python and dependencies
3. Run with PM2 or systemd for process management

```bash
# Install PM2
npm install -g pm2

# Start app
pm2 start "streamlit run main.py --server.port=8501" --name stock-agent

# Save PM2 configuration
pm2 save
pm2 startup
```

## 🔧 Configuration for Production

### Environment Variables
Create a `.env` file with:
```
ALPHA_VANTAGE_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Security Considerations
1. Never commit API keys to repository
2. Use environment variables for sensitive data
3. Enable HTTPS in production
4. Set up proper logging and monitoring

## 📊 Monitoring & Maintenance

### Health Checks
- Monitor app uptime
- Check API rate limits
- Monitor memory usage
- Set up alerts for failures

### Updates
- Regular dependency updates
- Security patches
- Feature enhancements

## 🎯 Recommended Deployment Flow

1. **Start with Streamlit Cloud** (Free, easy setup)
2. **Scale to Railway/Render** if you need more resources
3. **Move to VPS** for full control and customization

## 📱 Custom Domain (Optional)

### For Streamlit Cloud
- Not directly supported
- Use Cloudflare or similar for custom domain

### For Other Platforms
- Most support custom domains
- Configure DNS settings
- Enable SSL certificates

## 🚨 Troubleshooting

### Common Issues
1. **Port binding errors**: Use `--server.address=0.0.0.0`
2. **Memory issues**: Optimize data loading
3. **API rate limits**: Implement caching
4. **Slow loading**: Use CDN for static assets

### Performance Optimization
1. Cache market data
2. Implement data pagination
3. Use async operations where possible
4. Optimize chart rendering
