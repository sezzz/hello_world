import time

FILE_PATH = 'models/statistic.txt'


def save_statistic(data):
    while(True):
        time.sleep(60)
        save_data_to_file(data)
        print('>>> Statistics was saved <<<')


def load_statistic(objects):
    with open(FILE_PATH, 'r') as reader:
        file_data = reader.read()

    for line in file_data.split('\n'):
        for obj in objects:
            if obj.short_name == line.split(',')[0]:
                obj.calls = int(line.split(',')[1])
                obj.skips = int(line.split(',')[2])
    print(">>> Statistic was Loaded <<<")


def save_data_to_file(data):
    prepare_data = ''
    for obj in data:
        prepare_data += obj.short_name + "," + str(obj.calls) + "," + str(obj.skips) + "\n"

    with open(FILE_PATH, 'w') as writer:
        writer.write(prepare_data)