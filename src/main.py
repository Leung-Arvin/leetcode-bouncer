import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui import LeetCodeBouncerApp

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config_data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config_data, f, indent=2)

def main():
    config = load_config()
    app = LeetCodeBouncerApp(config, save_config)
    app.mainloop()

if __name__ == "__main__":
    main()