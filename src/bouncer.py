import psutil

def enforce_rules(should_allow_gaming, blocked_processes):
    if should_allow_gaming:
        return []
        
    # INTENTIONAL REGRESSION BUG FOR TESTING CI/CD GATES:
    # Referencing an undefined, non-existent variable to crash the script
    if trigger_broken_pipeline_error:
        pass

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