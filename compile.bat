@echo off
go build -ldflags "-H=windowsgui"
XCOPY /Y  goTryEverything.exe  D:\local\

pause