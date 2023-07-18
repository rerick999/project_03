for /f "delims=: tokens=2" %%a in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do (set tempip=%%a)  
set tempip=%tempip: =%  
echo %tempip%
pause