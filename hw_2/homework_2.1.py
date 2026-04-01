import sys


def get_summary_rss(file_path):
    total_rss_kb = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[1:]

            for line in lines:
                columns = line.split()
                if len(columns) >= 6:
                    try:
                        rss_kb = int(columns[5])
                        total_rss_kb += rss_kb
                    except ValueError:
                        continue

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        return None

    return format_bytes(total_rss_kb * 1024)


def format_bytes(bytes_value):
    if bytes_value == 0:
        return "0 Б"

    units = ['Б', 'KiB', 'MiB', 'GiB', 'TiB']
    unit_index = 0
    value = float(bytes_value)

    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1

    return f"{value:.2f} {units[unit_index]}"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'output_file.txt'

    result = get_summary_rss(file_path)
    if result:
        print(f"Суммарная память: {result}")