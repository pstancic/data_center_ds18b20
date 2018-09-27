# data_center_ds18b20
This is a python script that will keep an eye on, and report threshold violations on, as many as 10 ds18b20 sensors connected to the 1-wire interface.

Default thresholds are set to 79.0 F

Ensure you have the w1 set:

- add `dtoverlay=w1-gpio` to `/boot/config.txt`
- reboot

Don't forget to change the email
