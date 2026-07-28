import matplotlib.pyplot as plt
import numpy as np
from ase.build import bulk
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.optimize import LBFGS
from ase.io import read
from ase.units import Ry
from pathlib import Path

atoms = read("FeAl.cif")
orig_cell = atoms.get_cell().copy()
orig_scaled_positions = atoms.get_scaled_positions().copy()
orig_volume = atoms.get_volume()
print(orig_cell)
print(orig_volume)
print(orig_scaled_positions)

pseudo_dir = "CMP_pseudos"
pseudopotentials = {"Al": "Al.pbe-n-kjpaw_psl.0.1.UPF",
                    "Fe": "Fe.pbe-spn-kjpaw_psl.0.2.1.UPF"}

# For medium precision calculations, use ecutwfc=70 Ry, ecutrho=700 Ry, k-mesh=6x4x4. For high precision calculations (which take more computer time), use ecutwfc=90 Ry, ecutrho=900 Ry, k-mesh=14x8x8. It will always be indicated when it is safe to use medium precision.

input_data = {
    'control': {
        'calculation': 'scf',       # Options: 'scf', 'relax', 'vc-relax'
        'prefix': 'FeAl',              # Prefix for input/output files
        'verbosity': 'low',
        "pseudo_dir": pseudo_dir,  # Directory for pseudopotentials
        'tprnfor': True,
        'tstress': True,
        'outdir': '.',          # Directory for scratch files
    },
    'system': {
        'ecutwfc': 70.0,            # Wavefunction cutoff in Ry
        'ecutrho': 700.0,          # Charge density cutoff in Ry
        'occupations': 'smearing',
        'smearing': 'mv',
        'degauss': 0.005,
    },
    'electrons': {
        'conv_thr': 1e-08,         # Convergence threshold
        'mixing_beta': 0.7,
    }
}
kpts = (6, 4, 4)  # k-point mesh

vol_range = [0.8,0.85,0.9,0.95,1.0]
results = {"volume": [], "energy": []}
for i, volume_factor in enumerate(vol_range):
    print(f"{i+1}/{len(vol_range)}. Volume factor: {volume_factor}")
    lin_frac = volume_factor ** (1/3)
    atoms.set_cell(orig_cell * lin_frac, scale_atoms=True)    

    run_dir = Path(f"vol_{volume_factor:.2f}")
    run_dir.mkdir(exist_ok=True)

    profile = EspressoProfile(command='pw.x', pseudo_dir=pseudo_dir)
    atoms.calc = Espresso(profile=profile, pseudopotentials=pseudopotentials,
                        kpts=kpts, input_data=input_data,
                        directory=run_dir)

    try:
        energy_eV = atoms.get_potential_energy()  # runs pw.x and parses the SCF total energy
        energy_Ry = energy_eV / Ry
        volume = atoms.get_volume()
    except Exception as e:
        print(f"Error during calculation: {e}")
        energy_Ry = None
        volume = None
    else:
        (run_dir / "espresso.err").unlink(missing_ok=True)
        (run_dir / "espresso.pwi").unlink(missing_ok=True)

    print(f"Total energy: {energy_Ry:.6f} Ry")
    print(f"Volume: {volume:.6f} A^3")
    results["volume"].append(volume)
    results["energy"].append(energy_Ry)

volumes = np.array(results["volume"])
energies = np.array(results["energy"])

plt.plot(volumes, energies, 'o-')
plt.xlabel('Volume (A^3)')
plt.ylabel('Energy (Ry)')
plt.title('Volume Optimization')
plt.show()







"""Total energy: -737.528017 Ry
Volume: 44.839734 A^3
Total energy: -737.542305 Ry
Volume: 47.642218 A^3
Total energy: -737.541999 Ry
Volume: 50.444701 A^3
Total energy: -737.530955 Ry
Volume: 53.247185 A^3
Total energy: -737.511980 Ry
Volume: 56.049668 A^3"""