import os
import platform
import psutil
import socket
import subprocess
import cpuinfo
import GPUtil

def get_system_info():
    # Get basic system info
    system_info = {
        "Hostname": socket.gethostname(),
        "System": platform.system(),
        "Kernel": platform.release(),
        "Compiler": platform.python_compiler(),
        "CPU": cpuinfo.get_cpu_info()['brand_raw'],
        "Memory": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GiB",
        "Disk": f"{round(psutil.disk_usage('/').total / (1024**3), 2)} GiB"
    }

    # Get GPU info
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "GPU Name": gpu.name,
            "GPU Load": f"{gpu.load * 100}%",
            "GPU Free Memory": f"{gpu.memoryFree}MB",
            "GPU Used Memory": f"{gpu.memoryUsed}MB",
            "GPU Total Memory": f"{gpu.memoryTotal}MB",
            "GPU Temperature": f"{gpu.temperature} °C"
        })

    # Get RAM and Disk usage
    ram_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    
    usage_info = {
        "RAM Used": f"{round(ram_usage.used / (1024**3), 2)} GiB / {round(ram_usage.total / (1024**3), 2)} GiB ({ram_usage.percent}%)",
        "Disk Used": f"{round(disk_usage.used / (1024**3), 2)} GiB / {round(disk_usage.total / (1024**3), 2)} GiB ({disk_usage.percent}%)"
    }

    # Combine all info
    system_info.update(usage_info)
    system_info["GPU"] = gpu_info

    return system_info

def print_system_info():
    info = get_system_info()
    for key, value in info.items():
        if key == "GPU":
            print(f"{key}:")
            for gpu in value:
                for gpu_key, gpu_value in gpu.items():
                    print(f"  {gpu_key}: {gpu_value}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    print_system_info()