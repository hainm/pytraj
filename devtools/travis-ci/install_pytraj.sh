#!bin/sh

# create this file to hide output
# python setup.py install --amber-release

if [ "$PYPY" = "true" ]; then
    python=pypy
else
    python=python
fi


git clone https://github.com/Amber-MD/cpptraj
(cd cpptraj && git checkout 0fed4368806d217765116a3f5b74e4a447b342f6)

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    $python setup.py install --disable-openmp
else
    if [ "$TEST_SETUP" == 'true' ]; then
        echo "TEST_SETUP"
    else
        if [ "$USE_OPENMP" == 'false' ]; then 
            $python setup.py install --disable-openmp
        else
            # pytraj will pick compiler based on COMPILER env
            # or using default (gnu for linux, clang for osx)
            $python setup.py install
        fi
    fi
fi
