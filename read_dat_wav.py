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

def date(start,minute):
    year = minute[start+50]*1+minute[start+51]*2+minute[start+52]*4+minute[start+53]*8+minute[start+54]*10+minute[start+55]*20+minute[start+56]*40+minute[start+57]*80
    month = minute[start+45]*1+minute[start+46]*2+minute[start+47]*4+minute[start+48]*8+minute[start+49]*10
    day = minute[start+36]*1+minute[start+37]*2+minute[start+38]*4+minute[start+39]*8+minute[start+40]*10+minute[start+41]*20
    day_of_week_number = minute[start+42]*1+minute[start+43]*2+minute[start+44]*4
    if(day_of_week_number == 1):
        day_of_week = 'Monday'
    elif(day_of_week_number == 2):
        day_of_week = 'Tuesday'
    elif(day_of_week_number == 3):
        day_of_week = 'Wednesday'
    elif(day_of_week_number == 4):
        day_of_week = 'Thursday'
    elif(day_of_week_number == 5):
        day_of_week = 'Friday'
    elif(day_of_week_number == 6):
        day_of_week = 'Saturday'
    elif(day_of_week_number == 7):
        day_of_week = 'Sunday'
    hour = minute[start+29]*1+minute[start+30]*2+minute[start+31]*4+minute[start+32]*8+minute[start+33]*10+minute[start+34]*20
    minute = minute[start+21]*1+minute[start+22]*2+minute[start+23]*4+minute[start+24]*8+minute[start+25]*10+minute[start+26]*20+minute[start+27]*40
    full = 'The date and time is ' + str(20) + str(year) + '.' + str(month) + '.' + str(day) + '., ' + day_of_week + ', ' + str(hour) + ':' + str(minute)
    return full

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
# samplerate, data = wavfile.read("websdr_recording_start_2023-12-20T22_36_42Z_75.4kHz.wav")

print(len(data))
print(len(data)/fs)

if PLOTRAW:
    plt.plot(data)
    plt.title("raw data")
    plt.show()

# f=74469
# f=9517
#f=257287
#f=162430
#f=395923
f=0
power = 0

dataS=np.fft.fft(data)

spectrum = 20*np.log10(np.abs(dataS))

for i in range(0,len(spectrum)-1):
    if (spectrum[i]>power):
        power = spectrum[i]
        f = i
print('f=' + str(f))

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
    if(end[i]>1e9):
        binary[i]=1
    elif(end[i]<-1e9):
        binary[i]=-1
    else:
        binary[i]=0
        
plt.plot(binary)
plt.grid()
plt.legend()
plt.title("binary")
plt.show()

minute = []
j = 0
for i in range (0,len(binary)-1):
    if(binary[i]==0 and binary[i-1]==1):
        minute.append(1)
        j+=1
    if(binary[i]==0 and binary[i-1]==-1):
        minute.append(0)
        j+=1
print(minute)
print(len(minute))

minbits=[]
hourbits=[]
dombits=[]
dowbits=[]
monthbits=[]
yearbits=[]

j = 0
start_i = 0
for i in range(0,len(minute)-1):
    if(minute[i] == 1):
        j+=1
    if(minute[i] == 0):
        j=0
    if(j == 10):
        start_i = i-9
        break
print('Starting bit is ' + str(start_i))
print(date(start_i,minute))
