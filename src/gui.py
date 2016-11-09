import gi
import SynonymCrawler
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class SynonymWindow(Gtk.Window):

    def __init__(self,startingWord,crawler=None):
        Gtk.Window.__init__(self, title=startingWord)

        #init instance vairables
        self.crawler = SynonymCrawler.SynonymCrawler(startingWord,leafWidth=5)
        self.number_of_synonyms = self.crawler.leafWidth

        #init window
        self.set_border_width(5)
        self.set_default_size(450,400)
        self.__createHeader()
        self.__createBody()
    

    def __createHeader(self):
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
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.__currSynonymBoxes = []
        for node in self.crawler.tree.children(self.crawler.currWord):
            listbox.add(self.__synonymBox(node.tag))        
        self.add(listbox)

    def __synonymBox(self,word,textSize=15):
        """ 
        Returns Gtk.row with specified word
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
        if word == None:
            word = widget.__value

        data = self.crawler.step(word)

        self.hb.props.title = word
        self.hb.set_subtitle(data[1])

        for i in range(0,len(self.__currSynonymBoxes)):
            self.__currSynonymBoxes[i].set_label(data[2][i])
            self.__currSynonymBoxes[i].__value = data[2][i]


    def on_back_pressed(self,widget):
        try:
            previousWord = self.crawler.tree.parent(self.crawler.currWord).tag
        except(AttributeError): #at root
            return
        self.on_synonym_clicked(word=previousWord)
        






if __name__ == "__main__":
    win = SynonymWindow("fiber")
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
