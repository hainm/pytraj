import unittest
from array import array
from pytraj.base import *
from pytraj import io as mdio
from pytraj.decorators import no_test
from pytraj.utils.check_and_assert import assert_almost_equal
from pytraj.common_actions import calc_score

class Test(unittest.TestCase):
    def test_0(self):
        IDX0 = 9 
        IDX1 = 8
        traj = mdio.load("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        # write pdb files for TMalign program so we can compare our result to TMalign
        # ./TMalign -A test_gdt_0.pdb -B test_gdt_1.pdb
        mdio.writetraj(filename="./output/test_gdt_0.pdb", traj=traj[IDX0], top=traj.top, overwrite=True)
        mdio.writetraj(filename="./output/test_gdt_1.pdb", traj=traj[IDX1], top=traj.top, overwrite=True)

        # do our calculation
        # score = 'gdtscore', 'tmscore' or 'maxsub'
        # need to add assert
        score = 'tmscore'
        print('%s = %s ' % (score, calc_score(traj[IDX0], traj[IDX1], "@CA", traj.top, score=score)))
        tmscore = calc_score(traj[IDX1], traj[IDX0], "@CA", traj.top, score=score)
        assert_almost_equal([tmscore,], [0.38941,], decimals=2) # 0.38941: from TMalign

        # calculate RMSD
        print("rmsd = ", traj[IDX0].rmsd(traj[IDX1]))

if __name__ == "__main__":
    unittest.main()
    #pass
