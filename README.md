# LeetCode Bouncer
An automated desktop productivity engine that monitors your public LeetCode activity and restricts access to gaming launchers until you meet your daily algorithmic problem-solving goals.

## Key Features
Real-time LeetCode API Syncing: Leverages LeetCode's public GraphQL infrastructure to trace your profile activity automatically.

Automated Process Enforcement: Actively monitors background execution layers and terminates unauthorized gaming launchers if your daily constraints are unfulfilled.

Daily Automation Reset: Evaluation frames resolve via local system calendar parameters, naturally resetting problem metrics to 0 at midnight.

Robust CI/CD Gatekeeping: Integrated GitHub Actions workflow to run regression testing, syntax compilation verification, and static linting rules on every Pull Request.

## Project Architecture
Plaintext
leetcode-bouncer/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline layout
├── src/
│   ├── main.py             # Script bootstrap entry point
│   ├── gui.py              # CustomTkinter dashboard engine
│   ├── bouncer.py          # Operating system process supervisor
│   └── leetcode_api.py     # LeetCode GraphQL request driver
├── config.json             # Core profile configurations
└── requirements.txt        # Third-party package dependencies

## Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/YOUR_GITHUB_USERNAME/leetcode-bouncer.git
cd leetcode-bouncer
2. Configure Dependencies
Install the required system and library frameworks.

On Windows:

Bash
pip install -r requirements.txt
On Linux (Ubuntu/Debian):

Bash
sudo apt-get update && sudo apt-get install -y python3-tk tk-dev libx11-dev
pip install -r requirements.txt
3. Initialize Environment Variables
Open config.json in your root directory and map out your execution parameters:

JSON
{
  "leetcode_username": "Leung-Arvin" // Replace mine with your username,
  "check_interval_seconds": 15,
  "daily_goal": 1,
  "blocked_processes": [
    "steam.exe",
    "riotclientservices.exe",
    "epicgameslauncher.exe",
    "battle.net.exe"
  ]
}
Important: Ensure your LeetCode account privacy settings allow Recent Submissions to be visible to the public profile engine so the API layer can parse your data.

### Usage
To run the application manually from your root terminal shell environment:

Bash
python -m src.main
Run on Startup Configuration (Windows)
Press Win + R, type shell:startup, and hit Enter.

Right-click inside the directory space and select New -> Shortcut.

Point the target location to your Python background runtime wrapper:

DOS
"C:\Python312\pythonw.exe" "C:\path\to\leetcode-bouncer\src\main.py"
(Using pythonw.exe ensures the program initializes without bringing up an empty command line console block).

## Automated Regression Testing
To verify structural changes or additions locally without spinning up a full GUI window context, execute the internal unit testing matrix:

Bash
python -m unittest discover -s src -p "test_*.py"
Plaintext
Ran 2 tests in 0.002s
OK
