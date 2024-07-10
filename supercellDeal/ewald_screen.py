# -*- encoding: utf-8 -*-
"""
    @File    :   supercell_cif_transify.py
    @Time    :   2024/07/3 15:49:14
    @Author  :   赖智聪 
    @Desc    :   处理Supercell生成的cif文件并通过ewald进行筛选。
"""

import os
from pymatgen.core.structure import Structure
from pymatgen.analysis.ewald import EwaldSummation
from pymatgen.io.cif import CifWriter
from typing import Dict, List, Union
from pathlib import Path
import csv

def get_atom_site_type_symbol(cif_file_path: Union[str, Path]):
    """
    获取"_atom_site_label"和"_atom_site_type_symbol"的行号
    """
    with open(cif_file_path, "r") as file:
        lines = file.readlines()
    ciffile = str(cif_file_path)
    for index, line in enumerate(lines):
        if "_atom_site_type_symbol" in line:
            _atom_site_type_symbol_index = index
        elif "_atom_site_label" in line:
            _atom_site_label_index = index
    return _atom_site_type_symbol_index, _atom_site_label_index

def modify_cif_file(cif_file_path: Union[str, Path], symbol_index: int, label_index: int):
    """
    将通过Supercell程序得到的有序结构的cif文件进行修改
    """
    with open(cif_file_path, "r") as file:
        lines = file.readlines()
    ciffile = str(cif_file_path)
    if "_atom_site_type_symbol" in lines[symbol_index] and "_atom_site_label" in lines[label_index]:
        lines[label_index], lines[symbol_index] = lines[symbol_index], lines[label_index]
    else:
        raise ValueError(
            f"in {ciffile} The lines[{label_index}] and lines[{symbol_index}] swap was not executed because '_atom_site_type_symbol' was not found in lines[76]."
        )
    with open(cif_file_path, "w") as file:
        file.writelines(lines)


def read_files_in_folder(folder_path: str):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files

def deal_SupercellCiffiles(folder_path: str):
    """
    将Supercell生成的cif文件集改为标准cif格式
    """
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    symbol_index, label_index = get_atom_site_type_symbol(files[0])
    for file in files:
        modify_cif_file(file, symbol_index, label_index)

def cal_ewald(cif_file_path: Union[str, Path]):
    """
    计算cif文件的ewald能
    """
    # 加载晶体结构
    structure = Structure.from_file(cif_file_path)

    # 创建 EwaldSummation 实例
    ewald = EwaldSummation(structure)

    # 计算 Ewald 能量
    ewald_energy = ewald.total_energy
    # print(f"{str(cif_file_path)}Ewald Energy:", ewald_energy)
    return ewald_energy

def get_ciffiles_ewald(folder_path: str):
    directory = os.path.dirname(folder_path)
    output_csv = os.path.join(directory, os.path.basename(folder_path) + "_ewald_energy.csv")
    rows = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        cif_file = Path(file_path)
        ewald_energy = cal_ewald(cif_file)
        rows.append({'filename': cif_file.name, 'Ewald energy': ewald_energy})

    # 按照'Ewald energy'从小到大排序
    sorted_rows = sorted(rows, key=lambda x: x['Ewald energy'])

    # 将排序后的结果写入CSV文件
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'Ewald energy']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(sorted_rows)

if __name__ == "__main__":
    deal_SupercellCiffiles(r"D:\warehouses\ciffile\lithium-rich-layered\p2-single(1)")
    get_ciffiles_ewald(r"D:\warehouses\ciffile\lithium-rich-layered\p2-single(1)")

