import os
import sys
import unittest
from unittest.mock import patch

# Ensure paths align with project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.leetcode_api import get_solved_count_today
from src.bouncer import enforce_rules

class TestLeetCodeBouncerRegressions(unittest.TestCase):

    @patch('requests.post')
    def test_leetcode_api_handles_zero_submissions(self, mock_post):
        """Regression Test: Ensure API correctly outputs 0 when user has zero daily submissions"""
        mock_post.return_value.json.return_value = {"data": {"recentAcSubmissionList": []}}
        
        result = get_solved_count_today("TestUser")
        self.assertEqual(result, 0)

    def test_bouncer_allows_gaming_when_flag_is_true(self):
        """Regression Test: Ensure no apps are terminated when gaming privileges are active"""
        blocked_list = ["steam.exe", "riotclientservices.exe"]
        # If should_allow_gaming is True, it should exit instantly returning an empty list
        killed = enforce_rules(should_allow_gaming=True, blocked_processes=blocked_list)
        self.assertEqual(killed, [])

if __name__ == '__main__':
    unittest.main()