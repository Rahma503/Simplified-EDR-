import psutil, shutil, os

def kill_process(pid):
    try:
        psutil.Process(pid).kill()
        return True
    except Exception:
        return False

def quarantine_file(path):
    os.makedirs("quarantine", exist_ok=True)
    try:
        dest = os.path.join("quarantine", os.path.basename(path) + ".quarantined")
        shutil.move(path, dest)
        return dest
    except Exception:
        return None