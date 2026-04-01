# scanners/system_scanner.py
import platform
import psutil
from datetime import datetime

def get_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def get_cpu_info():
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "cpu_usage_percent": psutil.cpu_percent(interval=1)
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total_memory": mem.total,
        "available_memory": mem.available,
        "used_memory": mem.used,
        "memory_usage_percent": mem.percent
    }

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_data = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            disk_data.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "total_size": usage.total,
                "used": usage.used,
                "free": usage.free,
                "usage_percent": usage.percent
            })
        except PermissionError:
            continue

    return disk_data

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    return {
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime_seconds": uptime.total_seconds()
    }

def run_system_scan():
    return {
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "uptime": get_uptime()
    }