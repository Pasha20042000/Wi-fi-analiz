from libhackrf import *
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack



hackrf = HackRF()

hackrf.sample_rate = 20e6
hackrf.center_freq = 88.5e6

sn = hackrf.get_serial_no()
print(sn)
while(True):
    samples = hackrf.read_samples()

    # количество семплов
    N = samples.size
    # 1/sample_rate
    T = 1.0 /hackrf.sample_rate
    x = np.linspace(0.0, N*T, N)
    #samples
    y = samples
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    print(samples[:100])
    # fig, ax = plt.subplots()
    # ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    # plt.show()


#result = libhackrf.hackrf_set_sample_rate(dev, 20e6)
#print "set sample rate = ", result
#
#result = libhackrf.hackrf_set_lna_gain(dev, 8)
#print "set lna gain = ", result
#
#result = libhackrf.hackrf_set_vga_gain(dev, 20)
#print "set vga gain = ", result
#
#result = libhackrf.hackrf_start_rx(dev, rx_callback, None)
#print "starting rx... = ", result


#libhackrf.hackrf_exit()
