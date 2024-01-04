#以下虚拟环境可以使用
# source  /d/project/PycharmProjects/pyqt5/venvpy39/Scripts/activate
 pyinstaller    --add-data "NJS_APpt;NJS_APpt"  --add-data "images;images"   --add-data "config;config" call_main6.py --icon images/logo.ico   -w
cp config dist/call_main6 -r
cp images dist/call_main6 -r
cp test_input dist/call_main6 -r
# cp NJS_APpt dist/call_main6 -r
