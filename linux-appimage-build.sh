#!/bin/bash

set -e

rm -rf AppDir dist build *.spec

mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps
mkdir -p AppDir/usr/share
mkdir -p AppDir/usr/bin/_internal

pip install -r requirements.txt

cp src/styles.qss AppDir/usr/share/styles.qss
cp src/styles.qss AppDir/usr/bin/styles.qss
cp src/styles.qss AppDir/usr/bin/_internal/styles.qss

pyinstaller --onefile --windowed --name liblouis-table-editor \
  --add-data "src/assets:assets" \
  --add-data "src/styles.qss:_internal/styles.qss" \
  --add-data "src/styles.qss:styles.qss" \
  src/main.py

cp dist/liblouis-table-editor AppDir/usr/bin/

cat > AppDir/AppRun << 'EOL'
#!/bin/bash
cd "${APPDIR}/usr/bin"
exec "${APPDIR}/usr/bin/liblouis-table-editor" "$@"
EOL
chmod +x AppDir/AppRun

cp src/assets/icons/icon.ico AppDir/liblouis-table-editor.png

cat > AppDir/liblouis-table-editor.desktop << 'EOL'
[Desktop Entry]
Name=Liblouis Table Editor
Exec=liblouis-table-editor
Icon=liblouis-table-editor
Type=Application
Categories=Utility;
EOL

cp AppDir/liblouis-table-editor.desktop AppDir/usr/share/applications/

if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    wget -O appimagetool-x86_64.AppImage https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

./appimagetool-x86_64.AppImage AppDir Liblouis-Table-Editor-x86_64.AppImage
