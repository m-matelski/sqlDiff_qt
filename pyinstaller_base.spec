# -*- mode: python ; coding: utf-8 -*-
import os


block_cipher = None

#Dynamically set paths
SPEC_ROOT = os.path.abspath(SPECPATH)
SQLDIFF = os.path.join(SPEC_ROOT, 'sqldiff')
MIGRATIONS = 'migrations'
MIGRATIONS_PATH = os.path.join(SPEC_ROOT, MIGRATIONS)

print(f'{SPEC_ROOT=}')
print(f'{SQLDIFF=}')

a = Analysis(['sqldiff/main.py', 'migrations/env.py'],
             pathex=[SPEC_ROOT, SQLDIFF, MIGRATIONS_PATH],
             binaries=[],
             datas=[('alembic.ini', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# TODO exclude __pycache__
# Add alebic migration directory with its content
a.datas += Tree(MIGRATIONS_PATH, prefix=MIGRATIONS)

print(f"{a.datas}")


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# remove /migrations/env.py script from execution scripts
# We don't want to execute env.py itself after main application finish its work
a.scripts = [t for t in a.scripts if t[0] != 'env']

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SqlDiff',
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
               name='SqlDiff')
