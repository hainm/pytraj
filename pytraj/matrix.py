from __future__ import print_function, absolute_import
import numpy as np
from .actions import CpptrajActions
from .analyses import CpptrajAnalyses
from .datasets import cpp_datasets
from ._get_common_objects import _get_topology, _get_data_from_dtype
from .datasets.DatasetList import DatasetList as CpptrajDatasetList

mat_keys = {
    'dist',
    'correl',
    'covar',
    'mwcovar',
    'distcovar',
    'idea',
    'dihcovar',
}

__all__ = mat_keys

__cpptrajdoc__ = """
    cpptraj manual
    --------------
    Calculate a matrix of the specified type from input coordinates.

    + dist: Distance matrix (default).
    + correl: Correlation matrix (aka dynamic cross correlation).
    + covar: Coordinate covariance matrix.
    + mwcovar: Mass-weighted coordinate covariance matrix.
    + distcovar: Distance covariance matrix.
    + idea: Isotropically Distributed Ensemble Analysis matrix.
    + dihcovar: Dihedral covariance matrix.
"""

template = '''
def %s(traj=None, command="", top=None, dtype='ndarray', mat_type='full', *args, **kwd):
    """
    Parameters
    ----------
    traj : Trajectory-like
    command : cpptraj command
    top : Topology, optional, default None
    mat_type : str, {'full', 'half', 'cpptraj'}, default 'full'
        if 'full': 2D full matrix
        if 'half': triangular matrix
        if 'cpptraj': 1D array
    *args, **kwd: more arguments

    cpptraj compat mode
    -------------------
    {'distance_matrix' : 'dist',
    'correlation_matrix' : 'correl',
    'coord_covariance_matrix' : 'covar',
    'mw_covariance_matrix' : 'mwcovar',
    'distcovar_matrix' : 'distcovar',
    'idea_matrix' : 'idea'}
    """
    from .datasets.DatasetList import DatasetList as CpptrajDatasetList

    _top = _get_topology(traj, top)
    dslist = CpptrajDatasetList()
    template_command = '%s '
    template_command += command 

    act = CpptrajActions.Action_Matrix()
    act(template_command, traj, top=_top, dslist=dslist, *args, **kwd)
    # need to call `print_output` so cpptraj can normalize some data
    # check cpptraj's code
    act.print_output()
    if dtype == 'ndarray':
        if mat_type == 'full':
            return dslist[0].values
        elif mat_type == 'half':
            return dslist[0].to_half_matrix()
        elif mat_type == 'cpptraj':
            return dslist[0]._to_cpptraj_sparse_matrix()
        else:
            raise ValueError()
    else:
        return _get_data_from_dtype(dslist, dtype=dtype)
'''

for k in mat_keys:
    my_func_str = template % (k, k)
    g_dict = globals()
    exec(my_func_str)
    g_dict[k].__doc__ += __cpptrajdoc__

del k


def diagonalize(mat, n_vecs, dtype='dataset'):
    '''diagonalize matrix and return (eigenvalues, eigenvectors)

    Parameters
    ----------
    mat : 2D ndarray or DatasetMatrixDouble
    n_vecs : number of output vectors
    dtype : 'tuple' or 'dataset'
        if 'tuple', return a tuple (eigenvalues, eigenvectors). If 'dataset' return CpptrajDataseList
    '''
    _vecs = 'vecs ' + str(n_vecs)
    dslist = CpptrajDatasetList()
    dslist.add_set('matrix_dbl', 'mymat')

    if isinstance(mat, np.ndarray):
        indices = np.triu_indices(mat.shape[0])
        arr = mat[indices]
        dslist[0]._set_data_half_matrix(arr.astype('f8'),
                                        vsize=len(arr),
                                        n_cols=mat.shape[0])
    elif isinstance(mat, cpp_datasets.DatasetMatrixDouble):
        assert mat.kind == 'half', 'DatasetMatrixDouble must be half matrix'
        dslist[0]._set_data_half_matrix(mat._to_cpptraj_sparse_matrix(),
                                        vsize=mat.size,
                                        n_cols=mat.n_cols)

    act = CpptrajAnalyses.Analysis_Matrix()
    act(' '.join(('mymat', _vecs)), dslist=dslist)
    dslist._pop(0)

    if dtype == 'tuple':
        return (dslist[-1].eigenvalues, dslist[-1].eigenvectors)
    elif dtype == 'dataset':
        return dslist


def _diag_np(mat, n_vecs):
    evals, evecs = np.linalg.eigh(mat)
    evals = evals[::-1][:n_vecs]
    evecs = evecs[:, ::-1].T[:n_vecs]
    return evals, evecs
