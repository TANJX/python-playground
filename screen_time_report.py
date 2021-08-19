import os
import re

DATA_FOLDER = "data/screen/"
DATA_EXPORT_FILE = "data/screen/json/"

if __name__ == "__main__":
    data = {}
    data_app = {}
    for file in os.listdir(DATA_FOLDER):
        x = re.search(r"^\d{4}-\d{2}-\d{2}\.txt$", file)
        if x is None or x.group() != file:
            continue
        date = file.replace('.txt', '')
        data[date] = {}
        data_app[date] = {}
        f = open(DATA_FOLDER + file, 'r')
        for line in f.readlines():
            part = line.split(',')
            hour = part[0]
            minute = part[1]
            app = part[2]
            moved = int(part[3])
            if hour not in data[date]:
                data[date][hour] = {}
            data[date][hour][minute] = {
                'app': app,
                'moved': moved
            }
        f.close()
        total = 0
        active = 0
        data_app[date]['app'] = {}
        for hour in data[date]:
            for minute in data[date][hour]:
                app = data[date][hour][minute]['app']
                moved = data[date][hour][minute]['moved']
                if app not in data_app[date]['app']:
                    data_app[date]['app'][app] = {'total': 0, 'active': 0}
                data_app[date]['app'][app]['total'] += 1
                total += 1
                if moved == 1:
                    data_app[date]['app'][app]['active'] += 1
                    active += 1
        data_app[date]['active'] = active
        data_app[date]['total'] = total

    print(data)

    e = open(DATA_EXPORT_FILE + 'data.js', 'w')
    e.write('const data = ' + str(data))
    e.close()

    e = open(DATA_EXPORT_FILE + 'time_app.js', 'w')
    e.write('const time_app = ' + str(data_app))
    e.close()
