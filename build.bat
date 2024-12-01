python -m PyInstaller --noconfirm --onefile --windowed --icon "C:\Users\Jordan\Workspace\Python\FolderCleaner\icon.ico" --name "Folder Cleaner" --add-data "C:\Users\Jordan\Workspace\Python\FolderCleaner\config.py;." --add-data "C:\Users\Jordan\Workspace\Python\FolderCleaner\helper.py;." --add-data "C:\Users\Jordan\Workspace\Python\FolderCleaner\icon.png;." --add-data "C:\Users\Jordan\Workspace\Python\FolderCleaner\ui.py;." --add-data "C:\Users\Jordan\Workspace\Python\FolderCleaner\widgets.py;."  "C:\Users\Jordan\Workspace\Python\FolderCleaner\main.py"

set /p deleteBuildFolder="Do you want to delete the build folder? (y/n): "
if /i "%deleteBuildFolder%"=="y" (
    rmdir /s /q build
    echo Build folder deleted.
) else (
    echo Build folder not deleted.
)