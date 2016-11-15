import gi
import SynonymCrawler
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class SynonymWindow(Gtk.Window):
    """
    Interface for SynonymCrawler.py
    """

    def __init__(self,startingWord,crawler=None):
        Gtk.Window.__init__(self, title=startingWord)

        #init instance vairables
        self.crawler = SynonymCrawler.SynonymCrawler(startingWord,leafWidth=3)
        self.number_of_synonyms = self.crawler.leafWidth

        print "target word: ", self.crawler.targetData[0]
        print "defition: ", self.crawler.scrapeDefinition(self.crawler.targetData[0])

        #init window
        self.set_border_width(5)
        self.set_default_size(450,400)
        self.__createHeader()
        self.__createBody()
    
    def __createHeader(self):
        """
        Creates header containing currently selected word and its definition
        """
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = self.crawler.currWord
        self.hb.set_subtitle(self.crawler.currDefinition)
        self.set_titlebar(self.hb)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        button.connect("clicked", self.on_back_pressed)
        box.add(button)

        self.hb.pack_start(box)

    def __createBody(self):        
        """
        Creates synonym boxes of selected word in body of window
        """
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.__currSynonymBoxes = []
        for node in self.crawler.tree.children(self.crawler.currWord):
            self.listbox.add(self.__synonymBox(node.tag))        
        self.add(self.listbox)

    def __synonymBox(self,word,textSize=15):
        """ 
        creates one synonym box, called by __createBody 
        @params:    
            word            - Required  : synonym to be displayed (string)
            textSize        - Optional  : size of text (int)
        @return Gtk.ListBoxRow
        """
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
#        label = Gtk.Label()
#        label.set_markup("<big> <span font_desc=\"" + str(textSize) + "\">" + word + " </span> </big>")        
#       TODO: display html in button
        button = Gtk.Button(word)
        button.__value = word
        button.connect("clicked", self.on_synonym_clicked)
        hbox.pack_start(button, True, True, 0)

        self.__currSynonymBoxes.append(button)
        return row


    def on_synonym_clicked(self,widget=None,word=None):
        """
        generates / displays new synonyms and definition when a synonym button is clicked
        """
        if word == None:
            word = widget.__value

        if word == "" or word == None: #none selected
            return

        if word == self.crawler.targetData[0]:
            #todo
            print "taget word reached!"
            return

        data = self.crawler.step(word)

        self.hb.props.title = word
        self.hb.set_subtitle(data[1])

        i = 0
        while i < len(data[2]):
            try:
                self.__currSynonymBoxes[i].set_label(data[2][i])
                self.__currSynonymBoxes[i].__value = data[2][i]
            except IndexError: #more synonyms than boxes
                self.listbox.add(self.__synonymBox(data[2][i]))
            i = i + 1

        if i < len(self.__currSynonymBoxes): #more boxes than synonyms
            while i < len(self.__currSynonymBoxes):
                self.__currSynonymBoxes[i].set_label("")
                i = i + 1


    def on_back_pressed(self,widget):
        """
        displays parent node of currently selected word
        """
        try:
            previousWord = self.crawler.tree.parent(self.crawler.currWord).tag
        except(AttributeError): #at root
            return
        self.on_synonym_clicked(word=previousWord)
        



if __name__ == "__main__":
    win = SynonymWindow("love")
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
