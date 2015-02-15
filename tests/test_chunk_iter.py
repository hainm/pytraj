import unittest
from pytraj import *
from pytraj.base import *
from pytraj.common_actions import calc_distance
from pytraj import io as mdio
from pytraj.utils.check_and_assert import assert_almost_equal

class Test(unittest.TestCase):
    def test_0(self):
        dslist = DataSetList()
        traj = mdio.load("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        #trajlist = (traj, traj.chunk_iter(chunk=2))
        #trajlist = (traj, traj[:])
        trajlist = traj
        calc_distance = adict['distance']
        calc_distance(":2@CA :10@CA", trajlist, traj.top, dslist=dslist)
        print (dslist[0].size)

if __name__ == "__main__":
    unittest.main()