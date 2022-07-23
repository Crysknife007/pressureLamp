# Pressure Trend Lamp with Pi Pico, BMP280 and ws2812b LED strip
# By Spike Snell 7.19.2022
# Lamp color indicates if pressure is gradually falling, rising, or staying about the same
# Red means rising, Blue means falling, Purple means relatively stable pressure

# Import everything that we need
import board, time, busio, adafruit_bmp280, neopixel

# Define the tick time in seconds
tick = 120

# Define the range, pressure change must be more or less than this to be considered significant
range = .8

# Create i2c sensor object
i2c = busio.I2C(board.GP1, board.GP0)

# Define the bmp280 sensor
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,0x76)

# Define the old pressure total
oldPressureTotal = 0

# Define the new pressure total
newPressureTotal = 0

# Set the number of neopixels on the strip
num_pixels = 3

# Initialize the neopixels
pixels = neopixel.NeoPixel(board.GP16, num_pixels)

# Set the pixel brightness
pixels.brightness = .7

# Fade in function
def fadeIn(r,g,b):

    # Loop 255 times to fade the light in
    for i in range(255):

        # Set the rgb brightness
        pixels.fill((i*r,i*g,i*b))

        # Sleep a little bit
        time.sleep(.02)

# Fade out function
def fadeOut(r,g,b):

    # Loop 255 times to fade the light out
    for i in range(255):

        # Fade out the rgb brightnesses
        pixels.fill((r*(255-i),g*(255-i),b*(255-i)))

        # Sleep a little bit
        time.sleep(.02)

# Fade out the current color
def fadeOutCurrent(currentColor):

    # If the current color is Red
    if currentColor == 'red':
        fadeOut(1,0,0)

    # If the current color is Blue
    elif currentColor == 'blue':
        fadeOut(0,0,1)

    # Else the current color must be Purple
    else:
        fadeOut(1,0,1)

# Fade in the color Purple by default
fadeIn(1,0,1)

# Set the current color identifier to Purple
currentColor = 'purple'

# Loop forever
while True:

    # Loop ten times
    for i in range(10):
        
        # Get the current pressure
        p = bmp280.pressure

        # Add this to the new pressure total
        newPressureTotal += p

        # Print the current pressure
        print('Current Pressure: ', p)
        print('New Total: ', newPressureTotal)
        print('Old Total: ', oldPressureTotal)

        # Sleep for tick amount of time
        time.sleep(tick)

    # If the old pressure total is not 0
    if oldPressureTotal != 0:
    
        # If the new pressure total is more than the old pressure total plus the range
        if newPressureTotal > oldPressureTotal + range:

            print('new pressure total is higher than the old pressure total plus the range of, ', range)

            # If the current color is not Red
            if currentColor != 'red':

                # Fade out the current color
                fadeOutCurrent(currentColor)

                # Set the current color identifier to Red
                currentColor = 'red'

                # Fade in Red
                fadeIn(1,0,0)

        # Else the new pressure total is not more than the old pressure total minus the range
        elif newPressureTotal < oldPressureTotal - range:

            print('new pressure total is lower than the old pressure total minus the range of, ', range)

            # If the current color is not Blue
            if currentColor != 'blue':

                # Fade out the current color
                fadeOutCurrent(currentColor)

                # Set the current color identifier to Blue
                currentColor = 'blue'
            
                # Fade in Blue
                fadeIn(0,0,1)

        # Else the new pressure total is not significantly more or less as defined by the range
        else:

            print('the new pressure total is pretty similar to the old pressure total')

            # If the current color is not Purple
            if currentColor != 'purple':

                # Fade out the current color
                fadeOutCurrent(currentColor)

                # Set the current color identifier to Purple
                currentColor = 'purple'

                # Fade in Purple
                fadeIn(1,0,1)

        # Set the old pressure total equal to the new pressure total
        oldPressureTotal = newPressureTotal

        # Reset the new pressure total back to zero
        newPressureTotal = 0


    # If the old pressure total is 0 because it has never been set
    if oldPressureTotal == 0:

        print('the old pressure total is 0 so this must be the first run')

        # Set the old pressure total to be equal to the new pressure total
        oldPressureTotal = newPressureTotal

        # Set the new pressure total back to 0
        newPressureTotal = 0 


