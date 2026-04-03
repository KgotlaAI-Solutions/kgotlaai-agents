#!/usr/bin/env python3
"""
Shared configuration for cloud agents
"""

import os

# Base paths for cloud environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'outputs')

# Create output directories
def ensure_dirs():
    dirs = [
        os.path.join(OUTPUT_DIR, 'leads'),
        os.path.join(OUTPUT_DIR, 'content'),
        os.path.join(OUTPUT_DIR, 'funding'),
        os.path.join(OUTPUT_DIR, 'team'),
        os.path.join(OUTPUT_DIR, 'website')
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

# Company config
COMPANY_CONFIG = {
    'company_name': 'Kgotla AI',
    'founder_name': 'Mahlo Kgotleng',
    'email': 'mahlo@kgotlaai.co.za',
    'website': 'kgotlaai.co.za',
    'linkedin_url': 'https://www.linkedin.com/in/mahlo-kgotleng-473830194',
    'funding_target': 320100,
    'equity_offered': 50
}
