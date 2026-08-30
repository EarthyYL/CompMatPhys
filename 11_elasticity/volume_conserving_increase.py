"""
Apply a volume conserving increase of <k> to the c/a ratio in an HCP system
Verifies that the volume is indeed conserved
"""
import numpy as np
from ase.io import read

atoms = read("/home/yluo/CompMatPhys/11_elasticity/9011704.cif")
orig_cell = atoms.get_cell().copy()
scaled_positions = atoms.get_scaled_positions()
old_V = atoms.get_volume()

k = 1.02 # scaleup factor
axis_lengths = orig_cell.lengths()

factors = np.array([k**(-1/3),k**(-1/3),k**(2/3)])

new_lengths = axis_lengths * factors
new_cell = orig_cell.copy()
new_cell[0] *= new_lengths[0] / axis_lengths[0]
new_cell[1] *= new_lengths[1] / axis_lengths[1]
new_cell[2] *= new_lengths[2] / axis_lengths[2]
atoms.set_cell(new_cell, scale_atoms=True)
new_V = atoms.get_volume()
assert np.isclose(old_V, new_V)

print(f"Old: {axis_lengths}")
print(f"New: {new_lengths}")