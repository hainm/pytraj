import pytraj as pt

traj = pt.iterload("../tests/data/md1_prod.Tc5b.x", "../tests/data/Tc5b.top")
top = traj.top

# get indices of CA atoms
print(pt.select_atoms(top, "@CA"))

# see how many H atoms
print(pt.select_atoms(top, "@H="))
