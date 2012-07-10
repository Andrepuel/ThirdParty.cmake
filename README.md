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

Future Work
-----------
The first feature that will be added is to add deployment capabilities with dependencies tracking.

Also, since my skills of explaing how to use `thirdparty.cmake` are very limited, I will add a sample of usage soon.
