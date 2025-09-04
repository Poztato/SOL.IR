from machine import ADC
import time

# RP2040 internal temperature sensor is on ADC(4)
sensor = ADC(4)

# Conversion constants (RP2040 datasheet values)
ADC_TO_VOLT = 3.3 / 65535          # read_u16() returns 0..65535
V_AT_27C = 0.706                   # volts at 27 °C
SLOPE_V_PER_C = 0.001721           # volts per °C

def read_temp_c(samples=32, delay_us=200):
    """
    Return averaged die temperature in °C.
    samples: number of ADC samples to average
    delay_us: microseconds between samples (helps settle/average)
    """
    total = 0
    for _ in range(samples):
        total += sensor.read_u16()
        if delay_us:
            time.sleep_us(delay_us)
    avg = total // samples
    voltage = avg * ADC_TO_VOLT
    temp_c = 27.0 - (voltage - V_AT_27C) / SLOPE_V_PER_C
    return temp_c


if __name__ == "__main__":
    while True:
        
        t_c = read_temp_c()
        print("Temp: {:.2f} °C".format(t_c))
        time.sleep(1)

