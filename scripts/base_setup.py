import sys
import os
import subprocess

if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins

MAJOR               = 0
MINOR               = 1
MICRO               = 2
ISRELEASED          = False
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

message_auto_install = """
Can not find cpptraj header and libcpptraj files.
We're trying to dowload and build libcpptraj for you, would take about 5-10 minutes.
You can check ./cpptraj/ folder after installation.

To avoid auto-installation
--------------------------
You should set CPPTRAJHOME or installing ./cpptraj/ in this current folder.

If you want to manually install `libcpptraj`, you can download cpptraj
development version from here: https://github.com/Amber-MD/cpptraj

$ git clone https://github.com/Amber-MD/cpptraj/
$ cd cpptraj
$ export CPPTRAJHOME=`pwd`
$ ./configure -shared -openmp gnu
$ make libcpptraj

and then go back to pytraj folder:
python setup.py install
"""

message_openmp_cpptraj = '''
libcpptraj was detected to be installed with openmp.
You can not use --disable-openmp flag with pytraj
'''

message_serial_cpptraj = '''
libcpptraj was detected not be installed with openmp. You can recompile it with -openmp flag or 
disable openpm install in pytraj by adding --disable-openmp

Example:
    - Turn off openmp in pytraj: python setup.py install --disable-openmp
    - Turn ON openmp in cpptraj: ./configure -shared -openmp gnu && make libcpptraj -j4
    - Turn ON openmp in cpptraj and using netcdf, lapack, ... in $AMBERHOME (if having
      one):
          ./configure -shared -openmp -amberlib gnu && make libcpptraj -j4
'''

message_after_sucessful_install = '''
make sure to add {0} to your LD_LIBRARY_PATH
    - Example: export LD_LIBRARY_PATH={1}:$LD_LIBRARY_PATH

    - Notes: you can move `libcpptraj.so` to any where you want, just properly add it to
      $LD_LIBRARY_PATH

Run test:
    - simple (few seconds): python ./runtests.py simple
    - full (5-10 minutes): python runtests.py

Check compiling info:
    # change directory so python does not try to import source code
    cd tests # or any other folders
    python -c 'import pytraj as pt; pt.show_versions()'

'''

def remind_export_LD_LIBRARY_PATH(build_tag, libdir, pytraj_inside_amber):
    if build_tag:
        if not pytraj_inside_amber:
            from scripts.acsii_art import batman
            print("")
            print("")
            print(batman)
            libdir = os.path.abspath(libdir)
            print(message_after_sucessful_install.format(libdir, libdir))
            print("")
        else:
            # pytraj is a part of Amber
            print('make sure to `source $AMBERHOME/amber.sh` (if using bash) '
                  'or `source $AMBERHOME/amber.csh` if using csh')
    else:
        print("not able to install pytraj")

# Return the git revision as a string
# git_version, get_version_info, write_version_py  was lightly adapted from numpy package
# http://www.numpy.org/
# Numpy is licensed under the BSD license, 

def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

# This is a bit hackish: we are setting a global variable so that the main
# numpy __init__ can detect if it is being loaded by the setup routine, to
# avoid attempting to load components that aren't built yet.  While ugly, it's
# a lot more robust than what was previously being used.
builtins.__PYTRAJ_SETUP__ = True


def get_version_info():
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('pytraj/__version__.py'):
        # must be a source distribution, use existing version file
        try:
            from pytraj.__version__ import git_revision as GIT_REVISION
        except ImportError:
            # FIXME pytraj
            #raise ImportError("Unable to import git_revision. Try removing " \
            #                  "numpy/version.py and the build directory " \
            #                  "before building.")
            pass
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev12+' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION


def write_version_py(filename='pytraj/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM PYTRAJ SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    FULLVERSION, GIT_REVISION = get_version_info()

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version' : FULLVERSION,
                       'git_revision' : GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()
