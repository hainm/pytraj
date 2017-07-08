import pytraj as pt

from utils import fn

def test_lifetime():
    cmd = """
    parm {parm}
    trajin {trajin}
    hbond H1 series @N,H,C,O
    go
    lifetime H1[solutehb] window 5 name mylifetime
    runanalysis
    """.format(parm=fn("DPDP.parm7"),
               trajin=fn("DPDP.nc"))
    state = pt.load_cpptraj_state(cmd)
    state.run()

    key = "GLU_13@O-VAL_2@N-H"
    h_data = state.data[key].values
    print('h_data', h_data)

    data = pt.lifetime(h_data, window=5)
    print('data', data)

    print('lifetime')
    print(state.data['curve:0'].values)
