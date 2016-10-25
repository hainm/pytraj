#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import unittest
import numpy as np
import subprocess
import pytraj as pt
from pytraj.utils import eq, aa_eq
from pytraj.version import version
from pytraj.utils.get_common_objects import get_reference
from pytraj.utils import misc
from pytraj import all_actions
import pytest


class TestExtraCoverage(unittest.TestCase):

    def setUp(self):
        self.traj = pt.iterload("./data/tz2.nc", "./data/tz2.parm7")

    def test_datafiles(self):
        traj = pt.datafiles.load_remd_ala2()
        assert len(traj.filelist) == 4, 'should have 4 replica trajs'
        filenames = [fn.split('/')[-1] for fn in traj.filelist]
        assert ['rem.nc.000', 'rem.nc.001', 'rem.nc.002', 'rem.nc.003'] == filenames, \
        'must have 4 replica trajs (rem.nc*)'

    def test_extra_coverage(self):
        '''all kind of tests that do not belong to anywhere else
        '''
        traj = pt.iterload("./data/tz2.nc", "./data/tz2.parm7")

        # show_versions
        pt.show_versions()
        pt._verbose()
        pt._verbose(False)
        print(version)

        # info
        pt.info()
        pt.info('parallel')
        misc.parallel_info('pmap')
        misc.parallel_info('openmp')
        misc.parallel_info(None)

        eq([2, 3], [2, 3])
        # raise if comparing NaN
        self.assertRaises(ValueError, lambda: aa_eq(np.nan, np.nan))

        dslist = pt.multidihedral(traj)
        string_ = str(dslist[0])

    def testget_common_objects(self):
        # raises
        # raise if try to index traj()
        self.assertRaises(TypeError, lambda: get_reference(self.traj(), 3))
        self.assertRaises(TypeError, lambda: get_reference(self.traj(), None))

        # specify wrong mask
        self.assertRaises(TypeError, lambda: pt.superpose(self.traj[:], 3))

    def test_all_actions(self):
        self.assertRaises(ValueError, lambda: all_actions._assert_mutable(self.traj))

    def test_io(self):
        os.environ['AMBERHOME'] = ''
        with pytest.raises(EnvironmentError):
            pt.io._get_amberhome()

    def test_testing_file_with_cpptrajhome(self):
        from pytraj.testing import testing
        os.environ['CPPTRAJHOME'] = '../cpptraj/'
        testing.cpptraj_test_dir

    def test_testing_file_without_cpptrajhome_but_having_amberhome(self):
        from pytraj.testing import testing
        os.environ['CPPTRAJHOME'] = ''
        os.environ['AMBERHOME'] = './fake_amberhome/'
        testing.cpptraj_test_dir

    def test_testing_file_without_cpptrajhome_without_amberhome(self):
        from pytraj.testing import testing
        os.environ['CPPTRAJHOME'] = ''
        os.environ['AMBERHOME'] = ''
        testing.cpptraj_test_dir

if __name__ == "__main__":
    unittest.main()
