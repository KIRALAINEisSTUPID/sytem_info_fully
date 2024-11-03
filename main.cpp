#include <iostream>
#include <cstdio>  // для popen() и pclose()

int main() {
    std::string command = "shutdown 0";
    FILE* pipe = popen(command.c_str(), "r");

    if (!pipe) {
        std::cerr << "Ошибка при открытии pipe!" << std::endl;
        return 1;
    }

    char buffer[128];
    std::string result = "";

    // Чтение данных из pipe
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result += buffer;
    }

    // Закрытие pipe
    pclose(pipe);

    std::cout << "Вывод команды:\n" << result << std::endl;
    return 0;
}
