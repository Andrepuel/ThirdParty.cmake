ThirdParty.cmake
================
Cmake module to ease working with thirdparty libraries not installed on system wide configuration.

How to use it
-------------
Include `thirdparty.cmake` and invoke `THIRDPARTY_DIR(thirdparty)` with the thirdparty directory. This macro will give a hint to CMake of another place to also look for the libraries when invoking FindPackage.

The thirdparty directory contains a folder for each lib and inside this folder it is expected to exists at least "include","lib" or "bin".

For example, the GLEW lib inside the thirdparty folder looks like this:

    thirdparty/glew-1.7.0/lib/glew32mxs.lib
    thirdparty/glew-1.7.0/lib/glew32s.lib
    thirdparty/glew-1.7.0/lib/glew32mx.lib
    thirdparty/glew-1.7.0/lib/glew32.lib
    thirdparty/glew-1.7.0/include
    thirdparty/glew-1.7.0/include/GL
    thirdparty/glew-1.7.0/include/GL/glxew.h
    thirdparty/glew-1.7.0/include/GL/wglew.h
    thirdparty/glew-1.7.0/include/GL/glew.h
    thirdparty/glew-1.7.0/bin/glew32.dll
    thirdparty/glew-1.7.0/bin/glew32mx.dll
    (...)

(This is exactly what you get when you extract the package you get at Glew official page)

Deploy with Dependents Libraries
--------------------------------
On your CMakeLists.txt, instead of `INSTALL(...)` invoke `INSTALL_WITH_DEPS(...)`, the ThirdParty will search for dependencies of the specified targets through a helper python script which invokes `ldd` on posix and Dependency Walker on windows. Dependency walker must be available in the thirdparty directory.

Then, when you invoke _cpack_ or _make install_ the dependents libraries will be installed as well.

Read [CMake INSTALL documentation](http://www.cmake.org/cmake/help/v2.8.8/cmake.html#command:install) for help on how to use the `INSTALL` command.

Source group tree
-----------------
The source_group_tree.cmake provides the source_group_tree macro, which may be used as `source_group_tree(FilteName directory)`.
source_group_tree will scan `directory` recursively and will create source_group according to the dir hierarchy.


Future Work
-----------
Support `objdump` (if dependency walker is not available) on windows deploying.

Since my skills of explaing how to use `thirdparty.cmake` are very limited, I will add a sample of usage soon.
