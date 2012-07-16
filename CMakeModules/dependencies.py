#!/usr/bin/python3
import os
import shutil
import subprocess
import re
import sys

_libs_blacklist_win = set({
	"kernel32.dll","msvcrt.dll","glu32.dll","mswsock.dll","opengl32.dll","wsock32.dll","ws2_32.dll","advapi32.dll","ole32.dll",
	"user32.dll","comdlg32.dll","gdi32.dll","imm32.dll","shell32.dll","oleaut32.dll","winmm.dll"
})

_libs_blacklist_posix = set([
	"libdl.so",
	"libexpat.so",
	"libfontconfig.so",
	"libfreetype.so",
	"libgcc_s.so",
	"libGL.so",
	"libICE.so",
#	"libm.so",
	"libnvidia-glcore.so",
	"libnvidia-tls.so",
	"libpthread.so",
	"librt.so",
	"libSM.so",
	"libuuid.so",
	"libX11.so",
	"libXau.so",
	"libxcb.so",
	"libXdmcp.so",
	"libXext.so",
	"libXi.so",
	"libXmu.so",
	"libXrender.so",
	"libXt.so",
	"libXxf86vm.so",
	"libgio-2.0.so"
])

def _find_win_dll(search_paths,dll_basename):
	assert os.name == 'nt'
	search_path = os.environ['PATH'].split(';')
	search_path.extend(search_paths)
	search_path.append(os.getcwd())
	for i in search_path:
		if os.path.exists(i):
			if os.path.exists(os.path.join(i,dll_basename)):
				return os.path.realpath(os.path.join(i,dll_basename))
	raise Exception("Dll not found")

def _find_depends(search_paths):
	for i in search_paths:
		if os.path.exists(os.path.join(i,"depends.exe")):
			return os.path.join(i,"depends.exe")
	raise Exception("Dependency walker not found")

def _dependencies_libs_nt(search_paths,path):
	result = []
	path2 = os.path.abspath(path)
	assert os.path.basename(path) not in _libs_blacklist_win
	dependsExePath = _find_depends(search_paths)
	lastdir = os.getcwd()
	subprocess.call([dependsExePath,"/c","/ot:dependency-output.txt",path2])

	depfile = open("dependency-output.txt")
	depfile_tree = []
	started = False
	start_string = "***************************| Module Dependency Tree"
	end_string = "********************************| Module List"
	lineNumber = 0+8
	for i in depfile:
		if started:
			if(re.match("\s*\[",i) is not None):
				depfile_tree.append(i)
			if i[:len(end_string)] == end_string:
				break
		else:
			lineNumber += 1
			if i[:len(start_string)] == start_string:
				started = True
	assert started
	
	ignore_until = 1000
	for i in depfile_tree:
		lineNumber += 1
		lvl = len(re.search("^\s*",i).group(0))/5
		if lvl == 0:
			continue
		if( lvl > ignore_until ):
			continue;
		else:
			ignore_until = 1000
		searched = re.search("[^ ]*\.DLL",i)
		if searched is None:
			searched2 = re.search("[^ ]*\.[A-Z]{3}",i)
			if searched2 is not None:
				ignore_until = lvl
			continue
		dll_name = searched.group(0).lower()
		if dll_name in _libs_blacklist_win:
#				print(lvl,dll_name,"ignore") #Debugging line that helps making the blacklist
			ignore_until = lvl
		else:
#				print(lvl,dll_name,lineNumber) #Debugging line that helps making the blacklist
			try:
				if lvl > 0:
					result.append(_find_win_dll(search_paths,dll_name))
			except Exception:
				sys.stderr.writelines((dll_name)+" not found.")
	depfile.close()
	os.unlink("dependency-output.txt")
	os.chdir(lastdir)
	return result

def _posix_lib_basename(path):
	file_basename = os.path.basename(path).split(".")
	while file_basename[-1].isdigit():
		file_basename.pop()
	return ".".join(file_basename)

def _dependencies_libs_posix(search_paths,path):
	result = []
	p = subprocess.Popen(["ldd", path], stdout=subprocess.PIPE)
	out = p.communicate()[0].decode().split("\n")
	for i in out:
		if len(i.split("=>")) != 2:
			continue
		dep_path = i.split("=>")[1].strip().split(" ")
		if len(dep_path) != 2:
			continue
		if not _posix_lib_basename(dep_path[0]) in _libs_blacklist_posix:
			abspath = os.path.abspath(dep_path[0])
			result.append(abspath)
			if os.path.realpath(abspath) != abspath:
				result.append(os.path.realpath(abspath))
	return result

def dependencies_libs(search_paths,path):
	strategies = {'nt':_dependencies_libs_nt,
			'posix':_dependencies_libs_posix}
	return strategies[os.name](search_paths,path)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		sys.stderr.writelines("Usage: "+sys.argv[0]+"[search_paths] binaryfile\n")
		sys.exit(1)
	target = sys.argv[-1]
	search_paths = list(map(os.path.abspath,sys.argv[1:len(sys.argv)-1]))
	
	os.chdir(os.path.dirname(target))
	sys.stdout.writelines( ";".join(dependencies_libs(search_paths,os.path.basename(target))) )
