import mraa


buz = mraa.Gpio(8)
buz.dir(mraa.DIR_OUT)
buz.write(0)

