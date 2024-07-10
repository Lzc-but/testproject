import pandas as pd
import os


def dealcsv(file_csv):
    """
    将csv文件按照标题的不同进行分组保存
    """
    # 读取csv文件，假设分隔符是逗号
    df = pd.read_csv(file_csv, delimiter=",")
    directory = os.path.dirname(file_csv)
    # 打印列名以检查是否有 'filename' 列
    print(df.columns)

    # 确定 'filename' 列名无误后，继续处理
    if "filename" in df.columns:
        # 提取filename的前面字段作为新的一列
        df["category"] = df["filename"].str.extract(r"(\d+_\d+)_")

        # 根据category分组
        grouped = df.groupby("category")

        # 将分组后的数据保存到不同的csv文件中
        for group_name, group_df in grouped:
            output_file_path = os.path.join(directory, f"{group_name}.csv")
            group_df.to_csv(output_file_path, index=False, sep=",")
    else:
        print("Error: 'filename' column not found in the CSV file.")


def csv_sorted(file_csv):
    """
    按照csv文件标题为"energy"进行排序并保存在一个新的csv文件中
    """
    # 提取文件名部分
    file_name = os.path.basename(file_csv)
    # 获取文件名中除去扩展名后的部分
    file_name_without_extension = os.path.splitext(file_name)[0]
    newfilename = "sorted_" + str(file_name_without_extension) + ".csv"
    df = pd.read_csv(file_csv)
    sorted_df = df.sort_values(by="energy")
    directory = os.path.dirname(file_csv)
    output_file_path = os.path.join(directory, newfilename)
    sorted_df.to_csv(output_file_path, index=False)


def read_files_in_folder(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


if __name__ == "__main__":
    # dealcsv(r"D:\warehouses\ciffile\wrf\ewald_energy.csv")
    # print("ss")
    files = read_files_in_folder(r"D:\warehouses\ciffile\wrf\result_new")
    for index, file in enumerate(files):
        csv_sorted(file)
