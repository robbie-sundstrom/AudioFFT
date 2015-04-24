import numpy as np
from scipy.io.wavfile import read,write


def speedup(soundarray, factor):
    indices = np.round(np.arange(0,len(soundarray),factor))
    indices = indices[indices < len(soundarray)].astype(int)
    return soundarray[indices.astype(int)]

def stretch(soundarray, factor, window_size, h):
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(len(soundarray)/factor + window_size)

    for i in np.arange(0, len(soundarray)-window_size-h, h*factor):
        a1 = soundarray[i:i+window_size]
        a2 = soundarray[i+h:i+window_size+h]

        s1 = np.fft.fft(hanning_window*a1)
        s2 = np.fft.fft(hanning_window*a2)

        phase = (phase+np.angle(s2/s1))%2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        i2 = int(i/factor)
        result[i2:i2+window_size] += hanning_window*a2_rephased

    result= ((2**(16-4)) * result/result.max())
    return result.astype('int16')

def pitchshift(soundarray, x, window_size=2**13, h =2*11):
    factor = 2**(x/12.0)
    stretched_sound = stretch(soundarray, 1.0/factor, window_size, h)
    return speedup(stretched_sound[window_size:], factor)

rate,data=read('rap.wav')
y=data[:]
print pitchshift(y, 2)