# -*- mode: python ; coding: utf-8 -*-
import os


block_cipher = None

#Dynamically set paths
SPEC_ROOT = os.path.abspath(SPECPATH)
SQLDIFF = os.path.join(SPEC_ROOT, 'sqldiff')
MIGRATIONS = os.path.join(SPEC_ROOT, 'migrations')

print(f'{SPEC_ROOT=}')
print(f'{SQLDIFF=}')

a = Analysis(['sqldiff/main.py', 'migrations/env.py'],
             pathex=[SPEC_ROOT, SQLDIFF, MIGRATIONS],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['env'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# remove /migrations/env.py script from execution scripts
# We don't want to execute env.py itself after main application finish its work
a.scripts = [t for t in a.scripts if t[0] != 'env']

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
