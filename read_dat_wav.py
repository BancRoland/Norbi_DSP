import wave
import argparse
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

# file from http://websdr.ewi.utwente.nl:8901/ 
# 75-80 kHz 75 kHz fc CW demod

PLOTCODE=0
PLOTRAW=0
LPF_CHECK=0
BASEBAND=0

fs=14233 # [Hz] ???
BW_A=500 # [Hz] bandpass for the first filter
BW_B=0.5 # [Hz] bandpass for the first filter


def LPF(v,a):
    out=1j*np.zeros(len(v))
    out[0]=v[0]
    for i in range(len(v)-1):
        out[i+1]=(1-a)*out[i]+a*v[i+1]
    return out

def resamp(v):
    out=np.zeros(len(v)*22)
    for i in range(len(v)):
        out[i*22:(i+1)*22]=-1*(2*v[i]-1)*np.ones(22)
    return out

pCode=[0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,1,0,1,0,1,1,0,0,0,0,1,1,0,1,1,1,1,0,1,0,0,1,1,0,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,1,1,1,1,1,0,1,1,0,0,1,0,0,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,1,0,0,0,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,1,0,1,1,0,0,0,1,1,1,0,1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,0,0,0,0,1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,1,1,1,0,0,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,0,1,1,1,1,0,1,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,0,0,0,1,0,1,1,1,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,1,1,0,1,1,0,1,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0,1,1,0,0,0,1,0,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1]

pCode2=resamp(pCode)

if PLOTCODE:
    plt.plot(pCode2,"o-")
    plt.title(f"pCode, len={len(pCode2)}")
    plt.show()

# samplerate, data = wavfile.read("dcf77_hole_minute.wav")
samplerate, data = wavfile.read("start_2023-12-19T18_16_50Z_75.0kHz.wav")
# samplerate, data = wavfile.read("websdr_recording_start_2023-12-20T08_30_58Z_75.0kHz.wav")
# samplerate, data = wavfile.read("websdr_recording_start_2023-12-20T08_53_38Z_75.0kHz.wav")


print(len(data))
print(len(data)/fs)

if PLOTRAW:
    plt.plot(data)
    plt.title("raw data")
    plt.show()

# f=74469
# f=9517
f=257287
#f=162430
#f=395923

dataS=np.fft.fft(data)

plt.plot(20*np.log10(np.abs(dataS)))
plt.axvline(f,linestyle="--",alpha=0.5,color="C1")

BW_A0=int(BW_A/fs*len(data))
dataS[0:f-BW_A0]=np.zeros(len(dataS[0:f-BW_A0]))
dataS[f+BW_A0:]=np.zeros(len(dataS[f+BW_A0:]))

dataS0=np.copy(dataS)

BW_B0=int(BW_B/fs*len(data))
dataS0[0:f-BW_B0]=np.zeros(len(dataS[0:f-BW_B0]))
dataS0[f+BW_B0:]=np.zeros(len(dataS[f+BW_B0:]))

plt.plot(20*np.log10(np.abs(dataS)))
plt.title("signal spectrum")
plt.xlabel("frequency []")
plt.ylabel("power [dB]")
plt.grid()
plt.show()

data=np.fft.ifft(dataS)
data0=np.fft.ifft(dataS0)

mix=np.exp(-1j*2*np.pi*f*np.arange(len(data))/len(data))


data3=data*mix
data30=data0*mix

dataS=np.fft.fft(data3)

if LPF_CHECK:
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

if BASEBAND:
    plt.plot(np.real(data4),label="real")
    plt.plot(np.imag(data4),label="imag")
    plt.plot(np.abs(data4),color="gray",alpha=0.5,label="abs")
    plt.plot(-np.abs(data4),color="gray",alpha=0.5)

    plt.grid()
    plt.legend()
    plt.title("data3")
    plt.show()

end=np.correlate(np.imag(data4),pCode2,"full")


plt.plot(end)
plt.axvspan(1.32e5,3.45e5,color="C1",alpha=0.5)
plt.axvspan(9.87e5,12e5,color="C1",alpha=0.5)
plt.grid()
plt.legend()
plt.title("end")
plt.show()


binary = [0]*len(end)
for i in range(0,len(end)-1):
    if(end[i]>7e8):
        binary[i]=1
    elif(end[i]<-7e8):
        binary[i]=-1
    else:
        binary[i]=0
        
plt.plot(binary)
plt.grid()
plt.legend()
plt.title("binary")
plt.show()
