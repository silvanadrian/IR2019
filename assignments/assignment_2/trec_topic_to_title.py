import os
import sys
import re

# make sure the argument is good (0 = the python file, 1 the actual argument)
if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
    print 'Trec topic file'
    exit(0)

cleanTextRegex = re.compile('[^a-zA-Z]')
count = 0
outFilepath = 'data/'+"queries.txt"
line_num = 0

with open(outFilepath, 'w') as outputFile:
    with open(sys.argv[1], 'r') as inputFile:
        currentId = ''
        lines = inputFile.readlines()
        for inLine in lines:
            line_num += 1
            if inLine.startswith('<num> Number:'):
                currentId = inLine.replace('<num> Number:', '').strip()
            if inLine.startswith('<title>'):
                text = inLine.replace('<title>', '').strip()
                text = cleanTextRegex.sub(' ', text).lower()
                text = text.replace('    ',' ').replace('   ',' ').replace('  ',' ')
                if not text:
                	text = lines[line_num]
                	text = cleanTextRegex.sub(' ', text).lower()
                	text = text.replace('    ',' ').replace('   ',' ').replace('  ',' ')
                wordList = []
                for w in text.split(' '):
                    if w:
                        cleaned = w.strip()
                        wordList.append(cleaned)
                outputText = ' '.join(wordList)

                outputFile.write(currentId)
                outputFile.write(' ')
                outputFile.write(outputText.strip())
                outputFile.write('\n')
                count = count + 1

print 'Completed all ', count, ' topics'
print 'Saved in: ', outFilepath
