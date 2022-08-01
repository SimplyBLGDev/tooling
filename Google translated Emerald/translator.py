from concurrent.futures import process
import os
from googletrans import Translator

class DialogPiece:
    lines = ""


translator = Translator(service_urls=['translate.google.com'])
translatorLanguageSequence = ['en', 'ru', 'es', 'ja', 'fi', 'ar', 'co', 'zh-CN', 'en']
manualAlerts = ["{PLAYER}", "{KUN}", "{STR_VAR_1}", "{STR_VAR_2}", "{STR_VAR_3}", "{POKEBLOCK}", "{PLUS}", "{PAUSE 0x0F}",
    "{PAUSE_UNTIL_PRESS}", "{", "}", "{PAUSE 15}", "{STRING 5}"]
systemStrings = ["{PAUSE 0x0F}", "{PAUSE_UNTIL_PRESS}", "{PAUSE 15}"]
replacersFrom = {
    "…": "..."
}
replacersTo = {
    "...": "…"
}
skipFiles = []
# Archimede
brAutoReplace = ['archimedes', 'alkaline', 'archimede', 'alchimeds', 'archimède', 'alcimede', 'alkinomed', 'archimidis', 'alkimede',
            'archimede', 'archime', 'alcimide', 'alkimed', 'archimidy', 'alchimede', 'alkimid', 'akimiad', 'artemito', 'archmidis',
            'alkimé', 'alkimen', 'archmidis', 'archimito', 'archmids', 'arcimter', 'akim', 'archimo', 'archimids', 'arquimes', 'archimides',
            'arcimed', 'arcimato', 'alkali', 'rchimedo', 'alachi', 'aquida', 'archimida', 'archimid', 'arimedes', 'arthrica', 'achimidi',
            'achimid', 'alkyamide', 'artemidy', 'alkimiaudia', 'archoid', 'abamid', 'achi', 'alkimde', 'arnimiy', 'achimir', 'arnimidy',
            'abund', 'akhimi', 'architect', 'alchemy', 'achipbaba', 'arnimedes', 'archimrid', 'aquid', 'archimidi', 'archiminduus',
            'alkimde', 'aksimi', 'alaba', 'archedri', 'albasov', 'archae', 'arrezi', 'arvi', 'arisette', 'akimidblbas', 'archimedavr',
            'arch', 'archimedic', 'archimndabasa', 'arched', 'archimily', 'arthito', 'almighty', 'archimeda', 'arcibis', 'aclimedes',
            'alkimea', 'elkimid', 'arthrito']

# Bulbasaur
br2AutoReplace = ['bolvasorus', 'bazer', 'brobsaurus', 'bolvassorus', 'bolbbazaur', 'bulbasavr', 'bulbasaur', 'bulbasavr', 'borbazor',
            'bokimon sabra', 'bolbeze', 'stachfassorus', 'bolbas', 'borva soros', 'bulbabastaur', 'popsurus', 'brobroaurus', 'borosol',
            'propassuso', 'bulbasvr', 'bulbrr', 'bulbazaur', 'bululasiaur', 'brobashaurus', 'brobashaur', 'bulb', 'brassur', 'brazil',
            'polbas', 'bulasaur', 'bulasaaf', 'porazoros', 'propassorus', 'brobashaurus', 'brunado', 'boorbassoors', 'bulbasvr', 'bulbasurur',
            'bulBrr', 'bulbrr', 'brobashaur', 'bilassavra', 'bulbasav', 'blapapafs', 'bRunado', 'bullabasore', 'brobbasaurus', 'porpasoros',
            'babas', 'bulbasor', 'propassor', 'polipassover', 'bulawsau', 'barcelona', 'bulasaur', 'bulbassav', 'bulasaur', 'bulbazuvr',
            'bulabasv', 'bulbasaverr', 'blabavr', 'bolbawazor', 'brawlsr', 'bulbass', 'porpasses', 'bulbrr', 'procabo', 'binbin',
            'popuser', 'bilbassur', 'bilbassafer', 'brobashaur', 'blaghasafin', 'prasororus', 'porpassor', 'bulbazuru', 'bulbalon',
            'brabricis', 'blabbre', 'pelcore', 'bulpazvfavav', 'polzra', 'bulabavara', 'porbasoros']

def crawl(dest):
    valdi = False
    for subdir in os.listdir(dest):
        if subdir != '.gitignore':
            if os.path.isdir(os.path.join(dest, subdir)):
                if subdir == 'BattleFrontier_BattleTowerMultiPartnerRoom':
                    valdi = True
                if subdir == 'BirthIsland_Harbor':
                    valdi = False
                if valdi:
                    for file in os.listdir(os.path.join(dest, subdir)):
                        if file.endswith('scripts.inc'):
                            fullPath = os.path.join(dest, subdir, file)
                            lines = readFile(fullPath)
                            translateAndWriteFile(lines, fullPath)


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


def translateAndWriteFile(originalLines, filename):
    def finishTextBlock(trimmed):
        ending = ''
        if trimmed.endswith('$'):
            trimmed = removeFromEnd(trimmed, '$')
            ending = '$'
        else:
            trimmed = removeFromEnd(trimmed, '\p')
            ending = '\p'
        
        trimmed, systemEndings = getSystemEndingsAndTrim(trimmed)

        if shouldbeManuallyReplaced(trimmed):
            trimmed = manuallyReplace(trimmed)
        else:
            trimmed = translate(trimmed)

        trimmed = changeQuotes(trimmed)
        trimmed += systemEndings

        processAndWrite(trimmed, ending)
    

    def processAndWrite(text, ending):
        toWrite = processText(text, ending)
        file.write(toWrite)
        print(toWrite, end='')


    file = open(filename, "w+", encoding='UTF-8', newline='\n')
    parsed = ''

    for line in originalLines:
        if line.__contains__('.string'):
            trimmed = trimTextLine(line)
            if parsed != '':
                parsed += ' ' # Fuse different lines with spaces
            parsed += trimmed

            # End of text block or paragraph break, translate and write
            if parsed.endswith('$') or parsed.endswith('\p'):
                finishTextBlock(parsed)
                parsed = ''
        else:      
            file.write(line)
            print(line, end='')
    
    file.close()


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


def getSystemEndingsAndTrim(text):
    if stringContainsOneOf(text, systemStrings):
        pass
    else:
        return text, ''
    
    for s in systemStrings:
        if text.__contains__(s):
            ending = s * text.count(s)
            text = text.rstrip(s)

            return text, ending
    
    return text, ''


def removeFromEnd(fr, what):
    if fr.endswith(what):
        return fr[:-len(what)]
    return fr


def trimTextLine(line):
    text = line.split('.string')[1]
    text = text.strip()
    text = text.strip('\"')
    text = removeFromEnd(text, '\\n')
    text = removeFromEnd(text, '\l')
    text = replaceWithDictionary(text, replacersFrom)
    
    return text


def shouldbeManuallyReplaced(text):
    return stringContainsOneOf(text, manualAlerts)


def manuallyReplace(text):
    containsKun = False
    if text.__contains__('{PLAYER}{KUN}'):
        text = text.replace('{KUN}', '')
        containsKun = True

    defaultReplace = text.replace('{PLAYER}', 'Archimede').replace('{STR_VAR_1}', 'Bulbasaur')
    defaultReplace = defaultReplace.replace('{STR_VAR_2}', 'Chanodler').replace('{STR_VAR_3}', 'Monica')
    defaultReplace = defaultReplace.replace('{POKEBLOCK}', 'Jorge')

    if text.count('{STR_VAR_2}') + text.count('{POKEBLOCK}') + text.count('{STR_VAR_3}') == 0:
        if text.count('{STR_VAR_1}') + text.count('{PLAYER}') > 0:
            # Auto replace
            replacer = ''
            if text.__contains__('{PLAYER}'):
                replacer = '{PLAYER}'
                if containsKun:
                    replacer += '{KUN}'
            elif text.__contains__('{STR_VAR_1}'):
                replacer = '{STR_VAR_1}'

            ar = autoReplace(translate(defaultReplace),  replacer)
            if ar != False:
                return ar

    print(text)
    print(defaultReplace)
    translated = translate(defaultReplace)
    print("Translated:")
    print(translated)
    print("Input final value:")
    final = input()
    if final == '':
        return translated
    else:
        return final


def autoReplace(text, replacer):
    replacerIx = brAutoReplace
    if replacer == '{STR_VAR_1}':
        replacerIx = br2AutoReplace
    should = False
    ret = text
    for r in replacerIx:
        rr = r
        if ret.__contains__(rr):
            ret = ret.replace(rr, replacer)
            should = True
        rr = r.capitalize()
        if ret.__contains__(rr):
            ret = ret.replace(rr, replacer)
            should = True
        rr = r.upper()
        if ret.__contains__(rr):
            ret = ret.replace(rr, replacer)
            should = True
    
    if should:
        return ret
    else:
        print("Auto replace failed")
        return False


def processText(text, ending):
    text, systemEndings = getSystemEndingsAndTrim(text)
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

    return compileFinalText(lines, systemEndings, ending)


def compileFinalText(lines, systemEndings, ending):
    # \n is a regular line break,
    # \l is a 'wait for user input to continue to the next line' break
    # The textbox in game is two lines long so we do this
    for i in range(len(lines) - 1):
        if i % 2 == 0:
            lines[i] += '\\n'
        else:
            lines[i] += '\l'
    
    lines[-1] += systemEndings + ending # Add original ending to last line (\p or $)
    
    finalText = ''
    for line in lines:
        finalText += '	.string "' + line + '"\n'
    
    return finalText


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


def replaceAllOf(text, what, to):
    for replacer in what:
        text = text.replace(replacer, to)
    
    return text


def stringContainsOneOf(s, contained):
    for c in contained:
        if s.__contains__(c):
            return True
    return False


def replaceWithDictionary(text, dict):
    for replacer in dict:
        text = text.replace(replacer, dict[replacer])
    
    return text


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


def translateAndWriteLinear(originalLines, filename):
    file = open(filename, "w+", encoding='UTF-8', newline='\n')

    for line in originalLines:
        if line.__contains__('_("")'):
            parsed = parseLinear(line)
        else:
            file.write(line)
            print(line, end='')

    file.close()


def parseLinear(line):
    indexOfFirstQuote = line.index('"')
    indexOfLastQuote = line.rindex('"')
    return line[indexOfFirstQuote:indexOfLastQuote].replace('\\n', ' ').replace('\l', ' ').replace('\p', '')


def translateLinear(text):
    skips = ['PALETTE', 'COLOR', 'PAUSE', 'ESCAPE', 'ARROW', 'CLEAR_TO', 'WAIT']

    if stringContainsOneOf(text, skips):
        return trueManualTranslate(text)
    
    
def trueManualTranslate(text):
    print(text)
    tt = input('>')
    
    if tt == '':
        tt = text
    elif tt == '-':
        return text
    
    translated = translate(tt)
    print(translated)
    yy = input()
    
    if yy == '':
        yy = translated
    
    return yy


def  main():
    crawl(os.path.join('src', 'pokeemerald', 'data', 'maps'))


def checkAllFilesInDirForTripleQuotes(dest):
    for file in os.listdir(dest):
        fullPath = os.path.join(dest, file)
        lines = readFile(fullPath)
        for line in lines:
            if line.count('"') >= 3:
                print(file)
                print(line)

if __name__ == '__main__':
    if input("Input something to acces simple translation:") == '':
        main()
    else:
        print(translate(input("Translate what?")))
