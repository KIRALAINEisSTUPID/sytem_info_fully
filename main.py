import platform
import psutil
import socket
import netifaces  # Для получения более детализированной информации о сетевых интерфейсах

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
    info['ip_address'] = socket.gethostbyname(info['hostname'])

    # Информация о CPU
    info['cpu_count'] = psutil.cpu_count(logical=True)
    info['cpu_freq'] = psutil.cpu_freq()._asdict()
    info['cpu_usage'] = psutil.cpu_percent(interval=1, percpu=True)

    # Информация о памяти
    mem = psutil.virtual_memory()
    info['memory_total'] = mem.total
    info['memory_available'] = mem.available
    info['memory_used'] = mem.used
    info['memory_percent'] = mem.percent

    # Информация о диске
    disk = psutil.disk_usage('/')
    info['disk_total'] = disk.total
    info['disk_used'] = disk.used
    info['disk_free'] = disk.free
    info['disk_percent'] = disk.percent

    # Информация о сетевых интерфейсах
    interfaces = netifaces.interfaces()
    info['network_interfaces'] = {}

    for iface in interfaces:
        addresses = netifaces.ifaddresses(iface)
        info['network_interfaces'][iface] = {
            'IPv4': addresses.get(netifaces.AF_INET, []),
            'IPv6': addresses.get(netifaces.AF_INET6, []),
            'MAC': addresses.get(netifaces.AF_LINK, [])
        }

    # Информация о процессах
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        processes.append(proc.info)
    info['running_processes'] = processes

    return info

def save_system_info(info):
    with open("system_info.txt", "w") as file:
        # Добавление заголовка
        file.write("Информация о системе:\n\n")
        
        # Основная информация о системе
        file.write("Основная информация:\n")
        file.write(f"ОС: {info['system']} - Операционная система\n")
        file.write(f"Имя узла: {info['node_name']} - Имя устройства в сети\n")
        file.write(f"Версия: {info['release']} - Версия операционной системы\n")
        file.write(f"Полная версия: {info['version']} - Полная версия операционной системы\n")
        file.write(f"Архитектура: {info['architecture']} - Архитектура процессора\n")
        file.write(f"Имя хоста: {info['hostname']} - Имя хоста устройства\n")
        file.write(f"IP адрес: {info['ip_address']} - Локальный IP адрес\n\n")

        # Информация о CPU
        file.write("Информация о CPU:\n")
        file.write(f"Количество ядер: {info['cpu_count']} - Общее количество ядер процессора\n")
        file.write(f"Частота: {info['cpu_freq']} - Текущая частота процессора\n")
        file.write(f"Загрузка CPU: {info['cpu_usage']} - Загруженность CPU (в %)\n\n")

        # Информация о памяти
        file.write("Информация о памяти:\n")
        file.write(f"Объем памяти: {info['memory_total']} - Общая память (в байтах)\n")
        file.write(f"Доступно: {info['memory_available']} - Доступная память (в байтах)\n")
        file.write(f"Используется: {info['memory_used']} - Используемая память (в байтах)\n")
        file.write(f"Загрузка памяти: {info['memory_percent']}% - Загруженность памяти (в %)\n\n")

        # Информация о диске
        file.write("Информация о диске:\n")
        file.write(f"Объем диска: {info['disk_total']} - Общий объем диска (в байтах)\n")
        file.write(f"Используется: {info['disk_used']} - Используемый объем диска (в байтах)\n")
        file.write(f"Свободно: {info['disk_free']} - Свободный объем диска (в байтах)\n")
        file.write(f"Загрузка диска: {info['disk_percent']}% - Загруженность диска (в %)\n\n")

        # Информация о сетевых интерфейсах
        file.write("Информация о сетевых интерфейсах:\n")
        for iface, addresses in info['network_interfaces'].items():
            file.write(f"{iface}:\n")
            file.write(f"  IPv4: {addresses['IPv4']} - IPv4 адреса\n")
            file.write(f"  IPv6: {addresses['IPv6']} - IPv6 адреса\n")
            file.write(f"  MAC: {addresses['MAC']} - MAC адрес\n")
        file.write("\n")

        # Информация о процессах
        file.write("Запущенные процессы:\n")
        for process in info['running_processes']:
            file.write(f"  PID: {process['pid']} - {process['name']} (Статус: {process['status']})\n")

if __name__ == "__main__":
    system_info = get_system_info()
    
    # Вывод информации в терминал
    for key, value in system_info.items():
        print(f"{key}: {value}")

    # Сохранение информации в файл
    save_system_info(system_info)
