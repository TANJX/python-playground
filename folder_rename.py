import os

my_path = 'Y:/working/[2019.12.15]New Year/footage/1.19/audio'

folders = os.listdir(my_path)

for folder_name in folders:
    print(folder_name)
    folder = os.listdir(os.path.join(my_path, folder_name))
    for item in folder:
        if item.endswith('.hprj'):
            os.rename(os.path.join(my_path, folder_name),
                      os.path.join(my_path, folder_name + '-' + item.replace('.hprj', '')))
            break
