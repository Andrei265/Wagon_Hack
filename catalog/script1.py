# -*- coding: utf-8 -*-

import datetime
import wave, math, contextlib
import speech_recognition as sr
import os, glob
from progress.bar import IncrementalBar
import asyncio

import pandas as pd
import re
import nltk
import pymorphy2

def main():

    for root, dirs, files in os.walk("media/files/"):  
        for filename in files:
            os.rename("media/files/"+str(filename), 'media/files/wagon.wav')



    start_time = datetime.datetime.now()
    ###########################################################################

    transcribed_audio_file_name = "media/files/wagon.wav"
    with contextlib.closing(wave.open(transcribed_audio_file_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    total_duration = math.ceil(duration / 15)

    bar = IncrementalBar('progress', max = total_duration)

    r = sr.Recognizer()
    row = ''
    for i in range(0, total_duration):
        try:
            with sr.AudioFile(transcribed_audio_file_name) as source:
                audio = r.record(source, offset=i*15, duration=15)
            row += f"{r.recognize_google(audio,language='ru-RU')}"
            f = open("media/result/transcription.txt", "a", encoding='utf-8')
            f.write(r.recognize_google(audio,language='ru-RU'))
            f.write(" ")
            
        except:
            pass
        bar.next()
        
    f.close()
    bar.finish()

    lack = row.split()

    ###########################################################################
    finish_time = datetime.datetime.now()

    for file in glob.glob("media/files/*"):
        os.remove(file)


    morph = pymorphy2.MorphAnalyzer()
    df = pd.DataFrame(columns = ['наименование', 'номер', 'год', 'завод', 'комментарий'])

    f = open('media/result/transcription.txt', 'r', encoding = "utf-8")
    started_text = f.read()
    text0 = started_text.split()
    text = []


    for el in range(len(text0)):
        p = morph.parse(text0[el])[0]
        word = p.normal_form

        if word == 'колёсный':
            text.append('\n')
            text.append('колесная')
        elif word == 'боковой':
            text.append('\n')
            text.append('боковая')
        elif word == 'следующий':
            continue
        else:
            text.append(text0[el])

    #print(text)

    nabor = []

    indices = [i for i in range(0, len(text)) if text[i]=='\n']

    for ind in range(0, len(indices), 1):
        if ind + 1 <= len(indices) - 1:
            sub_text = text[indices[ind] + 1: indices[ind + 1]]

            nabor.append(sub_text)

    #print(nabor)
    for row0 in nabor:
    #print(row0)

        temp = []
        for x in row0:
            if x not in temp:
                temp.append(x)

        row = temp

        for el in row:
            if el not in row0:
                row.remove(el)

        #print(row)

        name = ''
        number = ''
        year = ''
        factory = ''
        comment = ''

        for index in range(len(row)-1):

            if row[index] == 'колесная': ##### НАДО БУДЕТ ПРОПИСАТЬ РУКАМИ!!!!
                name += 'колесная пара'

            if row[index] == 'боковая':
                name += 'рама боковая'

            #if row[index] == 'номер' and row[index+1].isdigit():
                #number += row[index+1]

            if row[index].isdigit() and 1950 < int(row[index]) < 2023:
                year = row[index]

            if row[index] == 'год' and len(year) != 4:
                if row[index - 1].isdigit() and (1950 < int(row[index - 1]) < 2023 or 0 < int(row[index - 1]) < 100):
                    if 50 < int(row[index - 1]) < 100:
                        year = '19' + row[index - 1]
                    if 0 < int(row[index - 1]) < 23:
                        year += '20' + row[index - 1]

                if row[index + 1].isdigit() and (
                        1950 < int(row[index + 1]) < 2023 or 0 < int(row[index + 1]) < 100) and len(year) != 4:
                    if 50 < int(row[index + 1]) < 100:
                        year = '19' + row[index + 1]
                    if 0 < int(row[index + 1]) < 23:
                        year = '20' + row[index + 1]

            if row[index].isdigit() and 2 < len(row[index]) < 8 and (len(number) + len(row[index])) < 8:
                if int(row[index]) < 1950 or int(row[index]) > 2023:
                    number += row[index]

            if 'китай' in row:
                factory += 'китай'

            if row[index] == 'завод' and len(factory) == 0:
                if row[index+1].isdigit() and len(row[index+1]) != 4:
                    factory = row[index+1]
                elif row[index-1].isdigit() and len(row[index-1]) != 4:
                    factory = row[index-1]

        if 'китай' in row:
            factory = 'китай'

        if 'шайба' in row and 'с' not in row[-1]:
            comment = 'шайба'

        if 'гайка' in row:
            comment = 'гайка'

        if 'шайба' in row and ('с' in row[-1] or 'с' in row[-2]):
            comment = 'шайба, без буксы'

        if 'брак' in row:
            comment = 'брак'

        new_row = {'наименование': name, 'номер': number, 'год': year, 'завод': factory, 'комментарий': comment}
        df = df.append(new_row, ignore_index=True)


    try:
        os.remove("media/result/output.xlsx")
    except:
        pass
    
    df.to_excel("media/result/output.xlsx")

main()