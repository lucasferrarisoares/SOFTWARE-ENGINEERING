@echo off
setlocal
pushd "%~dp0\..\.."

where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 src\cliente_encurtador.py %*
) else (
    python src\cliente_encurtador.py %*
)

popd
endlocal
pause
