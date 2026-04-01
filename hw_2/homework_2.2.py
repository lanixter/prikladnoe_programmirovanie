import sys


def get_mean_size(lines):
    total_size = 0
    file_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        columns = line.split()
        if len(columns) >= 5:
            try:
                size = int(columns[4])
                total_size += size
                file_count += 1
            except ValueError:
                continue

    if file_count == 0:
        return 0

    return total_size / file_count


if __name__ == '__main__':
    lines = sys.stdin.readlines()[1:]

    mean_size = get_mean_size(lines)
    print(f"Средний размер файла: {mean_size:.2f} байт")