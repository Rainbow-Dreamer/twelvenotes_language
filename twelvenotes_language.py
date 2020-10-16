'''
Use 12 notes from C to Bb to represent any numbers, letters and symbols.
This is a duodecimal (base 12) system. Use C, C#, D, D#, E, F, F#, G, G#,
A, A#, B to represent 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 in decimal.
Because all of the characters need to be represented in one character,
so use lowercase c to represent C#, d for D#, f for F#, g for G#, a for A#.
So we have:
Decimal:    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ...
Duodecimal: C c D d E F f G g A a  B  cC cc cD cd cE cF cf cG cg ...
For letters and symbols and any other characters, use decimal in the
ASCII and Unicode system and then convert to 12 notes system.
To represent an interval between two characters, just use interval notes
in music(which means don't play any notes at the note)
So we can use music to represent any informations and files.

'''
# Note: can use both of Dg (since the conversion of Dg to decimal is 32,
# the ascii number of " ") and space to represent interval
transdict = {
    0: 'C',
    1: 'c',
    2: 'D',
    3: 'd',
    4: 'E',
    5: 'F',
    6: 'f',
    7: 'G',
    8: 'g',
    9: 'A',
    10: 'a',
    11: 'B'
}
notedict = {
    'C': 'C',
    'c': 'C#',
    'D': 'D',
    'd': 'D#',
    'E': 'E',
    'F': 'F',
    'f': 'F#',
    'G': 'G',
    'g': 'G#',
    'A': 'A',
    'a': 'A#',
    'B': 'B',
    ' ': 'interval'
}
realnotedict = {j: i for i, j in notedict.items()}


def to12notes(a, system=10):
    if system == 10:
        alist = []
        while a != 0:
            current = divmod(a, 12)
            alist.append(transdict[current[1]])
            a = current[0]
        alist.reverse()
        return ''.join(alist)
    else:
        decimal = []
        a = str(a)
        N = len(a)
        decimal = sum([eval(a[i]) * (system**(N - i - 1)) for i in range(N)])
        return to12notes(decimal)


def notels(a):
    return [notedict[i] for i in a]


reversedict = {j: i for i, j in transdict.items()}
reversenotedict = {j: reversedict[i] for i, j in notedict.items() if i != ' '}


def noteto(a, system=10, number=0, mode=0, unit=None, nospace=0):
    if system == 10:
        N = len(a)
        whole = a.split(' ')
        if number == 0:
            if mode == 0:
                return ''.join([
                    chr(
                        sum([
                            reversedict[j[i]] * (12**(len(j) - i - 1))
                            for i in range(len(j))
                        ])) for j in whole
                ])
            else:
                if unit is None:
                    return 'a unit of split standard must be provided'
                else:
                    if nospace == 0:
                        return ' '.join([
                            ''.join([
                                noteto(j[i:i + unit])
                                for i in range(0, len(j), unit)
                            ]) for j in whole
                        ])
                    else:
                        return ''.join([
                            noteto(a[i:i + unit])
                            for i in range(0, len(a), unit)
                        ])

        else:
            if mode == 0:
                every = [
                    sum([
                        reversedict[j[i]] * (12**(len(j) - i - 1))
                        for i in range(len(j))
                    ]) for j in whole
                ]
            else:
                if unit is None:
                    return 'a unit of split standard must be provided'
                else:
                    if nospace == 0:
                        every = [[
                            noteto(j[i:i + unit], number=1)
                            for i in range(0, len(j), unit)
                        ] for j in whole]
                    else:
                        return [
                            noteto(a[i:i + unit], number=1)
                            for i in range(0, len(a), unit)
                        ]
            return every if len(every) > 1 else every[0]

    else:
        N = len(a)
        decimal = noteto(a, 10, 1, mode, unit, nospace)
        if type(decimal) != list:
            decimal = [decimal]
        if type(decimal[0]) != list:
            decimal = [decimal]
        result = []
        for j in decimal:
            unitlist = []
            for i in j:
                alist = []
                while i != 0:
                    current = divmod(i, system)
                    alist.append(str(current[1]))
                    i = current[0]
                alist.reverse()
                unitlist.append(''.join(alist))
            result.append(unitlist)
        if len(result) == 1:
            return result[0] if len(result[0]) > 1 else result[0][0]
        else:
            return result


def convert(a, mode=0, maxlen=None, nospace=0):
    if type(a) != str:
        a = str(a)
    if mode == 0:
        current = [ord(i) for i in a]
        return ' '.join([to12notes(j) for j in current])
    else:
        if nospace == 0:
            current = a.split(' ')
        else:
            current = a
        tempmaxlen = max([len(''.join(to12notes(ord(i)))) for i in a])
        if maxlen is None:
            maxlen = tempmaxlen
        else:
            if maxlen < tempmaxlen:
                maxlen = tempmaxlen
        temp = []
        for i in current:
            newstr = ''
            for j in i:
                new = ''.join([to12notes(ord(j))])
                new = 'C' * (maxlen - len(new)) + new
                newstr += new
            temp.append(newstr)
        if nospace == 0:
            return ' '.join(temp)
        else:
            return ''.join(temp)


def convertfile(path,
                name='twelve notes conversion.txt',
                mode=0,
                maxlen=None,
                nospace=0):
    with open(path, "r") as f:
        data = f.read()
        with open(name, "w") as new:
            new.write(convert(data, mode, maxlen, nospace))


def transfile(path,
              name='twelve notes translation.txt',
              mode=0,
              unit=None,
              nospace=0):
    with open(path, "r") as f:
        data = f.read()
        with open(name, "w") as new:
            new.write(noteto(data, 10, 0, mode, unit, nospace))


def tonotels(a, combine=0, bychar=0):
    current = convert(a)
    result = current.split('Dg')
    if combine == 0:
        if bychar == 0:
            return [notels(i.replace(' ', '')) for i in result]
        else:
            return [[notels(i) for i in j.split()] for j in result]
    else:
        return [notedict[i] for i in current]


def tonotelsfile(path,
                 name='twelve notes conversion list.txt',
                 combine=0,
                 bychar=0):
    with open(path, "r") as f:
        data = f.read()
        with open(name, "w") as new:
            new.write(str(tonotels(data, combine, bychar)))


def torealnotes(a, combine=0, bychar=0, mode=0):
    if mode == 0:
        result = a.split('Dg')
    else:
        result = a.split()
    if combine == 0:
        if bychar == 0:
            return [notels(i.replace(' ', '')) for i in result]
        else:
            return [[notels(i) for i in j.split()] for j in result]
    else:
        return [notedict[i] for i in a]


def torealnotesfile(path,
                    name='torealnotes conversion.txt',
                    combine=0,
                    bychar=0,
                    mode=0):
    with open(path, "r") as f:
        data = f.read()
        with open(name, "w") as new:
            new.write(str(torealnotes(data, combine, bychar, mode)))


def realnoteto(a, number=0):
    # example:
    # realnoteto([['C', 'F', 'G'], ['F', 'A']]) = 'CE'
    # realnoteto([['C', 'F', 'G'], ['F', 'A']], number = 1) = [67, 69]
    if type(a[0]) != list:
        a = [a]
    if number == 0:
        every = [
            chr(
                sum([
                    reversenotedict[j[i]] * (12**(len(j) - i - 1))
                    for i in range(len(j))
                ])) for j in a
        ]
        return ''.join(every)
    else:
        every = [
            sum([
                reversenotedict[j[i]] * (12**(len(j) - i - 1))
                for i in range(len(j))
            ]) for j in a
        ]
        return every


def realnoteto12notes(a):
    # the opposite are notels and tonotels
    if type(a[0]) != list:
        a = [a]
    every = ' '.join([''.join([realnotedict[j] for j in i]) for i in a])
    return every


def realnotefile(path, name='real note translation.txt', number=0):
    with open(path, "r") as f:
        data = f.read()
        with open(name, "w") as new:
            new.write(realnoteto(data, number))


trans = noteto