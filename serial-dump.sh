stty -F /dev/ttyUSB0 115200 raw -echo   #CONFIGURE SERIAL PORT
exec 3</dev/ttyUSB0                     #REDIRECT SERIAL OUTPUT TO FD 3
  cat <&3 > /tmp/ttyDump.dat           #DUMP CAPTURED DATA
