from pymatgen.core.structure import Structure
from pymatgen.analysis.bond_valence import BVAnalyzer
import os
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import read as ase_read
from pymatgen.transformations.standard_transformations import (
    OrderDisorderedStructureTransformation,
)
from pymatgen.analysis.ewald import EwaldSummation
import time


def asetopymatgen(file_cif):
    """
    当自强4000出现No module named '_sqlite3'时
    先通过ase读取cif文件再转为pymatgen格式的结构
    """
    atoms = ase_read(file_cif, format="cif")
    stru = AseAtomsAdaptor.get_structure(atoms)
    return stru


def formatcif(file):
    """
    通过pymatgen将不规则的cif文件转换为规则的cif文件
    """
    stru = Structure.from_file(file)
    stru.to(fmt="cif", filename=file)


def get_p1cif(file):
    """
    通过pymatgen得到p1空间群的cif文件格式
    """
    file_new = os.path.splitext(file)[0] + "p1.cif"
    stru = Structure.from_file(file)
    stru.to(fmt="cif", filename=file_new)


def get_supercell(file):
    """
    通过pymatgen括胞
    """
    stru = Structure.from_file(file)
    stru.make_supercell([2, 2, 3])
    stru.to(fmt="cif", filename=file)


def get_valence(ciffile):
    """
    通过pymatgen得到cif文件中离子化合价
    """
    # 键价法
    stru = Structure.from_file(ciffile)
    bv = BVAnalyzer()
    valences = bv.get_valences(stru)
    stru.add_oxidation_state_by_site(valences)
    stru_oxi = bv.get_oxi_state_decorated_structure(stru)
    print(stru_oxi)
    stru = Structure.from_file(ciffile)

    # 排列组合
    # stru.add_oxidation_state_by_guess()
    # for site in stru.sites:
    #     element = site.specie.element
    #     oxidation_state = site.specie.oxi_state
    #     print(f"Element:{element},Oxidation State:{oxidation_state}")
    print("ss")


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
    return_list = trans.apply_transformation(stru, return_ranked_list=100)

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

    # 计算 Ewald 能量
    ewald_energy = ewald.total_energy
    print(f"{str(file_cif)}Ewald Energy:", ewald_energy)


if __name__ == "__main__":
    get_p1cif("icsd_282.cif")
    # formatcif("O3_R3m.cif")
    get_valence("O3_R3m.cif")
    # get_supercell("Li1La095Ta0476Cl6-pmg_P63m.cif")
    # get_valence(r"D:\warehouses\ciffile\wrf\Li2TiO3.cif")
    # formatcif("05.cif")
    # get_p1cif("Ca2Al2SiO7.cif")
    start_time = time.time()
    cal_ewald(r"D:\warehouses\ciffile\wrf\11_18\11_18_i00004_w1.cif")
    end_time = time.time()
    exe_time = end_time - start_time
    print(exe_time)
