project(
  'mf2005',
  'fortran',
  'c',
  version: '1.12.02',
  license: 'CC0',
  meson_version: '>= 1.3.1',
  default_options : [
    'b_vscrt=static_from_buildtype', # Link runtime libraries statically on Windows
    'buildtype=release',
    'debug=false',
    'c_std=c99',
    'fortran_std=legacy',
])

if get_option('buildtype') == 'release'
  profile = 'release'
else
  profile = 'develop'
endif
message('Profile:', profile)

is_double = get_option('double')
message('Double precision:', is_double)

# parse compiler options
fc = meson.get_compiler('fortran')
fc_id = fc.get_id()
cc = meson.get_compiler('c')
cc_id = cc.get_id()
message('Fortran compiler ID:', fc_id)
message('C compiler ID:', cc_id)
compile_args = []
link_args = []
extra_deps = []

# Command line options for gfortran
if fc_id == 'gcc'
  # General options
  compile_args += [
                   '-fall-intrinsics',
                   '-pedantic',
                   '-cpp',
                   '-ffixed-line-length-none',
                   '-Wcharacter-truncation',
                   '-Wno-unused-dummy-argument', # This makes problems with OOP
                   '-Wno-intrinsic-shadow',      # We shadow intrinsics with methods, which should be fine
                   '-Wno-maybe-uninitialized',   # "Uninitialized" flags produce false positives with allocatables
                   '-Wno-uninitialized',
                   ]
  if is_double
    compile_args += [
                     '-fdefault-real-8',
                     '-fdefault-double-8',
                    ]
  endif

  # Define OS with gfortran for OS specific code
  # These are identical to pre-defined macros available with ifort
  system = build_machine.system()
  if system == 'linux'
    compile_args += '-D__linux__'
  elif system == 'darwin'
    compile_args += '-D__APPLE__'
  elif system == 'windows'
    compile_args += '-D_WIN32'
  endif
endif

# Command line options for ifort
if fc_id == 'intel-cl'
  # windows
  compile_args += ['/fpe:0',              # Activate all floating point exceptions
                   '/heap-arrays:0',
                   '/traceback',
                   '/fpp',                # Activate preprocessing
                   '/extend-source',
                   '/Qdiag-disable:7416', # f2008 warning
                   '/Qdiag-disable:7025', # f2008 warning
                   '/Qdiag-disable:5268', # Line too long
                   '/Qdiag-disable:10448',# ifort deprecation warning
                  ]
  link_args += ['/ignore:4217', # access through ddlimport might be inefficient
                '/ignore:4286'  # same as 4217, but more general
               ]
  if is_double
    compile_args += [
                     '/real-size:64',
                     '/double-size:64',
                    ]
  endif

elif fc_id == 'intel' or fc_id == 'intel-llvm'
  # linux and macOS
  compile_args += ['-fpe0',              # Activate all floating point exceptions
                   '-no-heap-arrays',
                   '-traceback',
                   '-extend-source',
                   '-diag-disable:7416',  # f2008 warning
                   '-diag-disable:7025',  # f2008 warning
                   '-diag-disable:5268',  # Line too long
                  ]
  link_args += '-static-intel'

  if is_double
    compile_args += [
                     '-r8',
                     '-autodouble',
                    ]
  endif

# Command line options for ifx
elif fc_id == 'intel-llvm-cl'
  # windows
  compile_args += ['/fpe:0',              # Activate all floating point exceptions
                   '/heap-arrays:0',
                   '/traceback',
                   '/extend-source',
                   '/fpp',                # Activate preprocessing
                   '/Qdiag-disable:7416', # f2008 warning
                   '/Qdiag-disable:7025', # f2008 warning
                   '/Qdiag-disable:5268', # Line too long
                  ]
  if is_double
    compile_args += [
                     '/4R8',
                     '/Qautodouble',
                    ]
  endif

endif

add_project_arguments(fc.get_supported_arguments(compile_args), language: 'fortran')
add_project_link_arguments(fc.get_supported_arguments(link_args), language: 'fortran')

compile_args = []
link_args = []
if cc_id == 'gcc'
  compile_args += ['-Wno-unused-but-set-variable']
elif cc_id == 'intel'
  compile_args += ['-frtti', '-diag-disable=10441']
  link_args += ['-diag-disable=10441']
endif

add_project_arguments(cc.get_supported_arguments(compile_args), language: 'c')
add_project_link_arguments(cc.get_supported_arguments(link_args), language: 'c')

# build
if is_double
  buildname = 'mf2005dbl'
else
  buildname = 'mf2005'
endif
message('Executable name: ' + buildname)
subdir('src')
