from ase.io import read, write

atoms = read("vc_relax/espresso.pwo", index=-1)
write("vc_relax/FeAl_relaxed.cif", atoms)
