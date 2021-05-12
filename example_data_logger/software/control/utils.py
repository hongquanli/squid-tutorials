import numpy as np

def unsigned_to_signed(unsigned_array,N):
    signed = 0
    for i in range(N):
        signed = signed + int(unsigned_array[i])*(256**(N-1-i))
    signed = signed - (256**N)/2
    return signed

def unsigned_to_unsigned(unsigned_array,N):
    unsigned = 0
    for i in range(N):
        unsigned = unsigned + int(unsigned_array[i])*(256**(N-1-i))
    return unsigned

def DACs_to_temp(DAC1,DAC2,R_fixed):
	fraction = float(DAC2/DAC1)
	# DAC2 measures the voltage across the thermistor (GND - middle pin)
	# DAC1 measures the voltage across the thermistor + fix resistor 1.977 kohm

	# R_fixed = 1977
	# R_fixed = 1980
	B = 3455
	R_thermistor = R_fixed*fraction/(1-fraction) # 1977 ohm is the resistance of the fixed resistor
	
	# r/(r0 + r) = fraction
	# r = r0*fraction + r*fraction
	# r = r0*fraction/(1-fraction)

	# https://www.digikey.com/en/maker/projects/how-to-measure-temperature-with-an-ntc-thermistor/4a4b326095f144029df7f2eca589ca54
	# https://www.digikey.com/en/products/detail/murata-electronics/NXFT15XH103FA2B100/2533821
	# https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html
	# B25/100 is 3455K

	inverseT_K = (1/(25+273.15)) + (1/B)*np.log(R_thermistor/10000)
	T_K = 1/inverseT_K
	T_degreeC = T_K - 273.15

	return T_degreeC

	# https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html