#!/usr/bin/env python3
"""
Setup script for LinkedIn Job Tracker
Helps users configure the job tracker with their preferences
"""

import json
import os
import sys
from getpass import getpass

def create_config():
    """Interactive configuration setup"""
    print("🚀 LinkedIn Job Tracker Setup")
    print("=" * 40)
    
    config = {
        "search_criteria": {},
        "email": {},
        "monitoring": {}
    }
    
    # Job search criteria
    print("\n📋 Job Search Criteria:")
    print("-" * 20)
    
    # Keywords
    keywords_input = input("Enter job keywords (comma-separated, e.g., 'python developer, software engineer'): ")
    config["search_criteria"]["keywords"] = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    # Location
    location = input("Enter location (e.g., 'United States', 'New York'): ").strip()
    config["search_criteria"]["location"] = location if location else "United States"
    
    # Experience level
    print("\nExperience levels available:")
    levels = ["Entry level", "Associate", "Mid-senior", "Director", "Executive"]
    for i, level in enumerate(levels, 1):
        print(f"{i}. {level}")
    
    exp_input = input("Enter experience levels (comma-separated numbers, e.g., '1,2'): ")
    try:
        exp_indices = [int(x.strip()) - 1 for x in exp_input.split(",") if x.strip()]
        config["search_criteria"]["experience_level"] = [levels[i] for i in exp_indices if 0 <= i < len(levels)]
    except:
        config["search_criteria"]["experience_level"] = ["Entry level", "Associate"]
    
    # Job type
    print("\nJob types available:")
    job_types = ["Full-time", "Part-time", "Contract", "Temporary", "Internship"]
    for i, job_type in enumerate(job_types, 1):
        print(f"{i}. {job_type}")
    
    job_input = input("Enter job types (comma-separated numbers, e.g., '1'): ")
    try:
        job_indices = [int(x.strip()) - 1 for x in job_input.split(",") if x.strip()]
        config["search_criteria"]["job_type"] = [job_types[i] for i in job_indices if 0 <= i < len(job_types)]
    except:
        config["search_criteria"]["job_type"] = ["Full-time"]
    
    # Remote work
    remote = input("Include remote jobs? (y/n): ").lower().strip()
    config["search_criteria"]["remote"] = remote in ['y', 'yes']
    
    # Email configuration
    print("\n📧 Email Configuration:")
    print("-" * 20)
    
    config["email"]["smtp_server"] = "smtp.gmail.com"
    config["email"]["smtp_port"] = 587
    
    sender_email = input("Enter your Gmail address: ").strip()
    config["email"]["sender_email"] = sender_email
    
    print("\n⚠️  IMPORTANT: You need to set up Gmail App Password:")
    print("1. Go to your Google Account settings")
    print("2. Enable 2-factor authentication")
    print("3. Generate an App Password for 'Mail'")
    print("4. Copy the 16-character password")
    
    sender_password = getpass("Enter your Gmail app password: ")
    config["email"]["sender_password"] = sender_password
    
    recipient_email = input("Enter email address to receive notifications: ").strip()
    config["email"]["recipient_email"] = recipient_email if recipient_email else sender_email
    
    # Monitoring configuration
    print("\n⏰ Monitoring Configuration:")
    print("-" * 20)
    
    interval = input("Check for new jobs every X minutes (default: 30): ").strip()
    try:
        config["monitoring"]["check_interval_minutes"] = int(interval) if interval else 30
    except:
        config["monitoring"]["check_interval_minutes"] = 30
    
    max_jobs = input("Maximum jobs per notification (default: 10): ").strip()
    try:
        config["monitoring"]["max_jobs_per_notification"] = int(max_jobs) if max_jobs else 10
    except:
        config["monitoring"]["max_jobs_per_notification"] = 10
    
    return config

def save_config(config, filename="config.json"):
    """Save configuration to file"""
    with open(filename, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\n✅ Configuration saved to {filename}")

def main():
    """Main setup function"""
    try:
        config = create_config()
        save_config(config)
        
        print("\n🎉 Setup Complete!")
        print("\nNext steps:")
        print("1. Test the configuration:")
        print("   python linkedin_job_tracker.py")
        print("\n2. For continuous monitoring:")
        print("   python linkedin_job_tracker.py --continuous")
        print("\n3. For GitHub Actions setup, see README.md")
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 