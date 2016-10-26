"""
Created by david on 10.24.2016 using 
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://www.youtube.com/watch?v=0mAGb6sCZWc
"""

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

def crawl(startingWord,treeHeight,treeWidth):
	""" parses thesaurus entries up to treeHeight. Root node = height 0 """
	print "generating tree.."
	tree = Tree() 
	root = ThesaurusEntry(startingWord,None,treeWidth)
	tree.create_node(startingWord,root.word)
	tree = crawlHelper(root,treeWidth,treeHeight,0,tree,0)
	print "done."
	return tree 

def crawlHelper(currEntry,treeWidth,maxHeight,currHeight,tree,entryNum):
	if currHeight > maxHeight-1:
		print currHeight
		return

	for synonym in currEntry.synonyms:
		url = currEntry.synonyms[synonym]
		try:
			newNode = ThesaurusEntry(synonym,url,treeWidth)
			tree.create_node(newNode.word,newNode.word,parent=currEntry.word)
			crawlHelper(newNode,treeWidth,maxHeight,currHeight + 1,tree)
			print "Added ",entryNum
			entryNum = entryNum + 1
		except:
			pass

	
	return tree



if __name__ == "__main__":
	tree = crawl("sick",6,4)
	tree.show(key=lambda x: x.tag, reverse=True, line_type='ascii-em')


	#root = ThesaurusEntry("sick",None,10)

	#startingEntry.printEntry()



	

