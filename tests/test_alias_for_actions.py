import unittest
from pytraj.base import *
from pytraj import io as mdio
from pytraj.utils.check_and_assert import assert_almost_equal
from pytraj.common_actions import *

class Test(unittest.TestCase):
    def test_0(self):
        traj = mdio.load("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")[:]
        for _ in range(2):
            traj.join(traj[:])
        print (calc_dih(":2@CA :3@CA :10@CA :11@CA", traj)[:])
        print (calc_distance(":2@CA :3@CA", traj)[:])
        print (calc_angle(":2@CA :3@CA :10@CA", traj)[:])
        print (calc_radgyr("@CA", traj)[:])
        print (calc_molsurf("@CA", traj)[:])

if __name__ == "__main__":
    unittest.main()