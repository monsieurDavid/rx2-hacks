rx2 hacks
=========

Fun with Realtek RX2 (RX2B) driven remote controlled toys.

Datasheet: http://www.datasheetdir.com/RX-2B+download

Two flavours (for now):
- RX2_Control.ino runs using micros() based timer for HIGH/LOW signals; obtains a better response from the RX2 chip.
- RX2_PWM_Control.ino runs using the Arduino controller chip hardware timer registers, namely Timer1.


Arduino demo: http://youtu.be/7js6pt2g0ac
