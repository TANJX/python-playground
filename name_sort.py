from xpinyin import Pinyin


def my_function(lis):  # 输入一个名字的列表
    pin = Pinyin()
    result = []
    for item in lis:
        result.append((pin.get_pinyin(item), item))
    result.sort()
    for i in range(len(result)):
        result[i] = result[i][1]
    result = '\n'.join(result)  # 将排好序的结果使用空格连接，方便输出
    print(result)  # 输出结果


name_list = []

while True:
    name = input()
    if name == 'e':
        break
    name_list.append(name)

my_function(name_list)
