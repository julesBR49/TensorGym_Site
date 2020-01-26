# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/reaghbruce-robertson/PycharmProjects/Tensors/main.py'],
             pathex=['/Users/reaghbruce-robertson/PycharmProjects/Tensors'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='TensorGym',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('/Users/reaghbruce-robertson/PycharmProjects/Tensors/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='TensorGym')
app = BUNDLE(coll,
             name='TensorGym.app',
             icon='/Users/reaghbruce-robertson/PycharmProjects/Tensors/TensorGym1024-1x.png,
             bundle_identifier=None)
