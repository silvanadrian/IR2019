import os
import timeit
import sys
import re
import codecs

if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print('Path to trec data documents')
    exit(0)

cleanTextRegex = re.compile('[^a-zA-Z]')
cleanHtmlRegex = re.compile('<[^<]+?>')

docCount = 0

def process_trec_files(filename, outputFile):
    global docCount
    with codecs.open(filename, "r", "iso-8859-1") as f:
        contents = f.readlines()
        currentDocId = ''
        currentDocContent = []
        recordContent = False
        for line in contents:

            if line.isspace():
                continue

            if line.startswith('<DOCNO>'):
                currentDocId = line.replace('<DOCNO>', '').replace('</DOCNO>', '').strip()
                recordContent = True
                continue

            if line.startswith('</DOC>'):

                parsed = cleanHtmlRegex.sub(' ', ' '.join(currentDocContent))
                parsed = cleanTextRegex.sub(' ', parsed)
                wordList = []
                for w in parsed.split(' '):
                    if w:
                        cleaned = w.lower().strip()
                        wordList.append(cleaned)
                outputText = ' '.join(wordList)

                outputFile.write(currentDocId)
                outputFile.write(' ')
                outputFile.write(outputText)
                outputFile.write('\n')
                recordContent = False
                currentDocContent = []
                docCount = docCount + 1
                continue

            if recordContent:
                currentDocContent.append(line)

        outputFile.flush()

count = 0
start_time = timeit.default_timer()
outFileName = 'trec_corpus.txt'

with open(outFileName, 'w') as outputFile:
    for dirpath, dirnames, fileNames in os.walk(sys.argv[1]):
        for file in fileNames:
            process_trec_files(dirpath + os.sep + file, outputFile)
            count = count + 1
            if count % 10 == 0:
                print('Completed ', count, ' files, with ', docCount, ' docs, time:', timeit.default_timer() - start_time)

print('\n-------\n', 'Completed all ', count, ' files, with ', docCount, ' docs, time: ', timeit.default_timer() - start_time)
