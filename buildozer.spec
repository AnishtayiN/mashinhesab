[app]

# (str) Title of your application
title = ماشین حساب پیشرفته

# (str) Package name
package.name = mashinhesab

# (str) Package domain (needed for android/ios packaging)
package.domain = org.anishtayin

# (str) Source code where the main.py live
source.dir = .

# (str) Main Python file
main.py = main.py

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ico

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"'](.*)['"']
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3,kivy>=2.1.0

# (str) Custom source folders for requirements
#requirements.source = 

# (list) Garden requirements
#garden_requirements = 

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/calculator.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:entrypoint_to_python_file

#
# OSX Specific
#
#
# author = © Copyright Info

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a, arm64-v8a

# (int) Android API to use
android.api = 24

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) python-for-android branch to use
#p4a.branch = develop

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of the Android .apk to build
#android.apk = mashinhesab-1.0.0.apk

#
# iOS specific
#

# (str) Path to the certificate used for signing the IPA
#ios.certificate.path = certs/my_certificate.pem

# (str) Name of the certificate
#ios.certificate.name = iPhone Developer: John Doe (5R5CM854L2)

# (str) Name of the provisioning profile
#ios.provisioning.profile = my_provisioning_profile.mobileprovision

# (str) Name of the code signing identity
#ios.codesigning.identity = iPhone Developer: John Doe (5R5CM854L2)

# (str) List of device identifiers allowed in the provisioning profile
#ios.provisioning.device_identifier = 00008030-001BD0651E84002D

# (str) Name of the entitlements file
#ios.entitlements = entitlements.plist

# (bool) whether to sign the app with entitlements or not
#ios.entitlements.enabled = True

# (str) List of font files to include
#ios.fonts = Roboto.ttf, Roboto-Bold.ttf

# (str) The directory in which the app will be signed
#ios.signing.directory = /Users/me/Code/signing

#
# Desktop specific
#

# (str) Packaged data directory name, in the Mac app bundle
#macos.app_data_dir = data

# (str) Packaged resources directory name, in the Mac app bundle
#macos.app_resources_dir = resources

# (str) Icon file name, in the Mac app bundle
#macos.app_icon = icon.png

# (str) List of resolution sizes to include in the Mac app bundle
#macos.app_resolutions = mipmap

# (str) List of framework directories to include in the Mac app bundle
#macos.app_frameworks_dir = frameworks

# (str) Path to the signing certificate for Mac
#macos.codesigning.certificate = Developer ID Application: John Doe (5R5CM854L2)

# (bool) Whether to sign the Mac app with entitlements or not
#macos.codesigning.entitlements = True

# (str) Name of the entitlements file for Mac
#macos.codesigning.entitlements = entitlements.plist

# (str) List of entitlements to include in the Mac app bundle
#macos.entitlements = entitlements.plist

#
# Define the build presets for different platforms

[p4a_android]

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#gitclone.url = https://github.com/kivy/python-for-android
#gitclone.branch = develop

# (str) The bootstraps to build for
#p4a.branch = develop

# (str) Architecture to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.arch = armeabi-v7a

#
# Python3 for android (pygame_webview only, deprecated in favor of p4a branch)
#
# (str) python3 git clone directory (if empty, it will be automatically cloned from github)
#python3.gitclone.url = https://github.com/kivy/python3
#python3.gitclone.branch = master

#
# ios specific (deprecated in favor of p4a branch)
#

# (str) Path to the certificate used for signing the IPA
#ios.certificate.path = certs/my_certificate.pem

# (str) Name of the certificate
#ios.certificate.name = iPhone Developer: John Doe (5R5CM854L2)

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
