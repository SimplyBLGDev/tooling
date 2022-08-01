from email import header
import os

from googletrans import Translator

autoReplace = [
    {'from': '{STR_VAR_1}',
        'to': ['archimedes', 'alkaline', 'archimede', 'alchimeds', 'archimède', 'alcimede', 'alkinomed', 'archimidis', 'alkimede',
            'archimede', 'archime', 'alcimide', 'alkimed', 'archimidy', 'alchimede', 'alkimid', 'akimiad', 'artemito', 'archmidis',
            'alkimé', 'alkimen', 'archmidis', 'archimito', 'archmids', 'arcimter', 'akim', 'archimo', 'archimids', 'arquimes', 'archimides',
            'arcimed', 'arcimato', 'alkali', 'rchimedo', 'alachi', 'aquida', 'archimida', 'archimid', 'arimedes', 'arthrica', 'achimidi',
            'achimid', 'alkyamide', 'artemidy', 'alkimiaudia', 'archoid', 'abamid', 'achi', 'alkimde', 'arnimiy', 'achimir', 'arnimidy',
            'abund', 'akhimi', 'architect', 'alchemy', 'achipbaba', 'arnimedes', 'archimrid', 'aquid', 'archimidi', 'archiminduus',
            'alkimde', 'aksimi', 'alaba', 'archedri', 'albasov', 'archae', 'arrezi', 'arvi', 'arisette', 'akimidblbas', 'archimedavr',
            'arch', 'archimedic', 'archimndabasa', 'arched', 'archimily', 'arthito', 'almighty', 'archimeda', 'arcibis', 'armimade',
            'alkimea', 'elkimid', 'arthrito', 'archimedeimedede', 'ashimidi', 'arshimids', 'arshmids', 'alkimeDes', 'akhide',
            'arthudes', 'alchemedes', 'arismas', 'alkimelagi', 'aalki', 'arimormian', 'acrgimidin', 'alcimeDes', 'alchimea',
            'armimedus', 'aldimad', 'akhemi', 'armsics', 'alcheTyes', 'alkane', 'alkyl', 'alimeDes', 'arshidi', 'altimeDes', 'alchemege']
    },
    {'from': '{STR_VAR_2}',
        'to': ['bulbasaur', 'bolvasorus', 'bazer', 'brobsaurus', 'bolvassorus', 'bolbbazaur', 'bulbasavr', 'bulbasaur', 'bulbasavr', 'borbazor',
            'bokimon sabra', 'bolbeze', 'stachfassorus', 'bolbas', 'borva soros', 'bulbabastaur', 'popsurus', 'brobroaurus', 'borosol',
            'propassuso', 'bulbasvr', 'bulbrr', 'bulbazaur', 'bululasiaur', 'brobashaurus', 'brobashaur', 'bulb', 'brassur', 'brazil',
            'polbas', 'bulasaur', 'bulasaaf', 'porazoros', 'propassorus', 'brobashaurus', 'brunado', 'boorbassoors', 'bulbasvr', 'bulbasurur',
            'bulBrr', 'bulbrr', 'brobashaur', 'bilassavra', 'bulbasav', 'blapapafs', 'bRunado', 'bullabasore', 'brobbasaurus', 'porpasoros',
            'babas', 'bulbasor', 'propassor', 'polipassover', 'bulawsau', 'barcelona', 'bulbassav', 'bulbazuvr', 'borbasor', 'barbascar',
            'bulabasv', 'bulbasaverr', 'blabavr', 'bolbawazor', 'brawlsr', 'bulbass', 'porpasses', 'bulbrr', 'procabo', 'binbin','brobiara',
            'popuser', 'bilbassur', 'bilbassafer', 'brobashaur', 'blaghasafin', 'prasororus', 'porpassor', 'bulbazuru', 'bulbalon', 'broviara',
            'brabricis', 'blabbre', 'pelcore', 'bulpazvfavav', 'polzra', 'brobassers', 'bulabavara', 'porbasoros', 'borrazor', 'porpasor',
            'bulbasaurasaur', 'busbed', 'bulbasaurassav', 'boubas', 'bravi', 'porpassers', 'boreva', 'bazoul', 'brobliuri', 'perbazorus',
            'bulsaur', 'bulasavrin', 'bolpinavra', 'polarbas', 'bulasavr', 'brewasaurus', 'boldzor', 'bulBrr', 'borabasaurus', 'brabras'
            'porassorus', 'porbasous', 'bolpassur', 'portasurer', 'badbazaul', 'balsovari', 'brabast', 'porvasorus', 'bulasar', 'bllabasau'
            'babbassur', 'bazari', 'brewsub', 'bilbazor', 'basavra', 'borbazeur', 'bourbasavurl', 'borobazabra', 'brobrasaurus', 'bulasvr',
            'borbasauraor', 'borbasaus', 'borbasa', 'borbador', 'borzing', 'bolbazu', 'belbaz', 'bourovasauro', 'porabasorus', 'burvasaurus',
            'procbonne', 'bruzur', 'bolibazor', 'polibazor']
    },
    {'from': '{STR_VAR_3}',
        'to': ['lugia', 'lugo', 'louis', 'luga', 'lugian', 'lugi', 'logia', 'july', 'logana', 'logya', 'ligny', 'loggia', 'ligid', 'lupia',
            'loghe', 'lu jia', 'lu Jia', 'luga', 'lunga', 'lungia', 'lunger', 'liagio', 'loga', 'loesakazorus', 'lu Jin', 'lu jin', 'luia',
            'logy', 'lola', 'lolita']
    },
    {'from': '{PLAYER}',
        'to': ['kyogre', 'kyogrenn', 'kogore', 'kiigra', 'kyogrren', 'kogre', 'korgon', 'gordon', 'morge', 'keegra', 'kegre', 'kergo',
            'gergo', 'kyyyogra', 'kyyogra', 'kororo', 'kogoro', 'kiogre', 'kilogre', 'kigore', 'kyogger', 'kooger', 'keogre', 'kioogra',
            'kyugura', 'kogura', 'kugura', 'kyogor', 'kaigor']
    }
]
replacersFrom = {
    "…": "...",
    '{KUN}': '',
    "{POKEBLOCK}": 'POKEBLOCK',
    '{LEFT_ARROW}': 'LEFT ARROW',
    '{RIGHT_ARROW}': 'RIGHT ARROW',
    '{UP_ARROW}': 'UP ARROW',
    '{DOWN_ARROW}': 'DOWN ARROW',

}
replacersTo = {
    "...": "…",
    'pokeblock': '{POKEBLOCK}',
    'pokebloc': '{POKEBLOCK}',
    'poke block': '{POKEBLOCK}',
    'poke bloc': '{POKEBLOCK}',
    'down arrow': '{DOWN_ARROW}',
    'arrow down': '{DOWN_ARROW}',
    'up arrow': '{UP_ARROW}',
    'arrow up': '{UP_ARROW}',
    'left arrow': '{LEFT_ARROW}',
    'arrow left': '{LEFT_ARROW}',
    'right arrow': '{RIGHT_ARROW}',
    'arrow right': '{RIGHT_ARROW}'
}
systemTagsAlert = ["PAUSE", "WAIT", "SKIP", "CLEAR", 'COLOR', 'SHADOW', 'DYNAMIC']

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
            if input("Error:") != '':
                print(text)


def parseFile(filename):
    lines = ''
    metaSections = []
    with open(filename, encoding='UTF-8') as file:
        lines = file.readlines()
    
    sections = []
    # {
    #   'header': [name]
    #   'contents': [text]
    # }

    for i in range(len(lines)):
        line = lines[i]

        if len(sections) > 0:
            if sections[-1]['type'] == '.string':
                if line.__contains__('.string "'):
                    start, content, end = trimStringLine(line)
                    
                    content = content.replace('\\n', ' ').replace('\\l', ' ').replace('$', '')
                    content = content.replace('\\p', '\n')

                    sections[-1]['contents'] += content
                    continue
        
        if len(sections) > 20:
            metaSections.append(sections)
            sections = []

        if line.startswith('//'):
            sections.append({
                'type': 'plain',
                'contents': line.replace('\n', '')
            })
        elif line.endswith(':\n') and lines[i+1].__contains__('.string "'):
            # Header
            sections.append({
                'type': '.string',
                'header': line[:-1],
                'contents': ''
            })
        elif line.__contains__(' = _("') and line.__contains__('");'):
            start, contents, end = trimStringLine(line)
            contents = contents.replace('\\n', ' ')
            contents = contents.replace('\n', '')

            contents, endTags = stripEndingSystemTags(contents)

            tags = getTags(contents)
            if hasSystemTag(tags):
                sections.append({
                    'type': 'plain',
                    'contents': line.replace('\n', '')
                })
                continue

            sections.append({
                'type': '(_singleLine',
                'header': line.split('_(')[0],
                'contents': contents,
                'endTags': endTags
            })
        else:
            sections.append({
                'type': 'plain',
                'contents': line.replace('\n', '')
            })
    
    if len(sections) > 0:
        metaSections.append(sections)
            
    return metaSections


def stripEndingSystemTags(text):
    tags = getTags(text)
    rTag = ''
    for i in range(len(tags)-1, -1, -1):
        if isSystemTag(tags[i]):
            if text.endswith('{' + tags[i] + '}'):
                # Remove it from the end
                # Append it to rTag
                charsToRemove = len(tags[i]) + 2
                rTag = text[-charsToRemove:] + rTag
                text = text[:-charsToRemove]
            else:
                break
        else:
            break
    
    return text, rTag


def isSystemTag(tag):
    for tagAlert in systemTagsAlert:
        if tag.__contains__(tagAlert):
            return True
    return False


def processTextToTags(text):
    containsKun = False
    if text.__contains__('{KUN}'):
        text = text.replace('{KUN}', '')
        containsKun = True
    tags = getTags(text)

    ret = ''
    if len(tags) == 0:
        ret = text
    else:
        ret = manualReplace(text, tags)
        
    if containsKun:
        ret = ret.replace('{PLAYER}', '{PLAYER}{KUN}')
    
    return ret


def hasSystemTag(tags):
    for tag in tags:
        for tagAlert in systemTagsAlert:
            if tag.__contains__(tagAlert):
                return True
    
    return False


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


def trimStringLine(line):
    start = line.index('"')
    end = line.rindex('"')
    return line[start:], line[start+1:end], line[end]


def printSections(sections):
    final = ''

    for section in sections:
        if section['type'] != 'plain':
            final += section['contents'] + '\n\n'

    return final


def processText(text):
    maxLinePixelLength = 208
    lines = []

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

    return compileText(lines)


def compileText(lines):
    # \n is a regular line break,
    # \l is a 'wait for user input to continue to the next line' break
    # The textbox in game is two lines long so we do this
    for i in range(len(lines) - 1):
        if i % 2 == 0:
            lines[i] += '\\n'
        else:
            lines[i] += '\l'

    return lines


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
        '…': 8,
    }
    l = 0
    for letter in text:
        if letter in particularLength:
            l += particularLength[letter]
        else:
            l += 6

    return l


def replaceWithDictionary(text, dict):
    for replacer in dict:
        text = text.replace(replacer, dict[replacer])
        text = text.replace(replacer.capitalize(), dict[replacer])
        text = text.replace(replacer.upper(), dict[replacer])
    
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


def putBackTogether(sections, translated):
    paragraphs = translated.split('\n\n')
    j = 0

    for i in range(len(paragraphs)):
        while sections[j]['type'] == 'plain':
            j += 1
            if j >= len(sections):
                return sections
        
        # .STRING
        if sections[j]['type'] == '.string':
            finalSectionContents = ''
            finalSectionLines = []
            for text in paragraphs[i].split('\n'):
                finalSectionLines += processText(text)
                finalSectionLines[-1] += '\p'
            
            finalSectionLines[-1] = finalSectionLines[-1][:-2] + '$'

            for line in finalSectionLines:
                finalSectionContents += '	.string "' + line + '"\n'
            
            sections[j]['contents'] = finalSectionContents
        
        # (_SINGLELINE
        elif sections[j]['type'] == '(_singleLine':
            finalSectionContents = ''
            lines = processText(paragraphs[i])
            for i in range(len(lines)):
                finalSectionContents += lines[i]

            tags = getTags(sections[j]['contents'])

            if hasInvalidTags(tags):
                print("MANUAL REPLACE TIME:")
                print(sections[j]['header'])
                print(sections[j]['contents'])
                print(translate(input("Translate:")))
                finalSectionContents = input(">")
            
            finalSectionContents += sections[j]['endTags']

            sections[j]['contents'] = finalSectionContents
        
        j += 1
        if j >= len(sections):
            return sections
    
    return sections


def hasInvalidTags(tags):
    for tag in tags:
        if tag not in ['STR_VAR_1', 'STR_VAR_2', 'STR_VAR_3', 'PLAYER', 'KUN']:
            return True
    
    return False


def processFile(filename):
    metasections = parseFile(filename)
    text = ''

    for sections in metasections:
        print("New metasection")

        newText = printSections(sections)
        

        newSections = putBackTogether(sections, newText)

        for section in newSections:
            if section['type'] == 'plain':
                text += section['contents'] + '\n'
            elif section['type'] == '.string':
                text += section['header'] + '\n'
                text += section['contents']
            elif section['type'] == '(_singleLine':
                text += section['header'] + '_("' + section['contents'] + '");\n'
    
        with open(filename + "_", "w+", encoding='UTF-8', newline='\n') as file:
            file.write(text)
            print(text, end='')
    
    with open(filename, "w+", encoding='UTF-8', newline='\n') as file:
        file.write(text)
        print(text, end='')
    
    os.remove(filename + '_')


def theBigTranslate(baseDir):
    for i in os.listdir(os.path.join(baseDir, 'data', 'maps')):
        if not os.path.isdir(os.path.join(baseDir, 'data', 'maps', i)):
            continue
        if not os.path.exists(os.path.join(baseDir, 'data', 'maps', i, 'scripts.inc')):
            continue
        file = os.path.join(baseDir, 'data', 'maps', i, 'scripts.inc')
        processFile(file)

    for i in os.listdir(os.path.join(baseDir, 'data', 'text')):
        file = os.path.join(baseDir, 'data', 'text', i)
        processFile(file)


def verifyAbilityDescLength(baseDir):
    lines = []
    with open(os.path.join(baseDir, 'src', 'data', 'text', 'abilities.h'), encoding="UTF-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.__contains__('Description[] = _("'):
            start, trim, end = trimStringLine(line)
            trim = trim.replace('\\n', '')
            if getRenderLength(trim) > 146:
                print(trim  + ' ' + str(getRenderLength(trim)))
                while getRenderLength(input('>')) > 146:
                    print(trim)


if __name__ == '__main__':
    #theBigTranslate(os.path.join('src', 'pokeemerald'))
    verifyAbilityDescLength(os.path.join('src', 'pokeemerald'))

