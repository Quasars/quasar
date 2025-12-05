@echo off
set "__PREFIX=%~dp0\.."
"%__PREFIX%\micromamba.exe" --root-prefix "%__PREFIX%" --prefix "%__PREFIX%" %*
