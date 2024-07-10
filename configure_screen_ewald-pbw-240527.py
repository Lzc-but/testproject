from pymatgen.core.structure import Structure
from pymatgen.transformations.standard_transformations import (
    OrderDisorderedStructureTransformation,
)
from pymatgen.analysis.ewald import EwaldSummation
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import read as ase_read
import os


def asetopymatgen(file_cif):
    """
    当自强4000出现No module named '_sqlite3'时
    先通过ase读取cif文件再转为pymatgen格式的结构
    """
    atoms = ase_read(file_cif, format="cif")
    stru = AseAtomsAdaptor.get_structure(atoms)
    return stru


def configure_screen(file_cif):
    """
    file_cif混合占据的cif文件
    输出为能量最低的几个有序结构
    """
    # file = "Li1La095Ta0476Cl6-pmg_P63m.cif"
    stru = Structure.from_file(file_cif)
    trans = OrderDisorderedStructureTransformation()
    # 晶胞大、位点数多、可能性多的结构, 计算很耗时
    # 不占内存, PC可以运行. 大的结构建议放自强上慢慢算
    return_list = trans.apply_transformation(stru, return_ranked_list=10)

    # return_list是字典的列表, 从每一个字典里的'structure'可以取出Structure
    # return_list中, 以ewald静电能从低到高排列, return_list[0]是ewald能最低的构型
    strus = [i["structure"] for i in return_list]

    # 从return_list导出所有configuration, 命名时加上编号区分
    for i, dic in enumerate(return_list):
        s = dic["structure"]
        s.to(fmt="cif", filename="config_{}.cif".format(i))


def cal_ewald(file_cif):
    """
    计算cif文件的ewald能
    """
    # 加载晶体结构
    structure = Structure.from_file(file_cif)

    # 创建 EwaldSummation 实例
    ewald = EwaldSummation(structure)
    test = ewald.point_energy+ewald.real_space_energy+ewald.reciprocal_space_energy+ewald._charged_cell_energy
    # 计算 Ewald 能量
    ewald_energy = ewald.total_energy
    print(f"{str(file_cif)}Ewald Energy:", ewald_energy)


def read_files_in_folder(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


if __name__ == "__main__":
    # configure_screen(r"D:\warehouses\ciffile\Li0778La095Ta0476Cl6\pbw\LiLaTaCl-x223-spg_176_P63m-ion_num_int.cif")
    configure_screen(r"D:\warehouses\ciffile\wrf\Li2TiO3_11_18.cif")
    # files = read_files_in_folder("17_18")
    # for file in files:
    #     cal_ewald(file)
    cal_ewald(r"D:\warehouses\ciffile\wrf\7_18\7_18_i00000_w1.cif")
    # cal_ewald("7_18_i00000_w1.cif")
    # asetopymatgen("7_18_i00000_w1.cif")
    # cal_ewald("config_0.cif")
