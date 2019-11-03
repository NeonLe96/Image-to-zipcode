from PyInstaller.utils.hooks import copy_metadata, get_package_dir

datas += copy_metadata('google-cloud-vision')
datas += copy_metadata('google_cloud_vision')  #altlll

hiddenimports += ['google-cloud-firestore_v1']
#pythonhosted.org/pyinstaller/hooks.html#understanding-pyinstaller-hooks
#get_package_dir returns tuple (where pkg stored, abs path to pkg)
pkg_dir = 'X:\Python\Lib\site-packages\google\cloud\vision_v1'

datas += (pkg_dir, 'google-cloud-vision')