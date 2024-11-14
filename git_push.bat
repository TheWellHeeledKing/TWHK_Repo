@echo off

git status

:: Change to the correct directory (adjust path if needed)
cd /d C:\Users\Mike\Software\Python\TWHK_Repository

:: Stage all changes
git add .

:: Get the commit message as the first argument
set "COMMIT_MESSAGE=%~1"

:: If no commit message is provided, ask for one
if "%COMMIT_MESSAGE%"=="" (
    echo Please provide a commit message.
    exit /b
)

:: Commit the changes with the provided message
git commit -m "%COMMIT_MESSAGE%"

:: Push the changes to the 'main' branch (or adjust if using a different branch)
git push origin main

git log

echo Changes have been pushed successfully!
pause
