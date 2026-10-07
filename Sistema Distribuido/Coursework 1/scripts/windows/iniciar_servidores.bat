@echo off
setlocal
pushd "%~dp0\..\.."

where py >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)

echo ========================================
echo INICIANDO OS 3 SERVIDORES RPC
echo ========================================

start "Servidor 0 - Porta 9000" cmd /k "%PYTHON_CMD% src\servidor_encurtador.py 0"
start "Servidor 1 - Porta 9001" cmd /k "%PYTHON_CMD% src\servidor_encurtador.py 1"
start "Servidor 2 - Porta 9002" cmd /k "%PYTHON_CMD% src\servidor_encurtador.py 2"

echo Servidores solicitados nas portas 9000, 9001 e 9002.
echo Confira as tres janelas antes de iniciar o balanceador.
popd
endlocal
pause
