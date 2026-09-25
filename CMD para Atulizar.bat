@echo off

cd /d "%~dp0"

echo === Atualizando site ===
echo.

:: Pega a data e hora atual do PC
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set DATETIME=%%a

set ANO=%DATETIME:~0,4%
set MES=%DATETIME:~4,2%
set DIA=%DATETIME:~6,2%
set HORA=%DATETIME:~8,2%
set MINUTO=%DATETIME:~10,2%
set SEGUNDO=%DATETIME:~12,2%

set COMMIT=%DIA%-%MES%-%ANO% %HORA%-%MINUTO%-%SEGUNDO%

echo Commit: %COMMIT%
echo.

echo === Verificando arquivos ===
git status
echo.

echo === Adicionando TODAS as alteracoes ===
git add -A
echo.

echo === Criando commit ===
git commit -m "%COMMIT%"
echo.

echo === Enviando para o GitHub ===
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo === PUSH FALHOU ===
    echo Tentando pull --rebase...
    echo.

    git pull origin main --rebase

    if %errorlevel% neq 0 (
        echo.
        echo O pull --rebase tambem falhou.
        pause
        exit /b 1
    )

    echo.
    echo === Tentando push novamente ===
    git push origin main

    if %errorlevel% neq 0 (
        echo.
        echo === SEGUNDO PUSH TAMBEM FALHOU ===
        pause
        exit /b 1
    )
)

echo.
echo === FINALIZADO ===
timeout /t 2 /nobreak >nul
exit