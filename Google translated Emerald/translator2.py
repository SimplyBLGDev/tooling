from multiprocessing.dummy import Array
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
            'arch', 'archimedic', 'archimndabasa', 'arched', 'archimily', 'arthito', 'almighty', 'archimeda', 'arcibis']
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
            'brabricis', 'blabbre', 'pelcore', 'bulpazvfavav', 'polzra', 'brobassers']
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
systemStrings = ["{PAUSE 0x0F}", "{PAUSE_UNTIL_PRESS}", "{PAUSE 15}", "{WAIT SE}", "{PAUSE 64}"]

translator = Translator(service_urls=['translate.google.com'])
translatorLanguageSequence = ['en', 'ru', 'es', 'ja', 'fi', 'ar', 'co', 'zh-CN', 'en']

def readFile(filename):
    printHeader(filename)

    file = open(filename, encoding="UTF-8")
    lines = file.readlines()
    file.close()
    return lines


def printHeader(text):
    print("===========================================", end="")
    print(text, end="")
    print("===========================================")


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


def processText(text, systemEndings, ending):
    maxLinePixelLength = 234
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

    return compileText(lines, systemEndings, ending)


def compileText(lines, systemEndings, ending):
    # \n is a regular line break,
    # \l is a 'wait for user input to continue to the next line' break
    # The textbox in game is two lines long so we do this
    for i in range(len(lines) - 1):
        if i % 2 == 0:
            lines[i] += '\\n'
        else:
            lines[i] += '\l'
    
    lines[-1] += systemEndings + ending # Add original ending to last line (\p or $)

    return lines


def replaceWithDictionary(text, dict):
    for replacer in dict:
        text = text.replace(replacer, dict[replacer])
    
    return text


def changeQuotes(text):
    i = 0
    while text.__contains__('"'):
        ix = text.index('"')
        if i % 2 == 0:
            text = text[:ix] + '“' + text[ix+1:]
        else:
            text = text[:ix] + '”' + text[ix+1:]
        i += 1
    return text


def trimDotString(line):
    text = line.split('.string')[1]
    text = text.strip()
    text = text.strip('\"')
    text = removeFromEnd(text, '\\n')
    text = removeFromEnd(text, '\l')


def removeFromEnd(fr, what):
    if fr.endswith(what):
        return fr[:-len(what)]
    return fr


def getRenderLength(text):
    particularLength = {
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


def compileDotString(lines: Array):
    finalText = ''
    for line in lines:
        finalText += '	.string "' + line + '"\n'
    
    return finalText


def trimUnderscoreString(line):
    start = line.index('"')
    end = line.rindex('"')
    text = line[start+1:end].replace('\\n', ' ').replace('\l', ' ')
    return text, line[:start+1], line[end:]


def replaceUnderscoreString(line):
    text, start, end = trimUnderscoreString(line)
    translated = completeTranslate(text)
    print(translated)
    while len(translated) > 12:
        translated = input("New name: >")
    translated = translated.upper()
    return start + translated + end


def completeTranslate(text):
    final = ''
    lines = separateString(text)
    for realLine in lines:
        for l in subTranslate(realLine):
            final += l
    
    return final


def separateString(text):
    return text.split('\p')


def subTranslate(text):
    text, ending = getSystemEndingsAndTrim(text)
    containsKun = False
    if text.__contains__('{KUN}'):
        text = text.replace('{KUN}', '')
        containsKun = True
    tags = getTags(text)

    ret = ''
    if len(tags) == 0:
        ret = translate(text)
    else:
        ret = manualReplace(text, tags)
        
    if containsKun:
        ret = ret.replace('{PLAYER}', '{PLAYER}{KUN}')
    
    return processText(ret, ending, '')


def manualReplace(ogText, tags = []):
    text = ogText
    if tags == []:
        tags = getTags(text)
    
    print("\nMANUAL REPLACE")
    replacedAll = True
    mrIx = 0
    for tag in tags:
        if mrIx >= len(autoReplace):
            replacedAll = False
            break
        text = text.replace('{' + tag + '}', autoReplace[mrIx]['from'])
        mrIx += 1
    
    if not replacedAll:
        print("Regular:")
        print(text)
        text = input("New regular: ")
    
    text = translate(text)
    print("Translated:")
    print(text)
    if replacedAll:
        text, success = tryAutoReplace(text, tags, mrIx)
        if success:
            print('Auto replaced!')
            print(text)
            return text
    
    print(ogText)
    return input("Final>")


def tryAutoReplace(text, tags, amountReplaced):
    # Go through text looking for some of the to tags within the replaced,
    # If the tag was replaced and we find one of the possible translations
    # in the translated text we replace it and mark it as done if at the
    # end of the routine we found a match for every replaced tag we return
    # the new text string and declare success, otherwise we return false
    # and make the user manually replace

    for ix in range(amountReplaced):
        replacedTag = False
        tagToReplace = '{' + tags[ix] + '}'
        for possibleTranslation in autoReplace[ix]['to']:
            if text.__contains__(possibleTranslation):
                text = text.replace(possibleTranslation, tagToReplace)
                replacedTag = True
                break

            possibleTranslation = possibleTranslation.capitalize()
            if text.__contains__(possibleTranslation):
                text = text.replace(possibleTranslation, tagToReplace)
                replacedTag = True
                break

            possibleTranslation = possibleTranslation.upper()
            if text.__contains__(possibleTranslation):
                text = text.replace(possibleTranslation, tagToReplace)
                replacedTag = True
                break
        
        if not replacedTag:
            return text, False
    
    return text, True


def getTags(text):
    ix = 0
    tags = []
    while text.find('{', ix) != -1:
        start = text.index('{', ix) + 1
        end = text.index('}', ix)
        tags.append(text[start:end])
        ix = end+1
    
    return tags


def replaceUnderscoreFile(filename):
    lines = readFile(filename)
    file = open(filename, "w+", encoding='UTF-8', newline='\n')

    for line in lines:
        if line.__contains__('_("'):
            nL = replaceUnderscoreString(line)
            file.write(nL)
            print(nL, end='')
        else:
            file.write(line)
            print(line, end='')

    file.close()


def getSystemEndingsAndTrim(text):
    for s in systemStrings:
        if text.__contains__(s):
            ending = s * text.count(s)
            text = text.rstrip(s)

            return text, ending
    
    return text, ''


def main():
    rep = os.path.join('src', 'pokeemerald', 'src', 'data', 'trainers.h')
    replaceUnderscoreFile(rep)

if __name__ == '__main__':
    main()
