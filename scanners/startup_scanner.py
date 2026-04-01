# scanners/startup_scanner.py
import winreg

def run_startup_scan():
    results = []

    paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    ]

    for path in paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
            i = 0
            while True:
                name, value, _ = winreg.EnumValue(key, i)
                results.append({
                    "name": name,
                    "command": value
                })
                i += 1
        except OSError:
            pass

    return results