@echo off
:name
echo. & echo. & set /P name=Type a name in lowercase for the patcher and press ENTER:  
if "%name%"=="" (
echo. & echo. & echo           --- Please enter something as instructed ---
goto:name
)
echo.
echo -----
echo Pruning the Docker builder...
echo -----
docker builder prune -f
echo.
echo.
echo -----
echo Building from Dockerfile...
echo -----
docker build --no-cache . -f Dockerfile -t %name%/%name%:latest --squash
echo.
echo.
echo -----
echo Build complete.
echo Running the container in detached mode...
echo -----
docker run -d -p 8000:8000 --name %name% %name%/%name%
echo.
echo.
echo -----
echo Stopping the container and setting always restart...
echo -----
docker stop %name%
docker update --restart always %name%
echo.
echo.
echo -----
echo Pruning the Docker builder...
echo -----
docker builder prune -f
echo.
echo.
echo -----
echo Finished.
echo.
echo Go to Docker Containers and press the play button to start the container.
echo -----
echo.
pause
exit /b
