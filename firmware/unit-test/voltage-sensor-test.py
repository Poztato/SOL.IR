from machine import ADC, Pin
import time

# --- wiring ---
# Voltage sensor OUT -> GP26  (ADC0)
# Sensor VCC -> 3V3
# Sensor GND -> GND
# Panel + -> sensor VIN+, Panel - -> sensor GND

ADC_PIN = 26
adc = ADC(Pin(ADC_PIN))

VREF = 3.3                   # Pico ADC reference ~3.3 V
DIVIDER_RATIO = 5.0          # Sensor ratio
SAMPLES = 64

def read_adc_avg(samples=SAMPLES, delay_us=200):
    total = 0
    for _ in range(samples):
        total += adc.read_u16()
        if delay_us:
            time.sleep_us(delay_us)
    return total / samples

def volts_at_adc(raw):
    # Voltage present on the Pico ADC pin (after the sensor’s divider)
    return (raw / 65535.0) * VREF

def sensed_voltage(raw):
    # Estimated source voltage before the divider
    return volts_at_adc(raw) * DIVIDER_RATIO


while True:
    raw = read_adc_avg()
    v_adc = volts_at_adc(raw)
    v_in  = sensed_voltage(raw)
    print(f"raw={int(raw)}  V_adc={v_adc:.4f} V  Panel≈{v_in:.4f} V")
    time.sleep(0.5)

