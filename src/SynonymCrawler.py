"""
Created by david on 10.24.2016
"""

import sys
import time
import random
from bs4 import BeautifulSoup
from urllib import urlopen
from treelib import Tree, Node

reload(sys)
sys.setdefaultencoding('utf-8')


class SynonymCrawler():
	"""
	Scraper which recursively finds definitions / synonyms of words online
	and stores them in a tree.
	"""

	def __init__(self,word,leafWidth=2,treeHeight=5):

		#init instance variables
		self.currWord = word
		self.leafWidth = leafWidth
		self.treeHeight = treeHeight

		#init model
		self.targetData = self.crawl(self.currWord) #[0] = targetWord, [1] = targetTree
		self.tree = self.__genChildren(self.currWord,1) #generate root and its children
		self.currDefinition = self.scrapeDefinition(self.currWord)

	def step(self,chosen_word):
		""" 
		generates children of one leaf from given word (used by GUI)

		@params:
	        chosen_word	- Required	: word inputted by user to generate children

		@return True (if target word)
		@return [currWord,definition,synonyms]
		"""
		if chosen_word not in self.tree:
			print chosen_word, " not in Tree"
			self.tree.show()
			return None


		if len(self.tree.children(chosen_word))==0:
			self.tree = self.__genChildren(chosen_word,1,self.tree,parent=self.currWord)

		self.currWord = chosen_word
		self.currDefinition = self.scrapeDefinition(chosen_word)
		synonyms = []
		for node in self.tree.children(chosen_word):
			synonyms.append(node.tag)

		#self.tree.show()
		#print "displaying: ", [self.currWord,self.currDefinition,synonyms]

		return [self.currWord,self.currDefinition,synonyms]

	def scrapeDefinition(self,word):
		"""parses definition of given word from online
		@params:
		    word 			- Required  : starting point in thesaurus.com (string)
		@return definition (string)
	    """
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

	def scrapeSynonyms(self,word,number,tree=None):
		"""
		scrapes synonyms of word from thesaurus.com
		@params:
		    word 			- Required  : starting point in thesaurus.com (string)
		    number 		    - Required  : number of synonyms to scrape (int)
		    tree 		   	- Optional  : specify tree to avoid repeating synonyms in tree  (treelib.Tree)

		@return synonyms (string[])
	    """
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

	def generateFullTree(self,startingWord,treeHeight=3,leafWidth=2,printOutput=True):
		"""
		generates the entire tree (with answer)
		parses thesaurus entries up to treeHeight. Root node = height 0 
		@params:
	        startingWord   	- Required  : starting point in thesaurus.com (string)
	        treeHeight      - Optional  : depth of crawl (int)
	        leafWidth    	- Optional  : children considered at each iteration (int)
	        printOutput     - Optional  : prints % progress after each iteration (bool) 
        @return tree (treelib.Tree)   
		"""
		totalNodes = (leafWidth ** (treeHeight + 1)) -  1
		if printOutput:
			printProgress(0, totalNodes,)
		tree=self.__genChildren(startingWord,treeHeight,printOutput=printOutput)
		if printOutput:
			printProgress(totalNodes, totalNodes)
		return tree

	def __genChildren(self,currWord,nIterations,tree=Tree(),printOutput=True,currHeight=0,parent=None,nodesCreated=0):
		"""
		recusrively parses to generate tree of specified height and width
		@params:
	        currWord 	  	- Required  : starting point in thesaurus.com (string)
	        nIterations     - Required  : depth of crawl (int)
	        tree    		- Optional  : starting tree (treelib.Tree)
	        printOutput     - Optional  : prints % progress after each iteration (bool)    
	        currHeight		- Optional	: starting deptth (int)
	        parent			- Optional	: parent of starting node (treelib.Node)
	        nodesCreated	- Optional	: # nodes already created for this branch of tree (int)
	    @return tree (treelib.Tree)
		"""
		#stop condition if reached spec. height
		if currHeight > nIterations - 1:
			return

		#create root
		if parent==None:
			tree.create_node(currWord,currWord)

		synonyms = self.scrapeSynonyms(currWord,self.leafWidth,tree)
		for synonym in synonyms:
			tree.create_node(synonym,synonym,parent = currWord)
			nodesCreated = nodesCreated + 1
			if printOutput:
				printProgress(nodesCreated, (self.leafWidth ** (nIterations)),prefix="Generating Children")
			

		#recurse through children
		for synonym in synonyms:
			self.__genChildren(synonym,nIterations,tree,currHeight + 1,currWord,nodesCreated)

		return tree

	def crawl(self,startingWord,tree=Tree(),currdepth=0):
		"""
		crawls until n depth and returns random synonym
	    @params:
	    	self			- Required	: instance of Synonyms Crawler
	        startingWord   	- Required  : starting point in thesaurus.com (string)
	        tree       		- Optional  : specified tree to add on to (treelib.Tree)
	        currdepth      	- Optional  : start on specified depth (int)
       	@return tree (treelib.Tree)
		"""
		if currdepth==0:
			tree.create_node(startingWord,startingWord)

		if currdepth == self.treeHeight:
			return [startingWord,tree]


		try:
			nextWord = self.scrapeSynonyms(startingWord,self.leafWidth,tree)[random.randint(0,self.leafWidth-1)]
		except:
			nextWord = self.scrapeSynonyms(startingWord,self.leafWidth,tree)[0]					
		tree.create_node(nextWord,nextWord,parent=startingWord)

		printProgress(currdepth+1,self.treeHeight,prefix="Crawling")
		return self.crawl(nextWord,tree,currdepth + 1)

		#end class

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
    bar             = '>' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == "__main__":
	start_time = time.time()
	crawler = SynonymCrawler("mean")
	print("--- executed in %s seconds ---" % (time.time() - start_time))




 
	

