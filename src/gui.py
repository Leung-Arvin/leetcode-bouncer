import os
import sys
import webbrowser
import customtkinter as ctk
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.leetcode_api import get_solved_count_today
from src.bouncer import enforce_rules

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LeetCodeBouncerApp(ctk.CTk):
    def __init__(self, config, save_config_callback):
        super().__init__()

        self.config = config
        self.save_config_callback = save_config_callback

        self.title("LeetCode Bouncer")
        self.geometry("450x500")
        self.resizable(False, False)

        self.title_label = ctk.CTkLabel(self, text="🛡️ LeetCode Bouncer", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=15)

        self.status_frame = ctk.CTkFrame(self, width=400, height=70)
        self.status_frame.pack(pady=5, padx=20, fill="x")
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Checking API...", font=ctk.CTkFont(size=16))
        self.status_label.pack(expand=True)

        self.solve_button = ctk.CTkButton(self, text="🚀 Open Blind 75 List", fg_color="#e67e22", hover_color="#d35400", command=self.open_leetcode)
        self.solve_button.pack(pady=10)

        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.pack(pady=10, padx=20, fill="x")
        
        self.username_label = ctk.CTkLabel(self.settings_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.username_entry = ctk.CTkEntry(self.settings_frame, width=200)
        self.username_entry.insert(0, self.config.get("leetcode_username", ""))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.goal_label = ctk.CTkLabel(self.settings_frame, text="Daily Goal Count:")
        self.goal_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.goal_entry = ctk.CTkEntry(self.settings_frame, width=200)
        self.goal_entry.insert(0, str(self.config.get("daily_goal", 1)))
        self.goal_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        self.save_button = ctk.CTkButton(self, text="Update Settings", command=self.update_settings)
        self.save_button.pack(pady=5)

        self.log_box = ctk.CTkTextbox(self, height=100, width=400, activate_scrollbars=True)
        self.log_box.pack(pady=15, padx=20)
        self.log_box.insert("0.0", "Account tracking online.\n")
        self.log_box.configure(state="disabled")

        self.monitor_loop()

    def open_leetcode(self):
        webbrowser.open("https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions")
        self.log_message("Opened curriculum overview.")

    def log_message(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{timestamp}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_settings(self):
        new_username = self.username_entry.get().strip()
        try:
            new_goal = int(self.goal_entry.get().strip())
            if new_goal < 1: raise ValueError
        except ValueError:
            self.log_message("Error: Goal must be a positive number.")
            return

        if new_username:
            self.config["leetcode_username"] = new_username
            self.config["daily_goal"] = new_goal
            self.save_config_callback(self.config)
            self.log_message(f"Saved! Tracking {new_username} | Daily Goal: {new_goal}")

    def monitor_loop(self):
        username = self.config["leetcode_username"]
        blocked = self.config["blocked_processes"]
        goal = self.config.get("daily_goal", 1)
        interval_ms = self.config.get("check_interval_seconds", 15) * 1000

        if not username or username == "YOUR_LEETCODE_USERNAME":
            self.status_label.configure(text="Please set your LeetCode username!", text_color="#ffcc00")
            self.status_frame.configure(fg_color="#3a3000")
        else:
            solved_today = get_solved_count_today(username)

            if solved_today >= goal:
                self.status_label.configure(text=f"✅ Goal Met ({solved_today}/{goal}). Go play!", text_color="#2ecc71")
                self.status_frame.configure(fg_color="#1e3d2f")
                enforce_rules(should_allow_gaming=True, blocked_processes=blocked)
            else:
                self.status_label.configure(text=f"❌ Progress: {solved_today}/{goal} Solved. Lock Active!", text_color="#e74c3c")
                self.status_frame.configure(fg_color="#3d1e1e")
                
                killed = enforce_rules(should_allow_gaming=False, blocked_processes=blocked)
                for proc in killed:
                    self.log_message(f"Terminated: {proc}")

        self.after(interval_ms, self.monitor_loop)