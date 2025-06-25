#!/usr/bin/env python3
"""
Test script for LinkedIn Job Tracker
Verifies that the tracker can connect to LinkedIn and send emails
"""

import json
import os
from linkedin_job_tracker import LinkedInJobTracker

def test_config():
    """Test if configuration file exists and is valid"""
    print("🔧 Testing configuration...")
    
    if not os.path.exists('config.json'):
        print("❌ config.json not found. Run setup.py first.")
        return False
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Check required fields
        required_fields = [
            'search_criteria.keywords',
            'search_criteria.location',
            'email.sender_email',
            'email.sender_password',
            'email.recipient_email'
        ]
        
        for field in required_fields:
            keys = field.split('.')
            value = config
            for key in keys:
                value = value.get(key)
                if value is None:
                    print(f"❌ Missing required field: {field}")
                    return False
        
        print("✅ Configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def test_linkedin_connection():
    """Test if we can connect to LinkedIn and scrape jobs"""
    print("\n🔍 Testing LinkedIn connection...")
    
    try:
        tracker = LinkedInJobTracker()
        jobs = tracker.scrape_linkedin_jobs()
        
        if jobs:
            print(f"✅ Successfully found {len(jobs)} jobs")
            print("Sample job:")
            sample_job = jobs[0]
            print(f"  Title: {sample_job['title']}")
            print(f"  Company: {sample_job['company']}")
            print(f"  Location: {sample_job['location']}")
            return True
        else:
            print("❌ No jobs found. This might be normal if no jobs match your criteria.")
            return True
            
    except Exception as e:
        print(f"❌ Error connecting to LinkedIn: {e}")
        return False

def test_email_config():
    """Test email configuration without sending"""
    print("\n📧 Testing email configuration...")
    
    try:
        tracker = LinkedInJobTracker()
        email_config = tracker.config['email']
        
        print(f"SMTP Server: {email_config['smtp_server']}")
        print(f"SMTP Port: {email_config['smtp_port']}")
        print(f"Sender: {email_config['sender_email']}")
        print(f"Recipient: {email_config['recipient_email']}")
        
        # Test SMTP connection
        import smtplib
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            print("✅ Email configuration is valid")
            return True
            
    except Exception as e:
        print(f"❌ Email configuration error: {e}")
        print("Make sure you have:")
        print("1. Enabled 2-factor authentication on your Google account")
        print("2. Generated an App Password for 'Mail'")
        print("3. Used the App Password (not your regular password)")
        return False

def test_search_url():
    """Test the search URL generation"""
    print("\n🔗 Testing search URL generation...")
    
    try:
        tracker = LinkedInJobTracker()
        url = tracker.build_search_url()
        print(f"Generated URL: {url}")
        print("✅ Search URL generated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error generating search URL: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 LinkedIn Job Tracker Test Suite")
    print("=" * 40)
    
    tests = [
        test_config,
        test_search_url,
        test_linkedin_connection,
        test_email_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your job tracker is ready to use.")
        print("\nNext steps:")
        print("1. Run once: python linkedin_job_tracker.py")
        print("2. Run continuously: python linkedin_job_tracker.py --continuous")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the tracker.")
        print("\nCommon fixes:")
        print("- Run setup.py to configure the tracker")
        print("- Check your Gmail app password")
        print("- Verify your job search criteria")

if __name__ == "__main__":
    main() 