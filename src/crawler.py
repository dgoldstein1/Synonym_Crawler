# -*- coding: utf-8 -*-
"""
Created by david on 10.24.2016 using 
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://www.youtube.com/watch?v=0mAGb6sCZWc
"""

import sys
import time
import random
from bs4 import BeautifulSoup
from urllib import urlopen
from treelib import Tree, Node


def scrapeDefinition(word):
	"""parses definition of given word from online"""
	url = 'http://www.thesaurus.com/browse/' + word + '?s=t'
	html = urlopen(url).read()
	soup = BeautifulSoup(html,"html.parser")

	#get definition
	definitionBlock = soup.find('div',{"class":"mask"})
	if definitionBlock == None:
		print "Could not find synonym block in parsing for URL: " + url
		return

	definition = ""
	for block in definitionBlock.findAll('strong',{"class":"ttl"}):
		definition += block.renderContents() + ", "

	return definition

def scrapeSynonyms(word,number,tree=None):
	"""scrapes synonyms of word from thesaurus.com"""
	url = 'http://www.thesaurus.com/browse/' + word + '?s=t'
	html = urlopen(url).read()
	soup = BeautifulSoup(html,"html.parser")

	#get synonym list
	synblock = soup.find('div',{"class":"relevancy-list"}) #synonym box
	i = 0
	synonyms = []
	for syn in synblock.findAll('a'):
		if i >= number:
			break
		word = syn.span.renderContents()			
		if tree!=None and not tree.contains(word):				
			synonyms.append(word)				
			i = i + 1

	return synonyms



def generateTree(startingWord,treeHeight=3,leafWidth=2,printOutput=True):
	""" parses thesaurus entries up to treeHeight. Root node = height 0 """
	totalNodes = (leafWidth ** (treeHeight + 1)) -  1
	if printOutput:
		printProgress(0, totalNodes)
	tree=genHelper(startingWord,leafWidth,treeHeight,printOutput)
	if printOutput:
		printProgress(totalNodes, totalNodes)
	return tree

def genHelper(currWord,leafWidth,treeHeight,printOutput,currHeight=0,tree=Tree(),parent=None):
	"""recusrively parses to generate tree of specified height and width"""

	#stop condition if reached spec. height
	if currHeight > treeHeight - 1:
		return

	#create root
	if parent==None:
		tree.create_node(currWord,currWord)

	synonyms = scrapeSynonyms(currWord,leafWidth,tree)
	for synonym in synonyms:
		tree.create_node(synonym,synonym,parent = currWord)
		if printOutput:
			printProgress(tree.size(), (leafWidth ** (treeHeight + 1)) -  1)
		
	#recurse through children
	for synonym in synonyms:
		genHelper(synonym,leafWidth,treeHeight,printOutput,currHeight + 1,tree,currWord)

	return tree

def crawl(startingWord,tree=Tree(),treeHeight=7,currdepth=0,leafWidth=3):
	"""crawls until n depth and returns random synonym"""
	if currdepth==0:
		tree.create_node(startingWord,startingWord)

	if currdepth == treeHeight:
		return [startingWord,tree]

	nextWord = scrapeSynonyms(startingWord,leafWidth,tree)[random.randint(0,leafWidth-1)]
	tree.create_node(nextWord,nextWord,parent=startingWord)

	printProgress(currdepth+1,treeHeight)
	return crawl(nextWord,tree,treeHeight,currdepth + 1,leafWidth)



	


# Print iterations progress
def printProgress (iteration, total, prefix = 'generating tree', suffix = '', decimals = 1, barLength = 40):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == "__main__":

	start_time = time.time()

	word = "mean"
	leafWidth = 2
	treeHeight = 5

	generateTree(word,leafWidth=leafWidth,treeHeight=treeHeight).show(key=lambda x: x.tag, reverse=True, line_type='ascii-em')	
	crawl(word,leafWidth=leafWidth,treeHeight=treeHeight)[1].show(key=lambda x: x.tag, reverse=True, line_type='ascii-em')

	print("\n")
	print("--- executed in %s seconds ---" % (time.time() - start_time))

	#root = ThesaurusEntry("sick",None,10)


 
	

