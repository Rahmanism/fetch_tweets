set t=%date%_%time%
set d=%t:~10,4%%t:~7,2%%t:~4,2%_%t:~15,2%%t:~18,2%%t:~21,2%
set d=%d: =%
set de=%d%_error
call run_fetch.cmd > %d% 2>%de%

@echo 'Fetching is done.'

@echo 'Copying files to meta4app...'
del C:\meta4app\src\life.txt
del C:\meta4app\src\history.txt
del C:\meta4app\src\culture.txt
copy life.csv C:\meta4app\src\life.txt
copy history.csv C:\meta4app\src\history.txt
copy culture.csv C:\meta4app\src\culture.txt

cd /d C:\meta4app\app\consoleapp\bin\Release\netcoreapp3.1\
.\ConsoleApp.exe  
curl -H "Host: localhost" -H "Cache-Control: max-age=0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36" -H "HTTPS: 1" -H "DNT: 1" -H "Referer: http://localhost/" -H "Accept-Language: en-US,en;q=0.8,en-GB;q=0.6,es;q=0.4" -H "If-Modified-Since: Thu, 23 Jul 2015 20:31:28 GMT" http://localhost/ > nul
cd /d C:\fetch_tweets
