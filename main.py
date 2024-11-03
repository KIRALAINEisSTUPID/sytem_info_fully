#  ____            _                     _        __           _           
# / ___| _   _ ___| |_ ___ _ __ ___     (_)_ __  / _| ___     | |__  _   _ 
# \___ \| | | / __| __/ _ \ '_ ` _ \    | | '_ \| |_ / _ \    | '_ \| | | |
#  ___) | |_| \__ \ ||  __/ | | | | |   | | | | |  _| (_) |   | |_) | |_| |
# |____/ \__, |___/\__\___|_| |_| |_|   |_|_| |_|_|  \___/    |_.__/ \__, |
#        |___/                                                       |___/ 
#  _  ___           _       _             
# | |/ (_)_ __ __ _| | __ _(_)_ __   ___  
# | ' /| | '__/ _` | |/ _` | | '_ \ / _ \ 
# | . \| | | | (_| | | (_| | | | | |  __/ 
# |_|\_\_|_|  \__,_|_|\__,_|_|_| |_|\___| 






import platform
import psutil
import socket
import netifaces
import os
import subprocess
from simple_term_menu import TerminalMenu  # Для меню выбора языка

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def get_system_info():
    info = {}

    # Основная информация о системе
    info['system'] = platform.system()
    info['node_name'] = platform.node()
    info['release'] = platform.release()
    info['version'] = platform.version()
    info['machine'] = platform.machine()
    info['processor'] = platform.processor()
    info['architecture'] = platform.architecture()
    info['hostname'] = socket.gethostname()
    try:
        info['ip_address'] = socket.gethostbyname(info['hostname'])
    except socket.error:
        info['ip_address'] = "Не удалось получить IP-адрес"

    # Информация о CPU
    info['cpu_count'] = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    info['cpu_freq'] = cpu_freq._asdict() if cpu_freq else "N/A"
    info['cpu_usage'] = psutil.cpu_percent(interval=1, percpu=True)

    # Использование каждого ядра
    info['cpu_usage_per_core'] = [psutil.cpu_percent(interval=1, percpu=True)]

    # Информация о памяти
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    info['memory_total'] = format_bytes(mem.total)
    info['memory_available'] = format_bytes(mem.available)
    info['memory_used'] = format_bytes(mem.used)
    info['memory_percent'] = mem.percent
    info['swap_total'] = format_bytes(swap.total)
    info['swap_used'] = format_bytes(swap.used)
    info['swap_free'] = format_bytes(swap.free)
    info['swap_percent'] = swap.percent

    # Информация о диске
    partitions = psutil.disk_partitions()
    info['disk_info'] = {}
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        info['disk_info'][partition.mountpoint] = {
            'total': format_bytes(usage.total),
            'used': format_bytes(usage.used),
            'free': format_bytes(usage.free),
            'percent': usage.percent
        }

    # Информация о сетевых интерфейсах
    interfaces = netifaces.interfaces()
    info['network_interfaces'] = {}

    for iface in interfaces:
        addresses = netifaces.ifaddresses(iface)
        iface_info = {
            'IPv4': addresses.get(netifaces.AF_INET, []),
            'IPv6': addresses.get(netifaces.AF_INET6, []),
            'MAC': addresses.get(netifaces.AF_LINK, []),
            'status': 'up' if netifaces.ifaddresses(iface) else 'down'
        }
        info['network_interfaces'][iface] = iface_info

    # Информация о соединениях
    connections = psutil.net_connections()
    info['active_connections'] = len(connections)

    # Информация о процессах
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_info', 'cpu_percent']):
        processes.append(proc.info)
    info['running_processes'] = processes

    return info

def save_system_info(info, language="english"):
    filename = "system_info.txt"
    with open(filename, "w") as file:
        if language == "english":
            file.write("System Information:\n\n")
            file.write(f"Operating System: {info['system']}\n")
            file.write(f"Node Name: {info['node_name']}\n")
            file.write(f"Release: {info['release']}\n")
            file.write(f"Version: {info['version']}\n")
            file.write(f"Architecture: {info['architecture']}\n")
            file.write(f"Hostname: {info['hostname']}\n")
            file.write(f"IP Address: {info['ip_address']}\n\n")
            file.write("CPU Information:\n")
            file.write(f"CPU Count: {info['cpu_count']}\n")
            file.write(f"CPU Frequency: {info['cpu_freq']}\n")
            file.write(f"CPU Usage: {info['cpu_usage']}\n")
            file.write(f"CPU Usage Per Core: {info['cpu_usage_per_core']}\n")
            file.write("\nMemory Information:\n")
            file.write(f"Total Memory: {info['memory_total']}\n")
            file.write(f"Available Memory: {info['memory_available']}\n")
            file.write(f"Used Memory: {info['memory_used']}\n")
            file.write(f"Memory Percent: {info['memory_percent']}%\n")
            file.write(f"Total Swap: {info['swap_total']}\n")
            file.write(f"Used Swap: {info['swap_used']}\n")
            file.write(f"Free Swap: {info['swap_free']}\n")
            file.write(f"Swap Percent: {info['swap_percent']}%\n")
            file.write("\nDisk Information:\n")
            for mountpoint, usage in info['disk_info'].items():
                file.write(f"Mountpoint: {mountpoint}, Usage: {usage}\n")
            file.write("\nNetwork Interfaces:\n")
            for iface, addr in info['network_interfaces'].items():
                file.write(f"Interface: {iface}, Addresses: {addr}\n")
            file.write(f"\nActive Connections: {info['active_connections']}\n")
            file.write("\nRunning Processes:\n")
            for process in info['running_processes']:
                file.write(f"PID: {process['pid']}, Name: {process['name']}, Status: {process['status']}, Memory: {process['memory_info']}, CPU Usage: {process['cpu_percent']}\n")

        elif language == "russian":
            file.write("Информация о системе:\n\n")
            file.write(f"ОС: {info['system']}\n")
            file.write(f"Имя узла: {info['node_name']}\n")
            file.write(f"Версия: {info['release']}\n")
            file.write(f"Полная версия: {info['version']}\n")
            file.write(f"Архитектура: {info['architecture']}\n")
            file.write(f"Имя хоста: {info['hostname']}\n")
            file.write(f"IP адрес: {info['ip_address']}\n\n")
            file.write("Информация о CPU:\n")
            file.write(f"Количество CPU: {info['cpu_count']}\n")
            file.write(f"Частота CPU: {info['cpu_freq']}\n")
            file.write(f"Использование CPU: {info['cpu_usage']}\n")
            file.write(f"Использование CPU по ядрам: {info['cpu_usage_per_core']}\n")
            file.write("\nИнформация о памяти:\n")
            file.write(f"Всего памяти: {info['memory_total']}\n")
            file.write(f"Доступно памяти: {info['memory_available']}\n")
            file.write(f"Использовано памяти: {info['memory_used']}\n")
            file.write(f"Процент использования памяти: {info['memory_percent']}%\n")
            file.write(f"Всего swap: {info['swap_total']}\n")
            file.write(f"Использовано swap: {info['swap_used']}\n")
            file.write(f"Свободно swap: {info['swap_free']}\n")
            file.write(f"Процент использования swap: {info['swap_percent']}%\n")
            file.write("\nИнформация о дисках:\n")
            for mountpoint, usage in info['disk_info'].items():
                file.write(f"Точка монтирования: {mountpoint}, Использование: {usage}\n")
            file.write("\nСетевые интерфейсы:\n")
            for iface, addr in info['network_interfaces'].items():
                file.write(f"Интерфейс: {iface}, Адреса: {addr}\n")
            file.write(f"\nАктивные соединения: {info['active_connections']}\n")
            file.write("\nРаботающие процессы:\n")
            for process in info['running_processes']:
                file.write(f"PID: {process['pid']}, Название: {process['name']}, Статус: {process['status']}, Память: {process['memory_info']}, Использование CPU: {process['cpu_percent']}\n")

def main():
    options = ["English", "Русский"]
    terminal_menu = TerminalMenu(options, title="Select Language / Выберите язык")
    choice_index = terminal_menu.show()
    selected_language = "english" if choice_index == 0 else "russian"

    system_info = get_system_info()
    save_system_info(system_info, language=selected_language)

    if selected_language == "english":
        print("System information has been saved to 'system_info.txt'.")
    else:
        print("Информация о системе сохранена в файле 'system_info.txt'.")

if __name__ == "__main__":
    try:
        import simple_term_menu  # Проверка, что модуль установлен
    except ImportError:
        subprocess.check_call(["pip", "install", "simple-term-menu"])  # Автоустановка при необходимости
    main()
