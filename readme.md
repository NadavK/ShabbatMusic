# ShabbatMusic
Plays music before Shabbat/Hag.
The song is selected per the specific Hag.
Switches on a raspberry GPIO that can be connected to a solid-state relay.

# Installation
1. In raspi-config:
   1. Set timezone to Other>UTC
   1. Enable I2C (I think)
1. `
sudo apt-get install omxplayer
` 
1. RTC: https://www.raspberrypi.org/forums/viewtopic.php?t=209700
1. Follow instructions in ~requirements.txt
1. Set `sudo crontab -e`<br>
```
45 2 * * *  /home/pi/shabbat/m
@reboot  /home/pi/shabbat/m
```
