# LinkedIn Job Tracker 🚀

An automated LinkedIn job search monitor that sends email notifications for new job listings matching your criteria. Perfect for job seekers who want to stay updated on new opportunities without manually checking LinkedIn constantly.

## ✨ Features

- 🔍 **Automated Job Monitoring**: Continuously monitors LinkedIn for new job postings
- 📧 **Email Notifications**: Get instant email alerts when new jobs are found
- 🎯 **Customizable Filters**: Set your own keywords, location, experience level, and job type
- 💰 **Completely Free**: Uses GitHub Actions for free hosting
- 📊 **Smart Deduplication**: Avoids sending duplicate notifications for the same job
- 🎨 **Beautiful Email Templates**: Professional HTML email notifications with direct LinkedIn links

## 🚀 Quick Start

### Option 1: GitHub Actions (Recommended - Free Hosting)

1. **Fork this repository** to your GitHub account

2. **Set up Gmail App Password**:
   - Go to your Google Account settings
   - Enable 2-factor authentication
   - Generate an App Password for "Mail"
   - Copy the 16-character password

3. **Configure GitHub Secrets**:
   - Go to your forked repository → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `SENDER_EMAIL`: Your Gmail address
     - `SENDER_PASSWORD`: Your Gmail app password (16 characters)
     - `RECIPIENT_EMAIL`: Email where you want to receive notifications

4. **Customize Job Search Criteria**:
   - Edit the `config.json` file in the GitHub Actions workflow (`.github/workflows/job_tracker.yml`)
   - Modify keywords, location, experience level, etc.

5. **Enable GitHub Actions**:
   - Go to Actions tab in your repository
   - The workflow will run automatically every 30 minutes
   - You can also trigger manual runs

### Option 2: Local Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd linkedin-job-tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the tracker**:
   - Edit `config.json` with your preferences
   - Set up your email credentials

4. **Run the tracker**:
   ```bash
   # Run once
   python linkedin_job_tracker.py
   
   # Run continuously
   python linkedin_job_tracker.py --continuous
   ```

## ⚙️ Configuration

Edit `config.json` to customize your job search:

```json
{
  "search_criteria": {
    "keywords": ["python developer", "software engineer", "data scientist"],
    "location": "United States",
    "experience_level": ["Entry level", "Associate"],
    "job_type": ["Full-time"],
    "remote": true
  },
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "your-email@gmail.com"
  },
  "monitoring": {
    "check_interval_minutes": 30,
    "max_jobs_per_notification": 10
  }
}
```

### Search Criteria Options

- **keywords**: List of job title keywords to search for
- **location**: Geographic location for job search
- **experience_level**: 
  - "Entry level"
  - "Associate" 
  - "Mid-senior"
  - "Director"
  - "Executive"
- **job_type**:
  - "Full-time"
  - "Part-time"
  - "Contract"
  - "Temporary"
  - "Internship"
- **remote**: `true` to include remote jobs

## 📧 Email Setup

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Google Account
2. **Generate App Password**:
   - Go to Google Account → Security → 2-Step Verification
   - Click "App passwords"
   - Select "Mail" and generate password
   - Use this 16-character password in your config

### Alternative Email Providers

You can use other SMTP providers by changing the configuration:

```json
{
  "email": {
    "smtp_server": "smtp.your-provider.com",
    "smtp_port": 587,
    "sender_email": "your-email@your-provider.com",
    "sender_password": "your-password",
    "recipient_email": "your-email@your-provider.com"
  }
}
```

## 🔧 Customization

### Adding More Job Sources

The script can be easily extended to monitor other job sites:

1. Create a new method in `LinkedInJobTracker` class
2. Add the scraping logic for the new site
3. Integrate it into the `run_once()` method

### Custom Email Templates

Modify the `send_email_notification()` method to customize email appearance:

```python
def send_email_notification(self, jobs: List[Dict]):
    # Customize HTML template here
    html_body = """
    <html>
    <head>
        <style>
            /* Your custom CSS */
        </style>
    </head>
    <body>
        <!-- Your custom HTML -->
    </body>
    </html>
    """
```

## 🛠️ Troubleshooting

### Common Issues

1. **Email not sending**:
   - Check your Gmail app password is correct
   - Ensure 2-factor authentication is enabled
   - Verify SMTP settings

2. **No jobs found**:
   - Check your search criteria in `config.json`
   - Verify LinkedIn search URL is accessible
   - Check the logs for errors

3. **Duplicate notifications**:
   - The script automatically tracks seen jobs
   - Check `seen_jobs.json` file

### Logs

The script creates detailed logs in `job_tracker.log`. Check this file for debugging:

```bash
tail -f job_tracker.log
```

## 📊 Monitoring

### GitHub Actions Dashboard

- Go to Actions tab in your repository
- View workflow runs and logs
- Check for any failures or errors

### Local Monitoring

When running locally, the script provides real-time logging:

```
2024-01-15 10:30:00 - INFO - Starting job search...
2024-01-15 10:30:05 - INFO - Found 15 jobs
2024-01-15 10:30:05 - INFO - Found 3 new jobs
2024-01-15 10:30:08 - INFO - Email notification sent successfully
```

## 🔒 Privacy & Security

- **No data storage**: Job data is not stored permanently
- **Local processing**: All processing happens locally or in GitHub Actions
- **Secure credentials**: Email passwords are stored as GitHub secrets
- **No LinkedIn login required**: Uses public job search pages only

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with Python, BeautifulSoup, and requests
- Hosted for free on GitHub Actions
- Uses Gmail SMTP for email notifications

---

**Happy job hunting! 🎯**

If you find this tool helpful, please give it a ⭐ on GitHub! 