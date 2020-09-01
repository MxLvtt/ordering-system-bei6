1_create a shell skript file e.g "order-sys.sh" and put the command in it of the file you want to execute 
     "python3 /home/pi/ordering-sys/ordering-system-bei5/src/UI/Kitchen/test.py"
2_Execute this command to make shell script runnable "chmod u+x order-sys.sh". now you can run it normally by clicking on it or per command line.
3_go to desktop folder and create a "Ordersys.desktop" file.
4_open it and write following
[Desktop Entry]
Encoding=UTF-8
Name=Ordering system
Comment=Launch OS
Exec=/home/pi/order-sys.sh     //path of shell script to be executed
Icon=input-tablet              //icon name. there is a large variety of icons to choose from or you can find a way to add your own
Type=Application
Name[en_US]=Ordersys
5_ save it , run it and it should works! 

       
