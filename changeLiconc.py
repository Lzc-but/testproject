from math import exp, sqrt
import re, os


def modify_cif_value(file_path, new_value):
    str2 = str(new_value).replace(".", "")
    file_new = os.path.splitext(file_path)[0] + str(str2) + ".cif"
    # 读取文件内容
    with open(file_path, "r") as file:
        lines = file.readlines()

    # 修改每一行的内容
    modified_lines = []
    for line in lines:
        if "Li10" in line:
            parts = line.split()
            parts[6] = str(new_value)
            new_line = " ".join(parts) + "\n"
            modified_lines.append(new_line)
            continue
        modified_lines.append(line)

    # 将修改后的内容写回文件
    with open(file_new, "w") as file:
        file.writelines(modified_lines)


def get_rij(ri, ci, rj, cj):
    Rij = ri + rj - ri * rj * (sqrt(ci) - sqrt(cj)) ** 2 / (ci * ri + cj * rj)
    return Rij


if __name__ == "__main__":
    for i in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
        Li_concen = round(i / 18, 6)
        modify_cif_value("05.cif", Li_concen)

    Rij = get_rij(1.0, 0.97, 0.63, 3.15)
    print(Rij)
