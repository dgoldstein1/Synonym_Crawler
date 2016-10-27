# -*- coding: utf-8 -*-
"""
Created by david on 10.24.2016 using 
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://www.youtube.com/watch?v=0mAGb6sCZWc
"""

import sys
from bs4 import BeautifulSoup
from urllib import urlopen
from treelib import Tree, Node

class ThesaurusEntry:
	"""parses web and contains word and dictionary of synonyms """

	def __init__(self,targetWord,targetUrl,max):
		self.synonyms = {}
		self.word = targetWord
		self.definition = ""
		self.maxEntries = max

		if targetUrl == None:
			self.url = 'http://www.thesaurus.com/browse/' + targetWord + '?s=t'
		else:
			self.url = targetUrl

		self.parseURL(self.url)

	def parseURL(self,url):
		"""parses synonyms and links of given thesaurs.com URL """
		html = urlopen(url).read()
		soup = BeautifulSoup(html,"html.parser")

		#get definition
		definitionBlock = soup.find('div',{"class":"mask"})
		if definitionBlock == None:
			print "Could not find synonym block in parsing for URL: " + url
			exit(1)
		for block in definitionBlock.findAll('strong',{"class":"ttl"}):
			self.definition += block.renderContents() + ", "

		#get synonym list
		synblock = soup.find('div',{"class":"relevancy-list"}) #synonym box
		i = 0
		for syn in synblock.findAll('a'):
			if i >= self.maxEntries:
				break
			word = syn.span.renderContents()
			link = syn.get('href')
			self.synonyms[word] = link
			i = i + 1



	def printEntry(self):
		"""prints tabbed synonyms"""
		output = ""
		output += "word:" + '\t' + self.word + '\n'
		output += "definition:" + '\t' + self.definition + '\n'
		output += "synonyms:" + '\n'
		for synonym in self.synonyms:
			output += '\t' + synonym + '\n'
		print output

def generateTree(startingWord,treeHeight,leafWidth):
	""" parses thesaurus entries up to treeHeight. Root node = height 0 """
	totalNodes = (leafWidth ** (treeHeight + 1)) -  1
	printProgress(0, totalNodes, prefix = 'generating tree:', barLength = 50)
	tree = genHelper(startingWord,None,leafWidth,treeHeight,0,None)
	return tree 

def genHelper(currWord,parent,leafWidth,treeHeight,currHeight,tree):
	newNode = ThesaurusEntry(currWord,None,leafWidth)

	if tree==None: #create root
		tree = Tree()
		tree.create_node(currWord,newNode.word)
	else:
		if tree.contains(currWord): #duplicate, do not add to tree
			return
		tree.create_node(currWord,newNode.word,parent=parent)

	printProgress(tree.size(), (leafWidth ** (treeHeight + 1)) -  1,prefix = 'generating tree:', barLength = 50)

	#stop condition if reached spec. height
	if currHeight > treeHeight - 1:
		return
	
	#recurse through children
	for synonym in newNode.synonyms:
		genHelper(synonym,currWord,leafWidth,treeHeight,currHeight + 1,tree)

	return tree

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    taken from: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
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
	tree = generateTree("ambiguous",7,2)
	tree.show(key=lambda x: x.tag, reverse=True, line_type='ascii-em')


	#root = ThesaurusEntry("sick",None,10)

	#startingEntry.printEntry()


 
	

