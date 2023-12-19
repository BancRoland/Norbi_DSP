import wave
import argparse
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

def LPF(v,a):
    out=1j*np.zeros(len(v))
    out[0]=v[0]
    for i in range(len(v)-1):
        out[i+1]=(1-a)*out[i]+a*v[i+1]
    return out

def resamp(v):
    out=np.zeros(len(v)*22)
    for i in range(len(v)):
        out[i*22:(i+1)*22]=(2*v[i]-1)*np.ones(22)
    return out

pCode=[0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,1,0,1,0,1,1,0,0,0,0,1,1,0,1,1,1,1,0,1,0,0,1,1,0,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,1,1,1,1,1,0,1,1,0,0,1,0,0,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,1,0,0,0,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,1,0,1,1,0,0,0,1,1,1,0,1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,0,0,0,0,1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,1,1,1,0,0,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,0,1,1,1,1,0,1,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,0,0,0,1,0,1,1,1,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,1,1,0,1,1,0,1,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0,1,1,0,0,0,1,0,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1]

pCode2=resamp(pCode)

plt.plot(pCode2,"o-")
plt.title(f"pCode, len={len(pCode2)}")
plt.show()

# samplerate, data = wavfile.read("dcf77_hole_minute.wav")
# samplerate, data = wavfile.read("websdr_recording_start_2023-12-19T13_16_54Z_77.5kHz.wav")
samplerate, data = wavfile.read("websdr_recording_start_2023-12-19T15_44_14Z_75.0kHz.wav")


print(len(data)/77500)

plt.plot(data)
plt.title("raw data")
plt.show()

# f=74469
f=9517

dataS=np.fft.fft(data)

plt.plot(np.log10(np.abs(dataS)))
plt.axvline(f,linestyle="--",alpha=0.5,color="C1")

dataS[0:f-5000]=np.zeros(len(dataS[0:f-5000]))
dataS[f+5000:]=np.zeros(len(dataS[f+5000:]))

dataS0=np.copy(dataS)

dataS0[0:f-50]=np.zeros(len(dataS[0:f-50]))
dataS0[f+50:]=np.zeros(len(dataS[f+50:]))

plt.plot(np.log10(np.abs(dataS)))
plt.title("Absolute spectrum")
plt.show()

data=np.fft.ifft(dataS)
data0=np.fft.ifft(dataS0)

mix=np.exp(-1j*2*np.pi*f*np.arange(len(data))/len(data))

# plt.plot(np.real(mix))
# plt.plot(np.imag(mix))
# plt.plot(np.abs(mix),color="gray",alpha=0.5)
# plt.plot(-np.abs(mix),color="gray",alpha=0.5)
# plt.show()

data3=data*mix
data30=data0*mix
# a=5e-2
# data3=LPF(data2,a)
# data3=LPF(data3,a)

dataS=np.fft.fft(data3)
plt.plot(np.log10(np.abs(dataS)))
plt.axvline(f,linestyle="--",alpha=0.5,color="C1")
plt.show()

plt.plot(np.real(data3),label="real")
plt.plot(np.imag(data3),label="imag")
plt.plot(np.abs(data3),color="gray",alpha=0.5,label="abs")
plt.plot(-np.abs(data3),color="gray",alpha=0.5)

plt.plot(np.real(data30),label="real")
plt.plot(np.imag(data30),label="imag")

plt.grid()
plt.legend()
plt.title("data3")
plt.show()

data4=data3*np.conj(data30)

plt.plot(np.real(data4),label="real")
plt.plot(np.imag(data4),label="imag")
plt.plot(np.abs(data4),color="gray",alpha=0.5,label="abs")
plt.plot(-np.abs(data4),color="gray",alpha=0.5)

plt.grid()
plt.legend()
plt.title("data3")
plt.show()

end=np.correlate(pCode2,np.imag(data4),"full")


plt.plot(end)

plt.grid()
plt.legend()
plt.title("end")
plt.show()




# plt.plot(np.angle(data3),label="phase")
# plt.grid()
# plt.legend()
# plt.show()

# data4=data3[:-1:]*np.conj(data3[1::])

# plt.plot(np.real(data4))
# plt.plot(np.imag(data4))
# plt.plot(np.abs(data4),color="gray",alpha=0.5)
# plt.plot(-np.abs(data4),color="gray",alpha=0.5)
# plt.show()