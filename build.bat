python -m PyInstaller --noconfirm --onefile --windowed --icon ".\icon.ico" --name "Folder Cleaner" --add-data ".\config.py;." --add-data ".\helper.py;." --add-data ".\icon.png;." --add-data ".\ui.py;." --add-data ".\widgets.py;."  ".\main.py"

set /p deleteBuildFolder="Do you want to delete the build folder? (y/n): "
if /i "%deleteBuildFolder%"=="y" (
    rmdir /s /q build
    echo Build folder deleted.
) else (
    echo Build folder not deleted.
)