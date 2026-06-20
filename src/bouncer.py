import sys
import psutil

# Windows UI Automation bindings
if sys.platform == "win32":
    import win32gui
    import win32con
    import win32process
    import win32com.client

def close_youtube_tabs():
    """Scans all visible desktop window titles and targets active YouTube browser tabs."""
    def window_enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            # Catch if the active tab layout matches a YouTube window signature
            if "youtube" in title:
                # Bring the browser window into focus
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                
                # Send the standard Ctrl + W shortcut code to close the current tab
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys("^w") 
    
    win32gui.EnumWindows(window_enum_callback, None)

def enforce_rules(should_allow_gaming, blocked_processes, block_games_enabled, block_youtube_enabled):
    # If daily targets are solved, bypass the safety loops entirely
    if should_allow_gaming:
        return []

    # Handle selective browser tab termination
    if block_youtube_enabled and sys.platform == "win32":
        try:
            close_youtube_tabs()
        except Exception:
            pass

    # Handle desktop process launching execution blocks
    if not block_games_enabled:
        return []
        
    killed_apps = []
    for proc in psutil.process_iter(['name']):
        try:
            process_name = proc.info['name'].lower()
            if process_name in [p.lower() for p in blocked_processes]:
                proc.kill()
                killed_apps.append(process_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed_apps