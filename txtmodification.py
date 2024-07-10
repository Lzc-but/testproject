import os
import glob
import random
import numpy as np


def operate_onefile(filename):
    """
    所有数据都操作
    """
    # 读取文件内容
    with open(filename, "r") as file:
        content = file.read()

    # 查找####之后的数据
    start_index = content.index("####") + 4
    data_str = content[start_index:]

    # 将数据按空格分割成列表
    data_list = data_str.split()

    # 将数据除以1.3
    data_updated = [f"{round(float(value)/1.3,3):.3f}" for value in data_list]

    # 将更新后的数据用制表符连接
    data_updated_str = "\t".join(data_updated)

    # 将更新后的数据替换原始数据
    content_updated = content[:start_index] + data_updated_str

    # 将更新后的内容写入文件
    with open(filename, "w") as file:
        file.write(content_updated)


def operappoint_datafile(filename):
    """
    操作指定数据
    """
    # 读取文件内容
    with open(filename, "r") as file:
        content = file.read()

    # 查找####之后的数据
    start_index = content.index("####") + 4
    data_str = content[start_index:]
    # 生成在24.9到29.2之间的正态分布的随机数
    random_values = np.random.uniform(24.9, 29.2, 400)
    # 将数据按空格分割成列表
    data_list = data_str.split()
    # Generate random numbers in the specified range and round to three decimal places
    # 更新列表
    data_list[1:401] = [f"{value:.3f}" for value in random_values]
    # for i in range(1, 401):
    #     data_list[i] = format(random.uniform(24.9, 29.2), ".3f")
    # 将更新后的数据用制表符连接
    data_updated_str = "\t".join(data_list)

    # 将更新后的数据替换原始数据
    content_updated = content[:start_index] + data_updated_str

    # 将更新后的内容写入文件
    with open(filename, "w") as file:
        file.write(content_updated)


def operappoint_datafile_ascend(filename):
    """
    操作指定数据
    """
    # 读取文件内容
    with open(filename, "r") as file:
        content = file.read()

    # 查找####之后的数据
    start_index = content.index("####") + 4
    data_str = content[start_index:]
    # 将数据按空格分割成列表
    data_list = data_str.split()
    number_401 = float(data_list[401])
    number_0 = float(data_list[0])
    # 计算递增步长
    step = (number_401 - number_0) / 400
    # 生成递增数据列表并添加浮动
    random_values = [
        number_0 + i * step + random.uniform(-0.1, 0.1) for i in range(400)
    ]
    # 更新列表
    data_list[1:401] = [f"{value:.3f}" for value in random_values]
    # 将更新后的数据用制表符连接
    data_updated_str = "\t".join(data_list)

    # 将更新后的数据替换原始数据
    content_updated = content[:start_index] + data_updated_str

    # 将更新后的内容写入文件
    with open(filename, "w") as file:
        file.write(content_updated)


def update_txtdata(filename):
    # 读取文件内容
    with open(filename, "r") as file:
        content = file.read()
    start = 0.9
    end = 1.1
    num_points = 170

    coefficients = np.linspace(start, end, num_points)
    # 查找####之后的数据
    start_index = content.index("####") + 4
    data_str = content[start_index:]
    # 将数据按空格分割成列表
    data_list = data_str.split()
    # 更新列表
    result = []

    for i in range(0, len(data_list), 100):
        for j in range(100):
            if i + j < len(data_list):
                coefficient_index = i // 100 % len(coefficients)  # 根据索引取出系数
                result.append(float(data_list[i + j]) * coefficients[coefficient_index])
    ra = random.randint(0, 1)
    result = [f"{x+ra:.3f}" for x in result]  # 保留三位小数并转换为字符串
    # 将更新后的数据用制表符连接
    data_updated_str = "\t".join(result)

    # 将更新后的数据替换原始数据
    content_updated = content[:start_index] + data_updated_str

    # 将更新后的内容写入文件
    with open(filename, "w") as file:
        file.write(content_updated)


def new_txtdata(filename, i, list1):
    folder_path = "C:/Users/33389/Desktop/225operaagain/18_test2/"
    newfilename = str(list1[i]) + ".txt"
    file_path = folder_path + newfilename
    # 读取文件内容
    with open(filename, "r") as file:
        content = file.read()
    start = 0.94
    end = 1.04
    num_points = 68

    coefficients = np.linspace(start, end, num_points)
    # 查找####之后的数据
    start_index = content.index("####") + 4
    data_str = content[start_index:]
    # 将数据按空格分割成列表
    data_list = data_str.split()
    # 更新列表
    result = []

    for i in range(0, len(data_list), 250):
        for j in range(250):
            if i + j < len(data_list):
                coefficient_index = i // 250 % len(coefficients)  # 根据索引取出系数
                result.append(float(data_list[i + j]) * coefficients[coefficient_index])
    ra = random.randint(0, 1)
    result = [f"{x+ra:.3f}" for x in result]  # 保留三位小数并转换为字符串
    # 将更新后的数据用制表符连接
    data_updated_str = "\t".join(result)

    # 将更新后的数据替换原始数据
    content_updated = content[:start_index] + data_updated_str

    with open(file_path, "w") as file:
        file.write(content_updated)


def modifydata(filename, i, list1):
    folder_path = "C:/Users/33389/Desktop/225operaagain/18_test2/"
    newfilename = str(list1[i]) + ".txt"
    file_path = folder_path + newfilename
    start = 0.9
    end = 1.0
    num_points = 68

    coefficients = np.flip(np.linspace(start, end, num_points))
    # 读取文件内容
    with open(filename, "r") as file:
        content = file.read()

    # 查找####之后的数据
    start_index = content.index("####") + 4
    data_str = content[start_index:]

    # 将数据按空格分割成列表
    data_list = data_str.split()
    # 计算列表长度
    length = len(data_list)
    # 计算后半部分的起始索引
    start_index = length // 2
    # 将后半部分存储到另一个列表中
    new_list = data_list[start_index:]
    # 更新列表
    result = []

    for i in range(0, len(new_list), 100):
        for j in range(100):
            if i + j < len(new_list):
                coefficient_index = i // 100 % len(coefficients)  # 根据索引取出系数
                result.append(float(new_list[i + j]) * coefficients[coefficient_index])
    ra = random.randint(0, 1)
    result = [f"{x:.3f}" for x in result]  # 保留三位小数并转换为字符串
    # 将长列表的后半部分替换为短列表
    data_list[start_index:] = result
    # 将更新后的数据用制表符连接
    data_updated_str = "\t".join(data_list)

    # 将更新后的数据替换原始数据
    content_updated = content[:start_index] + data_updated_str
    with open(file_path, "w") as file:
        file.write(content_updated)


# 遍历文件夹中的txt文件
folder_path = r"C:\Users\33389\Desktop\225operaagain\3_5"  # 文件夹路径
list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
for i, file_path in enumerate(txt_files):
    new_txtdata(file_path, i, list1)
