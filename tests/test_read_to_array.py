from __future__ import print_function
import unittest
import pytraj as pt
from pytraj.utils import eq, aa_eq
from pytraj.decorators import no_test, test_if_having, test_if_path_exists
import pytraj.common_actions as pyca
import numpy as np

expected_result = np.array("""
 -0.149000  0.097600  0.097600  0.097600 -0.415700  0.271900  0.214802 -0.455023
  0.440678 -0.580394  0.230150  0.546609  0.627861 -0.775845 -0.673807 -0.790615
  0.129410  0.093648 -0.352368  0.116022  0.596326 -0.386959  0.079841  0.148065
 -0.614839  0.165480  0.906069 -0.775724 -0.783444  0.206985  0.559558 -0.377967
  0.545248 -0.362708  0.050194  0.158582 -0.604041  0.163106  0.900514 -0.776397
 -0.774453  0.205434 -0.149000  0.097600  0.097600  0.097600 -0.415700  0.271900
  0.214802 -0.455023  0.440678 -0.580394  0.230150  0.546609  0.627861 -0.775845
 -0.673807 -0.790615  0.129410  0.093648 -0.352368  0.116022  0.596326 -0.386959
  0.079841  0.148065 -0.614839  0.165480  0.906069 -0.775724 -0.783444  0.206985
  0.559558 -0.377967  0.545248 -0.362708  0.050194  0.158582 -0.604041  0.163106
  0.900514 -0.776397 -0.774453  0.205434
""".split(), dtype='f8')

class Test(unittest.TestCase):

    def test_0(self):
         arr = pt.tools.read_to_array("./data/floBF-resp.chg")
         assert arr.shape == (84, )
         print (arr)
         aa_eq(arr, expected_result)

if __name__ == "__main__":
    unittest.main()
