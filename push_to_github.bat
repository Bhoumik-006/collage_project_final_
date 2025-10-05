@echo off
cd /d "d:\collage complete project\final collage project"
echo Current directory:
cd
echo.
echo Git status:
git status
echo.
echo Adding files...
git add .
echo.
echo Committing changes...
git commit -m "📚 Update StudentConnect project with API integration documentation"
echo.
echo Pushing to GitHub...
git push origin api-documentation
echo.
echo Done! Check your GitHub repository.
pause