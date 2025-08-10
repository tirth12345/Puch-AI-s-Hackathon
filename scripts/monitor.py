#!/usr/bin/env python3
"""
Monitoring and analytics for Puch AI + Health Buddy
"""

import os
import time
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List

logger = logging.getLogger(__name__)

class HealthMonitor:
    """Application health monitoring"""

    def __init__(self, app_url: str = "http://localhost:5000"):
        self.app_url = app_url
        self.metrics = {
            'uptime_checks': 0,
            'failed_checks': 0,
            'response_times': [],
            'last_check': None
        }

    def check_health(self) -> Dict:
        """Perform health check"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.app_url}/health", timeout=10)
            response_time = time.time() - start_time

            self.metrics['uptime_checks'] += 1
            self.metrics['response_times'].append(response_time)
            self.metrics['last_check'] = datetime.now().isoformat()

            # Keep only last 100 response times
            if len(self.metrics['response_times']) > 100:
                self.metrics['response_times'].pop(0)

            return {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_code': response.status_code,
                'response_time': response_time,
                'timestamp': self.metrics['last_check']
            }

        except Exception as e:
            self.metrics['failed_checks'] += 1
            self.metrics['last_check'] = datetime.now().isoformat()

            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': self.metrics['last_check']
            }

    def get_metrics(self) -> Dict:
        """Get monitoring metrics"""
        avg_response_time = (
            sum(self.metrics['response_times']) / len(self.metrics['response_times'])
            if self.metrics['response_times'] else 0
        )

        uptime_percentage = (
            (self.metrics['uptime_checks'] / 
             (self.metrics['uptime_checks'] + self.metrics['failed_checks']) * 100)
            if (self.metrics['uptime_checks'] + self.metrics['failed_checks']) > 0 else 100
        )

        return {
            'uptime_checks': self.metrics['uptime_checks'],
            'failed_checks': self.metrics['failed_checks'],
            'uptime_percentage': uptime_percentage,
            'average_response_time': avg_response_time,
            'last_check': self.metrics['last_check']
        }

def run_monitoring_loop():
    """Run continuous monitoring"""
    monitor = HealthMonitor()

    print("🔍 Starting Puch AI + Health Buddy monitoring...")

    while True:
        try:
            # Health check
            health_status = monitor.check_health()
            print(f"Health check: {health_status['status']} - {health_status.get('response_time', 0):.2f}s")

            # Get metrics every 10 checks
            if monitor.metrics['uptime_checks'] % 10 == 0:
                metrics = monitor.get_metrics()
                print(f"Uptime: {metrics['uptime_percentage']:.1f}% | Avg response: {metrics['average_response_time']:.2f}s")

            time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            time.sleep(60)

if __name__ == '__main__':
    run_monitoring_loop()
