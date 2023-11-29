# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['./ball_location/ball_final.py'],
             pathex=[],
             binaries=[],
             datas=[('launch_imag.png', '.'),('ball_ico.ico', '.'),('open_file.png', '.')],  # 添加这一行
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
# myapp.spec
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='智能球定位分析系统',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='ball_ico.ico',
          version='version.txt')  # 设置版本号为1.1.1
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='智能球定位分析系统')