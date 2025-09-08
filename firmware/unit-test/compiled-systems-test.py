# Integrated sensors + dBFS + IR pulse (MicroPython, Raspberry Pi Pico)
# Pins:
#   sound (ADC1): GP27
#   solar (ADC0): GP26
#   IR blaster (PWM @ 38 kHz): GP2
#
# Behavior:
#   - Computes mic level in dBFS (no threshold on solar).
#   - Triggers if sound dBFS >= SOUND_DBFS_THRESHOLD OR temp °C >= TEMP_C_THRESHOLD.
#   - When triggered, prints ALL readings (dBFS, temp, solar volts) and pulses IR for 1 second.

import math, utime
from array import array
from machine import ADC, Pin, PWM

# ====== Pin mapping ======
PIN_SOUND = 27   # GP27 / ADC1
PIN_SOLAR = 26   # GP26 / ADC0
PIN_IR    = 2    # GP2  / PWM

# ====== Thresholds ======
SOUND_DBFS_THRESHOLD = -4.0   # trigger if dBFS >= this (e.g., -30 dBFS)
TEMP_C_THRESHOLD     = 30.0    # trigger if °C >= this

# ====== Mic (dBFS) sampling config ======
SAMPLE_RATE_HZ = 8000          # 8 kHz
N_SAMPLES      = 1024          # ~128 ms window at 8 kHz
PERIOD_US      = int(1_000_000 // SAMPLE_RATE_HZ)
FS_RMS         = (65535 / 2.0) / math.sqrt(2)  # RMS of full-scale sine -> 0 dBFS
buf_sound      = array('H', [0] * N_SAMPLES)

# ====== Solar + temperature config ======
VREF = 3.3
DIVIDER_RATIO = 5.0 
SOLAR_SAMPLES = 64

# RP2040 internal temperature sensor constants (typical values)
V_AT_27C       = 0.706
SLOPE_V_PER_C  = 0.001721

# ====== Peripherals ======
adc_sound = ADC(Pin(PIN_SOUND))   # ADC1
adc_solar = ADC(Pin(PIN_SOLAR))   # ADC0
adc_temp  = ADC(4)                # internal temperature sensor

pwm_ir = PWM(Pin(PIN_IR))
pwm_ir.freq(38000)
pwm_ir.duty_u16(0)  # off

# ====== Helpers ======
def pulse_ir_ms(duration_ms=1000):
    pwm_ir.duty_u16(32768)   # ~50% duty
    utime.sleep_ms(duration_ms)
    pwm_ir.duty_u16(0)

def capture_dbfs():
    """Capture N_SAMPLES at SAMPLE_RATE_HZ from adc_sound and return dBFS."""
    # timed capture
    s = 0
    t_next = utime.ticks_us()
    for i in range(N_SAMPLES):
        t_next = utime.ticks_add(t_next, PERIOD_US)
        x = adc_sound.read_u16()
        buf_sound[i] = x
        s += x
        while utime.ticks_diff(t_next, utime.ticks_us()) > 0:
            pass

    # remove DC bias (mean) and compute RMS
    mean = s / N_SAMPLES
    acc = 0.0
    for x in buf_sound:
        v = x - mean
        acc += v * v
    rms = math.sqrt(acc / N_SAMPLES)
    if rms <= 0:
        return -120.0
    return 20.0 * math.log10(rms / FS_RMS)

def read_adc_avg(adc, samples=SOLAR_SAMPLES, delay_us=200):
    total = 0
    for _ in range(samples):
        total += adc.read_u16()
        if delay_us:
            utime.sleep_us(delay_us)
    return total / samples

def volts_at_adc(raw):
    return (raw / 65535.0) * VREF

def sensed_voltage(raw):
    # Voltage before the divider (panel side)
    return volts_at_adc(raw) * DIVIDER_RATIO

def read_temp_c(samples=32, delay_us=200):
    total = 0
    for _ in range(samples):
        total += adc_temp.read_u16()
        if delay_us:
            utime.sleep_us(delay_us)
    avg = total / samples
    voltage = volts_at_adc(avg)
    return 27.0 - (voltage - V_AT_27C) / SLOPE_V_PER_C

# ====== Main loop ======
while True:
    dbfs   = capture_dbfs()
    temp_c = read_temp_c()
    raw_s  = read_adc_avg(adc_solar)
    v_in   = sensed_voltage(raw_s)
    v_adc  = volts_at_adc(raw_s)

    flagged = (dbfs >= SOUND_DBFS_THRESHOLD) or (temp_c >= TEMP_C_THRESHOLD)
    if flagged:
        # Print ALL readings when any sensor trips
        print("ALERT:")
        print("  Sound: {:6.1f} dBFS".format(dbfs))
        print("  Temp : {:6.2f} °C".format(temp_c))
        print("  Solar: {:6.3f} V (at ADC: {:6.3f} V)".format(v_in, v_adc))
        pulse_ir_ms(1000)

    # Small idle so we’re not hammering continuously beyond the sound window time
    utime.sleep_ms(50)

