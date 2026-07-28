from ase.calculators.espresso import Espresso, EspressoProfile
from ase.io import read
from ase.units import Ry
from pathlib import Path


name = "NaCl_Full"
result_file = ("10_bonding" / Path("results.csv")).resolve()
cif_path = ("10_bonding" / Path(f"{name}.cif")).resolve()
atoms = read(f"{cif_path}")

pseudo_dir = str((Path(".") / "10_bonding").resolve())
pseudopotentials = {"Al": "Al.pbe-n-kjpaw_psl.1.0.0.UPF",
                    "Fe": "Fe.pbe-spn-kjpaw_psl.0.2.1.UPF",
                    "Cl": "Cl.pbe-n-kjpaw_psl.0.1.UPF",
                    "Na": "Na.pbe-spn-kjpaw_psl.0.2.UPF",
                    "Ge": 'ge_pbe_v1.4.uspp.F.UPF'}

input_data = {
    'control': {
        'calculation': 'scf',       # Options: 'scf', 'relax', 'vc-relax'
        'prefix': f'{name}',              # Prefix for input/output files
        'verbosity': 'low',
        "pseudo_dir": pseudo_dir,  # Directory for pseudopotentials
        'tprnfor': True,
        'tstress': True,
        'outdir': '.',          # Directory for scratch files
    },
    'system': {
        'ecutwfc': 60.0,            # Wavefunction cutoff in Ry
        'ecutrho': 360.0,          # Charge density cutoff in Ry
        'occupations': 'smearing',
        'smearing': 'mv',
        'degauss': 0.005,
    },
    'electrons': {
        'conv_thr': 1e-08,         # Convergence threshold
        'mixing_beta': 0.7,
    }
}
kpts = (7,7,7)  # k-point mesh

run_dir = "10_bonding" / Path(f"{name}")
run_dir.mkdir(exist_ok=True)

profile = EspressoProfile(command='pw.x', pseudo_dir=pseudo_dir)
atoms.calc = Espresso(profile=profile, pseudopotentials=pseudopotentials,
                    kpts=kpts, input_data=input_data,
                    directory=run_dir)

energy = atoms.get_potential_energy() / Ry / len(atoms)  # Ry per atom, so cells with different nat compare directly

with result_file.open("a") as f:
    f.write(f"{name},{energy}\n")
