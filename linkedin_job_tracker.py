#!/usr/bin/env python3
"""
LinkedIn Job Tracker
Automated job search monitor that sends email notifications for new listings
"""

import os
import json
import time
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_tracker.log'),
        logging.StreamHandler()
    ]
)

class LinkedInJobTracker:
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the job tracker with configuration"""
        self.config = self.load_config(config_file)
        self.seen_jobs_file = 'seen_jobs.json'
        self.seen_jobs = self.load_seen_jobs()
        self.last_run_file = 'last_run.json'
        self.last_run_time = self.load_last_run_time()
        
        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default config
            default_config = {
                "search_criteria": {
            "keywords": ["android", "cloud"],
            "location": "Ireland",
            "experience_level": [],
            "job_type": []
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
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            logging.info(f"Created default config file: {config_file}")
            return default_config
    
    def load_seen_jobs(self) -> set:
        """Load previously seen job IDs"""
        if os.path.exists(self.seen_jobs_file):
            with open(self.seen_jobs_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_seen_jobs(self):
        """Save seen job IDs to file"""
        with open(self.seen_jobs_file, 'w') as f:
            json.dump(list(self.seen_jobs), f)
    
    def load_last_run_time(self):
        if os.path.exists(self.last_run_file):
            with open(self.last_run_file, 'r') as f:
                return datetime.fromisoformat(json.load(f)['last_run'])
        else:
            # Default: 30 minutes ago
            return datetime.now() - timedelta(minutes=30)

    def save_last_run_time(self):
        with open(self.last_run_file, 'w') as f:
            json.dump({'last_run': datetime.now().isoformat()}, f)
    
    def build_search_url(self) -> str:
        """Build LinkedIn job search URL based on criteria"""
        criteria = self.config['search_criteria']
        
        # Base LinkedIn jobs URL
        base_url = "https://www.linkedin.com/jobs/search/?"
        
        # Build query parameters
        params = []
        
        # Keywords
        if criteria.get('keywords'):
            keywords = ' '.join(criteria['keywords'])
            params.append(f"keywords={keywords.replace(' ', '%20')}")
        
        # Location
        if criteria.get('location'):
            location = criteria['location'].replace(' ', '%20')
            params.append(f"location={location}")
        
        # Experience level
        if criteria.get('experience_level'):
            for level in criteria['experience_level']:
                if level.lower() == "entry level":
                    params.append("f_E=1")
                elif level.lower() == "associate":
                    params.append("f_E=2")
                elif level.lower() == "mid-senior":
                    params.append("f_E=3")
                elif level.lower() == "director":
                    params.append("f_E=4")
                elif level.lower() == "executive":
                    params.append("f_E=5")
        
        # Job type
        if criteria.get('job_type'):
            for job_type in criteria['job_type']:
                if job_type.lower() == "full-time":
                    params.append("f_JT=F")
                elif job_type.lower() == "part-time":
                    params.append("f_JT=P")
                elif job_type.lower() == "contract":
                    params.append("f_JT=C")
                elif job_type.lower() == "temporary":
                    params.append("f_JT=T")
                elif job_type.lower() == "internship":
                    params.append("f_JT=I")
        
        # Remote work
        if criteria.get('remote'):
            params.append("f_WT=2")  # Remote jobs
        
        # Sort by date posted
        params.append("sortBy=DD")  # Date posted
        
        return base_url + "&".join(params)
    
    def scrape_linkedin_jobs(self) -> List[Dict]:
        """Scrape job listings from LinkedIn"""
        try:
            url = self.build_search_url()
            logging.info(f"Searching jobs at: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            jobs = []
            
            # Find job cards
            job_cards = soup.find_all('div', class_='base-card')
            
            for card in job_cards[:20]:  # Limit to first 20 jobs
                try:
                    # Extract job information
                    job_id = card.get('data-entity-urn', '').split(':')[-1]
                    
                    # Job title
                    title_elem = card.find('h3', class_='base-search-card__title')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    # Company name
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    
                    # Location
                    location_elem = card.find('span', class_='job-search-card__location')
                    location = location_elem.get_text(strip=True) if location_elem else "N/A"
                    
                    # Posted time
                    time_elem = card.find('time')
                    posted_time = time_elem.get('datetime') if time_elem else "N/A"
                    
                    # Job URL
                    link_elem = card.find('a', class_='base-card__full-link')
                    job_url = link_elem.get('href') if link_elem else ""
                    
                    # Create job object
                    job = {
                        'id': job_id,
                        'title': title,
                        'company': company,
                        'location': location,
                        'posted_time': posted_time,
                        'url': job_url,
                        'found_at': datetime.now().isoformat()
                    }
                    
                    jobs.append(job)
                    
                except Exception as e:
                    logging.error(f"Error parsing job card: {e}")
                    continue
            
            logging.info(f"Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logging.error(f"Error scraping LinkedIn: {e}")
            return []
    
    def filter_new_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter out jobs that have already been seen"""
        new_jobs = []
        
        for job in jobs:
            job_hash = hashlib.md5(f"{job['id']}_{job['title']}_{job['company']}".encode()).hexdigest()
            
            if job_hash not in self.seen_jobs:
                new_jobs.append(job)
                self.seen_jobs.add(job_hash)
        
        logging.info(f"Found {len(new_jobs)} new jobs")
        return new_jobs
    
    def filter_jobs_by_time(self, jobs):
        new_jobs = []
        now = datetime.now()
        for job in jobs:
            # Parse job['posted_time'] to datetime
            # LinkedIn may use ISO format or relative time (e.g., '5 minutes ago')
            # You may need to parse accordingly
            try:
                posted_time = datetime.fromisoformat(job['posted_time'])
            except Exception:
                # Fallback: skip if can't parse
                continue
            if self.last_run_time < posted_time <= now:
                new_jobs.append(job)
        return new_jobs
    
    def send_email_notification(self, jobs: List[Dict]):
        """Send email notification with new job listings"""
        if not jobs:
            return
        
        email_config = self.config['email']
        
        # Create email content
        subject = f"New LinkedIn Job Alerts - {len(jobs)} new positions found"
        
        # Build HTML email body
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .job-card {{ 
                    border: 1px solid #ddd; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                .job-title {{ color: #0073b1; font-size: 18px; font-weight: bold; }}
                .company {{ color: #666; font-size: 14px; }}
                .location {{ color: #666; font-size: 12px; }}
                .apply-btn {{ 
                    background-color: #0073b1; 
                    color: white; 
                    padding: 8px 16px; 
                    text-decoration: none; 
                    border-radius: 3px;
                    display: inline-block;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <h2>🚀 New Job Opportunities Found!</h2>
            <p>We found {len(jobs)} new job listings matching your criteria:</p>
        """
        
        for job in jobs:
            html_body += f"""
            <div class="job-card">
                <div class="job-title">{job['title']}</div>
                <div class="company">{job['company']}</div>
                <div class="location">📍 {job['location']}</div>
                <div class="location">⏰ Posted: {job['posted_time']}</div>
                <a href="{job['url']}" class="apply-btn" target="_blank">View on LinkedIn</a>
            </div>
            """
        
        html_body += """
        <p><small>This notification was sent by your LinkedIn Job Tracker.</small></p>
        </body>
        </html>
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email_config['sender_email']
        msg['To'] = email_config['recipient_email']
        
        # Attach HTML content
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        try:
            # Send email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)
            
            logging.info(f"Email notification sent successfully to {email_config['recipient_email']}")
            
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
    
    def run_once(self):
        """Run one iteration of job checking"""
        logging.info("Starting job search...")
        jobs = self.scrape_linkedin_jobs()
        if not jobs:
            logging.warning("No jobs found or error occurred")
            self.save_last_run_time()
            return

        # Filter by time window
        jobs_in_window = self.filter_jobs_by_time(jobs)
        # Filter new jobs (not seen before)
        new_jobs = self.filter_new_jobs(jobs_in_window)

        if new_jobs:
            self.send_email_notification(new_jobs)
            self.save_seen_jobs()
        else:
            logging.info("No new jobs found in this time window")
        self.save_last_run_time()
    
    def run_continuous(self):
        """Run the job tracker continuously"""
        interval = self.config['monitoring']['check_interval_minutes']
        
        logging.info(f"Starting continuous monitoring (checking every {interval} minutes)")
        
        while True:
            try:
                self.run_once()
                logging.info(f"Waiting {interval} minutes until next check...")
                time.sleep(interval * 60)
                
            except KeyboardInterrupt:
                logging.info("Stopping job tracker...")
                break
            except Exception as e:
                logging.error(f"Error in continuous run: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main function"""
    tracker = LinkedInJobTracker()
    
    # Check if running in continuous mode
    if len(os.sys.argv) > 1 and os.sys.argv[1] == '--continuous':
        tracker.run_continuous()
    else:
        tracker.run_once()

if __name__ == "__main__":
    main() 