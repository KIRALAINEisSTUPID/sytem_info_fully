# System Information Script

---

## English

### Description
This Python script gathers system details (CPU, memory, disk, network interfaces, and processes) and saves them to `system_info.txt`.

### Usage
1. Install `psutil` and `netifaces`.
2. Run the script to display and save system info in `system_info.txt`.

### Functions
- `format_bytes(size)`: Converts bytes to readable units.
- `get_system_info()`: Collects system details.
- `save_system_info(info)`: Saves info to `system_info.txt`.

---

## Русский

### Описание
Скрипт на Python собирает информацию о системе (процессор, память, диск, сетевые интерфейсы и процессы) и сохраняет её в `system_info.txt`.

### Использование
1. Установите `psutil` и `netifaces`.
2. Запустите скрипт для вывода и сохранения информации в `system_info.txt`.

### Функции
- `format_bytes(size)`: Конвертирует байты в удобный формат.
- `get_system_info()`: Собирает информацию о системе.
- `save_system_info(info)`: Сохраняет информацию в `system_info.txt`.
