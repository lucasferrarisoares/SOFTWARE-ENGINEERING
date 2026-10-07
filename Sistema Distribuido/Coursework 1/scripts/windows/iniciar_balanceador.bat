@echo off
setlocal
pushd "%~dp0\..\.."

where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 src\balanceador_carga.py
) else (
    python src\balanceador_carga.py
)

popd
endlocal
pause
