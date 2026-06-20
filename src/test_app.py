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
        """Regression Test: Ensure API outputs 0 when user has zero daily submissions"""
        mock_post.return_value.json.return_value = {"data": {"recentAcSubmissionList": []}}
        
        result = get_solved_count_today("TestUser")
        self.assertEqual(result, 0)

    def test_bouncer_skips_everything_when_goal_met(self):
        """Regression Test: Ensure rules exit immediately if should_allow_gaming is True"""
        blocked_list = ["steam.exe"]
        killed = enforce_rules(
            should_allow_gaming=True, 
            blocked_processes=blocked_list, 
            block_games_enabled=True, 
            block_youtube_enabled=True
        )
        self.assertEqual(killed, [])

    def test_bouncer_bypasses_games_when_toggle_is_disabled(self):
        """Regression Test: Ensure launchers aren't killed if block_games toggle is turned off"""
        blocked_list = ["steam.exe"]
        killed = enforce_rules(
            should_allow_gaming=False, 
            blocked_processes=blocked_list, 
            block_games_enabled=False, 
            block_youtube_enabled=False
        )
        self.assertEqual(killed, [])

if __name__ == '__main__':
    unittest.main()