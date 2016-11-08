import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class SynonymWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="HeaderBar Demo")
        self.set_border_width(15)
        self.set_default_size(300,300)
        self.__createHeader()
        self.__createBody()

    def __createHeader(self):
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Header"
        self.hb.set_subtitle("subtitle")
        self.set_titlebar(self.hb)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

        self.hb.pack_start(box)

    def __createBody(self):        
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.__currSynonymBoxes = []
        listbox.add(self.__synonymBox("synoynm 1"))
        listbox.add(self.__synonymBox("synonym 2"))
        listbox.add(self.__synonymBox("synonym 3")) 
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

        self.__currSynonymBoxes.append(row)
        return row

    def on_synonym_clicked(self,widget):
        self.hb.props.title = widget.__value
        self.hb.set_subtitle(widget.__value)




if __name__ == "__main__":
    win = SynonymWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
