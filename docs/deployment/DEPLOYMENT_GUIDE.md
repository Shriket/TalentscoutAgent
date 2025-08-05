# 🚀 TalentScout Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Requirements Verification
- [ ] Python 3.9+ installed
- [ ] Git repository access
- [ ] Google Cloud Console access
- [ ] Groq API account and key
- [ ] Domain/hosting platform ready (if applicable)

### ✅ Environment Setup
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables configured
- [ ] Google Sheets API enabled
- [ ] Service account created and shared

## 🏠 Local Development Deployment

### Step 1: Clone and Setup
```bash
# Clone repository
git clone https://github.com/shriket/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration
Create `.env` file:
```env
# AI Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Google Sheets Integration
GOOGLE_SHEET_ID=1_yIKa9TFFyMpy5L2E4isp0nwMSxb5ptwFPDQGUhEl34
GOOGLE_SERVICE_ACCOUNT_JSON={"type": "service_account", "project_id": "your-project", ...}

# Security Keys
SECRET_KEY=your-secret-key-minimum-32-characters
ENCRYPTION_KEY=your-encryption-key-for-fernet-32-bytes

# Application Settings
APP_ENV=development
DEBUG_MODE=True
LOG_LEVEL=INFO
```

### Step 3: Google Sheets Setup
1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project: "TalentScout-Hiring"
   - Enable Google Sheets API

2. **Create Service Account**:
   ```bash
   # Navigate to IAM & Admin > Service Accounts
   # Create service account: "talentscout-sheets-service"
   # Download JSON key file
   ```

3. **Setup Google Sheet**:
   - Create new Google Sheet: "TalentScout Candidate Data"
   - Share with service account email (Editor permissions)
   - Copy Sheet ID from URL

### Step 4: Launch Application
```bash
# Test configuration
python -c "from src.config.settings import Settings; print('Config OK')"

# Run application
streamlit run main.py

# Application will be available at: http://localhost:8501
```

## ☁️ Cloud Deployment Options

### Option 1: Streamlit Cloud (Recommended)

#### Prerequisites
- GitHub repository (public or private)
- Streamlit Cloud account
- Environment secrets configured

#### Deployment Steps
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Production ready deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub repository
   - Select branch: `main`
   - Main file path: `main.py`

3. **Configure Secrets**:
   ```toml
   # .streamlit/secrets.toml
   GROQ_API_KEY = "gsk_your_api_key"
   GOOGLE_SHEET_ID = "your_sheet_id"
   GOOGLE_SERVICE_ACCOUNT_JSON = '{"type": "service_account", ...}'
   SECRET_KEY = "your_secret_key"
   ENCRYPTION_KEY = "your_encryption_key"
   ```

4. **Deploy**:
   - Click "Deploy!"
   - Monitor deployment logs
   - Access via provided URL

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run
```bash
# Build Docker image
docker build -t talentscout-hiring-assistant .

# Run container
docker run -p 8501:8501 --env-file .env talentscout-hiring-assistant

# Or with docker-compose
docker-compose up -d
```

#### Docker Compose Configuration
```yaml
version: '3.8'
services:
  talentscout:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GOOGLE_SHEET_ID=${GOOGLE_SHEET_ID}
      - GOOGLE_SERVICE_ACCOUNT_JSON=${GOOGLE_SERVICE_ACCOUNT_JSON}
      - SECRET_KEY=${SECRET_KEY}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Option 3: Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Deployment Steps
1. **Create Heroku App**:
   ```bash
   heroku create talentscout-hiring-assistant
   ```

2. **Configure Environment Variables**:
   ```bash
   heroku config:set GROQ_API_KEY=your_api_key
   heroku config:set GOOGLE_SHEET_ID=your_sheet_id
   heroku config:set GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", ...}'
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set ENCRYPTION_KEY=your_encryption_key
   ```

3. **Create Procfile**:
   ```
   web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Heroku deployment"
   git push heroku main
   ```

## 🔧 Production Configuration

### Performance Optimization
```python
# .streamlit/config.toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

### Security Hardening
1. **Environment Variables**:
   - Never commit secrets to version control
   - Use strong, unique keys for encryption
   - Rotate API keys regularly

2. **Access Control**:
   - Restrict Google Sheets access to service account only
   - Use HTTPS in production
   - Implement rate limiting if needed

3. **Data Protection**:
   - Enable audit logging
   - Regular backup of Google Sheets data
   - Monitor for unauthorized access

### Monitoring Setup
```python
# Add to main.py for production monitoring
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

# Configure Sentry (optional)
sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[sentry_logging],
    traces_sample_rate=1.0
)
```

## 🧪 Testing in Production

### Health Checks
```bash
# Test application endpoints
curl -f http://your-domain.com/_stcore/health

# Test Google Sheets connectivity
python test_sheets_connection.py

# Run automated interview test
python final_test.py
```

### Load Testing
```bash
# Install load testing tools
pip install locust

# Create load test script
# locustfile.py
from locust import HttpUser, task, between

class TalentScoutUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_homepage(self):
        self.client.get("/")

# Run load test
locust -f locustfile.py --host=http://your-domain.com
```

## 📊 Monitoring & Maintenance

### Application Monitoring
1. **Uptime Monitoring**: Use services like UptimeRobot or Pingdom
2. **Performance Monitoring**: Track response times and error rates
3. **Usage Analytics**: Monitor interview completion rates
4. **GDPR Compliance**: Regular audit of data handling

### Regular Maintenance Tasks
- [ ] Weekly: Review error logs and performance metrics
- [ ] Monthly: Update dependencies and security patches
- [ ] Quarterly: Rotate API keys and encryption keys
- [ ] Annually: Full security audit and penetration testing

### Backup Strategy
1. **Google Sheets Data**: 
   - Automatic daily exports to cloud storage
   - Version control for sheet structure changes

2. **Application Code**:
   - Git repository with tagged releases
   - Docker images stored in registry

3. **Configuration**:
   - Encrypted backup of environment variables
   - Documentation of all external dependencies

## 🚨 Incident Response

### Common Issues and Solutions

#### High Response Times
1. Check Groq API status and quotas
2. Monitor Google Sheets API rate limits
3. Review application logs for bottlenecks
4. Scale resources if needed

#### Data Loss Prevention
1. Implement real-time data replication
2. Regular integrity checks
3. Automated backup verification
4. Disaster recovery procedures

#### Security Incidents
1. Immediate key rotation
2. Audit trail analysis
3. User notification (if required by GDPR)
4. System hardening improvements

### Emergency Contacts
- **Technical Lead**: [Your contact information]
- **Google Cloud Support**: [Support case system]
- **Groq API Support**: [API support channels]
- **GDPR Compliance Officer**: [Privacy contact]

## 📈 Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Session state management
- Database clustering (if moving from Google Sheets)

### Vertical Scaling
- Memory optimization for large datasets
- CPU scaling for concurrent interviews
- Storage scaling for audit logs

### Performance Optimization
- Caching strategies for frequently accessed data
- Async processing for non-blocking operations
- CDN integration for static assets

---

## ✅ Post-Deployment Verification

### Functional Testing
- [ ] Complete interview flow works end-to-end
- [ ] Google Sheets data saving verified
- [ ] GDPR consent and rights management functional
- [ ] All 21 data fields collecting properly
- [ ] Technical question generation working
- [ ] Sentiment analysis operational

### Performance Testing
- [ ] Response times under 2 seconds
- [ ] Multiple concurrent users supported
- [ ] Memory usage within acceptable limits
- [ ] Error handling graceful

### Security Testing
- [ ] Data encryption verified
- [ ] Access controls working
- [ ] Audit logging functional
- [ ] Privacy policy accessible
- [ ] Data subject rights operational

### Compliance Testing
- [ ] GDPR compliance score: 100%
- [ ] Privacy notices displayed
- [ ] Consent management working
- [ ] Data retention policies active
- [ ] Audit trails complete

---

**🎉 Congratulations! Your TalentScout Hiring Assistant is now deployed and ready for production use!**

For ongoing support and updates, refer to the [Technical Documentation](TECHNICAL_DOCUMENTATION.md) and [README](README.md).
