from pymatgen.analysis.ewald import EwaldSummation
from pymatgen.core.structure import Structure

stru = Structure.from_file("Li2TiO3_11_18.cif")
s = Structure.from_sites(stru)
matrix = EwaldSummation(s).total_energy_matrix

print(sum(sum(matrix)))