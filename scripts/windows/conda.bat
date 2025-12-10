@echo off
set "__PREFIX=%~dp0\.."
"%__PREFIX%\.micromamba\micromamba.exe" --root-prefix "%__PREFIX%" --prefix "%__PREFIX%" %*
