#!/bin/bash


exitenceMiror=$(ps -aux | grep reconnaissance_miror | grep -v "grep" | wc -l)
exitenceUDP=$(ps -aux | grep serveurUdp.py | grep -v "grep" | wc -l)

 
if [ $exitenceMiror -eq 0 ] 
then
        echo "Miror not running"
        cd /home/pi/developpement
        python reconnaissance_miror.py &      
else
        echo "Miror running"    
fi

if [ $exitenceUDP -eq 0 ] ;
then
        echo "Udp not running"
        cd /home/pi/developpement
        python serveurUdp.py &    
else
        echo "Udp running"      
fi

exit 1