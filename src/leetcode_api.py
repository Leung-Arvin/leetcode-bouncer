import requests
from datetime import datetime

def get_solved_count_today(username):
    url = "https://leetcode.com/graphql"
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        timestamp
      }
    }
    """
    variables = {"username": username, "limit": 20}
    
    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json()
        submissions = data.get("data", {}).get("recentAcSubmissionList", [])
        
        if not submissions: 
            return 0
        
        today = datetime.now().date()
        solved_today = 0
        
        for sub in submissions:
            sub_date = datetime.fromtimestamp(int(sub["timestamp"])).date()
            if sub_date == today:
                solved_today += 1
                
        return solved_today
        
    except Exception:
        return 0