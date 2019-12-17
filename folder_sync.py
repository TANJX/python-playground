import os

# rename folders in folder B from folder A if the contents in the folders are the same
def method1():
    from_folder = 'Y:/Video/Anime/'
    to_folder = 'V:/Video/Anime/'

    from_subfolders = os.listdir(from_folder)
    to_subfolders = os.listdir(to_folder)

    for from_item in from_subfolders:
        from_item_content = os.listdir(os.path.join(from_folder, from_item))
        for to_item in to_subfolders:
            to_item_content = os.listdir(os.path.join(to_folder, to_item))
            if from_item_content == to_item_content and from_item != to_item:
                os.rename(os.path.join(to_folder, to_item), os.path.join(to_folder, from_item))
                to_subfolders = os.listdir(to_folder)
                print(from_item)
                print(to_item)
                print()
                break


# completely rearrange files in folder A according to the folder structure in folder B
def method2():
    from_folder = 'E:/Video/Anime/'
    to_folder = 'V:/Video/Anime/[1986-2013]スタジオジブリ'

    from_subfolders = os.listdir(from_folder)

    from_items_set = {}

    for from_item in from_subfolders:
        from_items_set[from_item] = []
        for file in os.listdir(os.path.join(from_folder, from_item)):
            from_items_set[from_item].append(file)
    for folder_name in from_items_set:
        path_name = os.path.join(to_folder, folder_name)
        if not os.path.exists(path_name):
            os.makedirs(path_name)
    for r, d, f in os.walk(to_folder):
        for file in f:
            for folder_name in from_items_set:
                if file in from_items_set[folder_name]:
                    print(os.path.join(r, file))
                    print(os.path.join(to_folder, folder_name, file))
                    print()
                    os.rename(os.path.join(r, file), os.path.join(to_folder, folder_name, file))


method2()
