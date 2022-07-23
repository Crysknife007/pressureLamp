# Pressure Lamp
Pressure Trend Lamp with Pi Pico, BMP280 and ws2812b LED strip
By Spike Snell 7.19.2022

Lamp color indicates if pressure is gradually falling, rising, or staying about the same
Red means rising, Blue means falling, Purple means relatively stable pressure.

I've added the necessary libraries and circuit python uf2 that I utilized for this project.

The main variables to play with are the tick time, which is the time in seconds between pressure readings. 
10 readings successive readings are taken, and then compared against the last set of ten.

The range value can be modified, this is the amount of variance in pressure that is needed between the current set
of ten readings and the previous ten to be considered a significant trend. 

