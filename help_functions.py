def notels(a):
    return [notedict[i] for i in a]


def torealnotes(a, mode=0):
    if mode == 0:
        result = a.split('Dg')
    else:
        result = a.split()
    return [[notedict[i] for i in j] for j in result]


def read12notesfile(path, mode=0):
    with open(path) as f:
        data = f.read()
        result = torealnotes(data, mode)
    return result


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


def tochords(a,
             pitch=4,
             combine=0,
             interval_unit=0.5,
             rest_unit=1,
             has_interval=0):
    if type(a[0]) != list:
        a = [a]
    if has_interval == 0:
        chordls = [
            chord([note(j, pitch)
                   for j in i], interval=interval_unit).rest(rest_unit)
            for i in a
        ]
    else:
        chordls = []
        for i in a:
            newchord = []
            N = len(i)
            newinterval = []
            for k in range(N):
                now = i[k]
                if now != 'interval':
                    newchord.append(note(now, pitch))
                    if k != N - 1 and i[k + 1] == 'interval':
                        newinterval.append(interval_unit + rest_unit)
                    else:
                        newinterval.append(interval_unit)
            chordls.append(chord(newchord, interval=newinterval))
    if combine == 0:
        return chordls
    else:
        return chord([j for i in chordls for j in i],
                     interval=[j for i in chordls for j in i.interval])


def tochordsfile(path,
                 pitch=4,
                 combine=0,
                 interval_unit=0.5,
                 rest_unit=1,
                 has_interval=0,
                 mode=0,
                 splitway=0,
                 combine1=0,
                 bychar=0):
    # mode == 0: open the real notes file and eval the nested by first checking if it is started with [[
    # mode == else: open the file written in 12notes language and translate to real notes
    # splitway == 0/1: corresponding to the mode == 0/1 in real notes translation
    with open(path) as f:
        data = f.read()
        if mode == 0:
            if data[:2] == '[[':
                data = eval(data)
                result = tochords(data, pitch, combine, interval_unit,
                                  rest_unit, has_interval)
            else:
                result = 'not a valid real notes file'
        else:
            data = torealnotes(data, combine1, bychar, splitway)
            result = tochords(data, pitch, combine, interval_unit, rest_unit,
                              has_interval)
    return result
