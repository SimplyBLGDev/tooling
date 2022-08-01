import os
from googletrans import Translator

autoReplace = [
    {'from': 'Archimede',
        'to': ['archimedes', 'alkaline', 'archimede', 'alchimeds', 'archimède', 'alcimede', 'alkinomed', 'archimidis', 'alkimede',
            'archimede', 'archime', 'alcimide', 'alkimed', 'archimidy', 'alchimede', 'alkimid', 'akimiad', 'artemito', 'archmidis',
            'alkimé', 'alkimen', 'archmidis', 'archimito', 'archmids', 'arcimter', 'akim', 'archimo', 'archimids', 'arquimes', 'archimides',
            'arcimed', 'arcimato', 'alkali', 'rchimedo', 'alachi', 'aquida', 'archimida', 'archimid', 'arimedes', 'arthrica', 'achimidi',
            'achimid', 'alkyamide', 'artemidy', 'alkimiaudia', 'archoid', 'abamid', 'achi', 'alkimde', 'arnimiy', 'achimir', 'arnimidy',
            'abund', 'akhimi', 'architect', 'alchemy', 'achipbaba', 'arnimedes', 'archimrid', 'aquid', 'archimidi', 'archiminduus',
            'alkimde', 'aksimi', 'alaba', 'archedri', 'albasov', 'archae', 'arrezi', 'arvi', 'arisette', 'akimidblbas', 'archimedavr',
            'arch', 'archimedic', 'archimndabasa', 'arched', 'archimily', 'arthito', 'almighty', 'archimeda', 'arcibis', 'aclimedes',
            'alkimea']
    },
    {'from': 'Bulbasaur',
        'to': ['bolvasorus', 'bazer', 'brobsaurus', 'bolvassorus', 'bolbbazaur', 'bulbasavr', 'bulbasaur', 'bulbasavr', 'borbazor',
            'bokimon sabra', 'bolbeze', 'stachfassorus', 'bolbas', 'borva soros', 'bulbabastaur', 'popsurus', 'brobroaurus', 'borosol',
            'propassuso', 'bulbasvr', 'bulbrr', 'bulbazaur', 'bululasiaur', 'brobashaurus', 'brobashaur', 'bulb', 'brassur', 'brazil',
            'polbas', 'bulasaur', 'bulasaaf', 'porazoros', 'propassorus', 'brobashaurus', 'brunado', 'boorbassoors', 'bulbasvr', 'bulbasurur',
            'bulBrr', 'bulbrr', 'brobashaur', 'bilassavra', 'bulbasav', 'blapapafs', 'bRunado', 'bullabasore', 'brobbasaurus', 'porpasoros',
            'babas', 'bulbasor', 'propassor', 'polipassover', 'bulawsau', 'barcelona', 'bulasaur', 'bulbassav', 'bulasaur', 'bulbazuvr',
            'bulabasv', 'bulbasaverr', 'blabavr', 'bolbawazor', 'brawlsr', 'bulbass', 'porpasses', 'bulbrr', 'procabo', 'binbin',
            'popuser', 'bilbassur', 'bilbassafer', 'brobashaur', 'blaghasafin', 'prasororus', 'porpassor', 'bulbazuru', 'bulbalon',
            'brabricis', 'blabbre', 'pelcore', 'bulpazvfavav', 'polzra']
    },
    {'from': 'Lugia',
        'to': ['lugia', 'lugo', 'louis', 'luga', 'lugian', 'lugi', 'logia', 'july', 'logana', 'logya', 'ligny', 'loggia', 'ligid', 'lupia',
            'loghe', 'lu jia', 'lu Jia', 'luga']
    },
    {'from': 'Kyogre',
        'to': ['kyogre', 'kyogrenn', 'kogore', 'kiigra', 'kyogrren']
    }
]
replacersFrom = {
    "…": "..."
}
replacersTo = {
    "...": "…"
}
systemStrings = ["PAUSE", "WAIT"]

translator = Translator(service_urls=['translate.google.com'])
translatorLanguageSequence = ['en', 'ru', 'es', 'ja', 'fi', 'ar', 'co', 'zh-CN', 'en']


def translate(text):
    if text == '':
        return ''

    while True:
        newText = text
        try:
            for i in range(1, len(translatorLanguageSequence)):
                newText = translator.translate(newText,
                        src=translatorLanguageSequence[i-1],
                        dest=translatorLanguageSequence[i]).text
            
            return newText
        except:
            input("Error:")


def singleLineStringTrim(text):
    start = text.index('"')
    end = text.rindex('"')
    return text[:start], text[start+1:end], text[end:]


def getAllPokedexEntries(lines):
    headers = []
    entries = []
    newEntry = ''

    for line in lines:
        if line == '\n' or line.__contains__('//'):
            continue
        if line.count('"') >= 2:
            start, trimmed, end = singleLineStringTrim(line)
            if newEntry != '':
                newEntry += ' '
            newEntry += trimmed.replace('\\n', '')

            if end.__contains__(');'):
                entries.append(newEntry)
                newEntry = ''
        else:
            headers.append(line)
    
    return headers, entries


def replaceWithDictionary(text, dict):
    for replacer in dict:
        text = text.replace(replacer, dict[replacer])
    
    return text


def processText(text):
    maxLinePixelLength = 150
    lines = []
    text = replaceWithDictionary(text, replacersTo)

    words = text.split(' ')
    line = ''
    lineLen = 0

    for word in words:
        wordLen = getRenderLength(word)
        if lineLen + wordLen > maxLinePixelLength:
            lines.append(line)
            line = ''
            lineLen = 0
        
        if line != '':
            line += ' '
        line += word
        lineLen = getRenderLength(line)
    
    lines.append(line)

    return compileFinalText(lines)


def compileFinalText(lines):
    # \n is a regular line break,
    # \l is a 'wait for user input to continue to the next line' break
    # The textbox in game is two lines long so we do this
    for i in range(len(lines) - 1):
        if i % 2 == 0:
            lines[i] += '\\n'
        else:
            lines[i] += '\\n'
    
    finalText = ''
    for line in lines:
        finalText += '    "' + line + '"\n'
    
    return finalText


def getRenderLength(text):
    particularLength = {
        ' ': 3,
        '=': 8,
        ';': 3,
        '!': 4,
        '.': 3,
        ':': 3,
        ',': 3,
        'x': 7,
        'i': 4,
        'r': 5,
        'j': 5,
        '&': 7,
    }
    l = 0
    for letter in text:
        if letter in particularLength:
            l += particularLength[letter]
        else:
            l += 6

    return l


def translatePokedexTextFile(filename):
    lines = []
    with open(filename, encoding='UTF-8') as f:
        lines = f.readlines()
    
    headers, entries = getAllPokedexEntries(lines)

    with open(filename, "w+", encoding='UTF-8', newline='\n') as f:
        for i in range(len(headers)):
            f.write(headers[i])
            print(headers[i], end='')
            entries[i] = processText(entries[i])
            f.write(entries[i] + ');\n')
            print(entries[i] + ');')


translatePokedexTextFile(os.path.join('src', 'pokeemerald', 'src', 'data', 'text', 'move_descriptions.h'))
