'''użyty algorytm odzyskiwania sygnału zaczerpnięty jest z pracy:
Total Variation Filtering
Ivan W. Selesnik, İlker Bayram
2010

the algorithm used to denoise the signal comes from:
Total Variation Filtering
Ivan W. Selesnik, İlker Bayram
2010
'''

import random
import matplotlib.pyplot as plt
import numpy as np
import pdb
import csv
import pickle

#GENERATING SIGNAL X
total_len = 200
sig_min_length = 10
sig_max_length = 30
sig_max_height = 6

#GENERATING SINGAL Y
noise_max_height = 0.5

#RETRIEVING SIGNAL
iteration_number = 1000
alpha = 4
lbda = 3


def generate_x():
    x = []
    while len(x) < total_len:
        x +=  [int(sig_max_height * random.random())] * ( int((sig_max_length - sig_min_length)*random.random()) + sig_min_length )
    x = x[:total_len]
    return np.asarray(x)

def generate_y():
    y = []
    for i in range(len(x)):
        rand = random.random()
        if rand < 0.5:
            y += [noise_max_height*random.random()]
        else:
            y += [-noise_max_height*random.random()]
    y = [float(i) + float(j) for i, j in zip(x,y)]
    return np.asarray(y)

def plot( show_x = True, show_y = True, show_denoised = True):
    if show_x: plt.plot(np.arange(0,total_len,1), x, color = 'g')
    if show_y: plt.plot(np.arange(0,total_len,1), y, color = 'b')
    if show_denoised: plt.plot(np.arange(0,total_len,1), denoised, color = 'r')
    plt.xlim(0,total_len)
    plt.ylim(-noise_max_height - 1,sig_max_height + noise_max_height +  1)
    plt.show()

def open_from_file(ar):
    if str(ar) not in ('x','y','denoised'):
        with open ('signal_'+ ar, 'r') as f:
            x = list(f.read().rstrip(',').split(','))
            x = np.asarray(x)
    else:
        print("run with x,y or denoised parameter")

def produce_D():
    D = np.zeros((len(y) - 1,len(y)))
    for i in range(len(y) -1):
        D[i][i] = -1
        D[i][i+1] = 1
    return D

def get_denoised():
    D = produce_D()
    z_it = np.zeros(len(y) - 1)
    for k in range(iteration_number):
        b = (1/alpha)*D.dot(  (2/lbda)*y - D.transpose().dot(z_it)  ) + z_it
        for i in range(len(z_it)):
            z_it[i] = np.sign(b[i])*min(abs(b[i]),1)
    denoised = y - (lbda/2)*D.transpose().dot(z_it)
    return denoised

def save_to_file():
    with open('saved_data.pickle', 'wb') as handle:
        pickle.dump({'x':x,'y':y, 'denoised':denoised}, handle)

def open_from_file():
    with open('saved_data.pickle', 'rb') as handle:
        data = pickle.load(handle)
        global x, y, denoised
        x = data['x']
        y = data['y']
        denoised = data['denoised']
#-----------------------------------------------------------------------------------------------------
'''
parametry można zmienić na górze pliku
przykład użycia znajduje się poniżej komentarza
w celu zapisu danych do pliku i odczytu używamy
save_to_file()
open_from_file()
żeby wygenerować y, najpierw trzeba wygenerować x
można rysować kilka wykresów na raz
najlepiej używać w sposób:
python3 denosing.py
albo w trybie interaktywnym
python3 -i denosing.py
żeby program działał dalej, należy zamknąć okno wykresu


parameters can be change at the beggining of the file
example usage is under this comment
in order save or load from file use
save_to_file()
open_from_file()
to generate y, it's necessary to generate x first
it's possible draw few plots at once
best use this way
python3 -i denosing.py
or in intearctive mode
python3 -i denosing.py
in order to proceed the program close the plot window
'''

x = generate_x()
y = generate_y()
denoised = get_denoised()

plot(show_x = True, show_y = False, show_denoised = False)
plot(show_x = False, show_y = True, show_denoised = False)
plot(show_x = False, show_y = False, show_denoised = True)
