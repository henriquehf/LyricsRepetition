from collections import Counter

def bitFiller(string, size):
    while(len(string) < size):
        string = "0" + string
    return string

def pointerGen(pos, size):
    str_bin = "1"
    str_pos = bin(pos).replace("0b","")
    str_pos = bitFiller(str_pos, 13)
    str_siz = bin(size).replace("0b","")
    str_siz = bitFiller(str_siz, 13)
    str_bin = str_bin + str_pos + str_siz
    pointer = chr(int(str_bin[0:9],2)) + chr(int(str_bin[9:18],2)+14) + chr(int(str_bin[18:27],2)+14)
    return pointer

def pointerDeco(char1, char2, char3):
    str1 = bin(int(ord(char1))).replace("0b","")
    str1 = bitFiller(str1, 9)
    str2 = bin(int(ord(char2))-14).replace("0b","")
    str2 = bitFiller(str2, 9)
    str3 = bin(int(ord(char3))-14).replace("0b","")
    str3 = bitFiller(str3, 9)
    strt = str1 + str2 + str3
    pos = int(strt[1:14], 2)
    tim = int(strt[14:27], 2)
    return pos, tim

def lyricCompress(lyric):
    aux_curr = 0
    aux_comp = 0
    com_lyrics = ""
    while (aux_curr<len(lyric)):
        cur_rep_size = 0
        rep_size = 0
        aux_rep = 0
        cur_aux_comp = 0
        for aux_comp in range(0, aux_curr+1): #aux_comp vai de 0 até aux_curr
            if (lyric[aux_comp] == lyric[aux_curr] and aux_comp < aux_curr):
                aux_rep = aux_comp
                aux_curr2 = aux_curr
                rep_size = 0
                while (lyric[aux_rep] == lyric[aux_curr2]):
                    rep_size += 1
                    aux_rep += 1
                    aux_curr2 += 1
                    if (aux_curr2 == len(lyric)):
                        break
            if (rep_size>cur_rep_size):
                cur_aux_comp = aux_comp
                cur_rep_size = rep_size
                cur_aux_curr2 = aux_curr2
        if (cur_rep_size > 3):
            string = pointerGen(cur_aux_comp, cur_rep_size)
            com_lyrics = com_lyrics + string
            aux_curr = cur_aux_curr2
        else:
            com_lyrics = com_lyrics + lyric[aux_comp]
            aux_curr += 1
    return com_lyrics

def lyricDecompress(string):
    decode_lyric = ""
    x = 0
    while(x < len(string)):
        if (int(ord(string[x])) < 256):
            decode_lyric = decode_lyric + string[x]
            x += 1
        else:
            pos, tim = pointerDeco(string[x], string[x+1], string[x+2])
            for y in range(0, tim):
                decode_lyric = decode_lyric + decode_lyric[pos+y]
            x += 3
    return decode_lyric

def cleanLyric(lyric):
    lyric2 = ""
    for char in lyric:
        if (ord(char) < 256):
            lyric2 = lyric2 + char
    return lyric2.lower()

def syllableCount(word):
    syl = 0
    n = 0
    vog = 0
    con = 0
    while(n < len(word)):
        if word[n] in 'aeiouy':
            while(word[n] in 'aeiouy'):
                vog += 1
                n += 1
                if(n == len(word)):
                    break
            syl += 1
        elif(word[n] in 'bcdfghjklmnpqrstvwxz'):
            ch = word[n]
            con += 1
            while(word[n] == ch):
                n += 1
                if(n == len(word)):
                    break
        else:
            n += 1
    return syl, vog, con

def hardWord(word):
    syl, vog, con = syllableCount(word)
    if((syl > 3 and con > vog) or (len(word) > 12)):
        return True
    return False

def hardWords(lyric):
    string = lyric.split()
    string2 = []
    n = 0
    for word in string:
        if(word not in string2):
            if(hardWord(word)):
                string2.insert(n, word)
                #print(word)
                n += 1
    return n

def repetCalculator(string):
    str1 = cleanLyric(string)
    str2 = lyricCompress(str1)
    hw = hardWords(str1)
    rep = round((1 - len(str2)/len(str1))*100,2)
    str3 = lyricDecompress(str2)
    dictionary = countWords(str1)
    return rep, len(str2), str3 == str1, hw, dictionary

def countWords(string):
    words = listWords(string)
    dictionary = Counter(words).most_common()
    return dictionary

def listWords(string):
    aux = string.lower()
    words = aux.split()
    for a in range(0, len(words)):
        while(len(words[a])!= 0 and not words[a][0].isdigit() and not words[a][0].isalpha()):
            words[a] = words[a][1:]
        while(len(words[a])!= 0 and not words[a][len(words[a])-1].isdigit() and not words[a][len(words[a])-1].isalpha()):
            words[a] = words[a][:len(words[a])-1]
    return words


# lyric = "Tonight, I'm gonna have myself a real good time I feel alive and the world I'll turn it inside out, yeah And floating around in ecstasy So don't stop me now don't stop me 'Cause I'm having a good time, having a good time I'm a shooting star, leaping through the sky Like a tiger defying the laws of gravity I'm a racing car, passing by like Lady Godiva I'm gonna go, go, go There's no stopping me I'm burnin' through the sky, yeah Two hundred degrees That's why they call me Mister Fahrenheit I'm traveling at the speed of light I wanna make a supersonic man out of you Don't stop me now, I'm having such a good time I'm having a ball Don't stop me now If you wanna have a good time, just give me a call Don't stop me now ('cause I'm having a good time) Don't stop me now (yes, I'm havin' a good time) I don't want to stop at all Yeah, I'm a rocket ship on my way to Mars On a collision course I am a satellite, I'm out of control I am a sex machine, ready to reload Like an atom bomb about to Oh, oh, oh, oh, oh explode I'm burnin' through the sky, yeah Two hundred degrees That's why they call me Mister Fahrenheit I'm traveling at the speed of light I wanna make a supersonic woman of you Don't stop me, don't stop me Don't stop me, hey, hey, hey Don't stop me, don't stop me Ooh ooh ooh, I like it Don't stop me, don't stop me Have a good time, good time Don't stop me, don't stop me, ah Oh yeah Alright Oh, I'm burnin' through the sky, yeah Two hundred degrees That's why they call me Mister Fahrenheit I'm traveling at the speed of light I wanna make a supersonic man out of you Don't stop me now, I'm having such a good time I'm having a ball Don't stop me now If you wanna have a good time (wooh) Just give me a call (alright) Don't stop me now ('cause I'm having a good time, yeah yeah) Don't stop me now (yes, I'm havin' a good time) I don't want to stop at all La da da da daah Da da da haa Ha da da ha ha haaa Ha da daa ha da da aaa Ooh ooh ooh"
# words = countWords(lyric)
# for word in words:
#     print(word[0], word[1])

