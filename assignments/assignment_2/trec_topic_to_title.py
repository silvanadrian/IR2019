import os
import sys
import re

# make sure the argument is good (0 = the python file, 1 the actual argument)
if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
    print 'Trec topic file'
    exit(0)

cleanTextRegex = re.compile('[^a-zA-Z]')
count = 0
outFilepath = 'data/'+os.path.basename(sys.argv[1])

with open(outFilepath, 'w') as outputFile:
    with open(sys.argv[1], 'r') as inputFile:
        currentId = ''
        for inLine in inputFile.readlines():
            if inLine.startswith('<num> Number:'):
                currentId = inLine.replace('<num> Number:', '').strip()
            if inLine.startswith('<title>'):
                text = inLine.replace('<title>', '').strip()
                # clean text
                text = cleanTextRegex.sub(' ', text).lower()
                # remove multiple whitespaces
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
