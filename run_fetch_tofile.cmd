set t=%date%_%time%
set d=%t:~10,4%%t:~7,2%%t:~4,2%_%t:~15,2%%t:~18,2%%t:~21,2%
set d=%d: =%
set de=%d%_error
run_fetch.cmd > %d% 2>%de%

rem if %errorlevel% == 0 (
  
copy life.csv C:\meta4app\src\life.txt
copy history.csv C:\meta4app\src\history.txt
copy culture.csv C:\meta4app\src\culture.csv

cd /d C:\meta4app\app\consoleapp\bin\Release\netcoreapp3.1\
.\ConsoleApp.exe
  
rem )