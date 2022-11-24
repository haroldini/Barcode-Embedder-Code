# -*- coding: utf8 -*-
'''
Created on 16 juin 2016

@author: Chevalier Thierry
'''
import tkinter
import tkinter.ttk


class ScrolledWindow(tkinter.ttk.Frame):
    """

    Parent = master of scrolled window

    """

    def __init__(self, parent, *args, **kwargs):
        """Parent = master of scrolled window
       """
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # creating scrollbars and canvas and window to contain future widgets of the scrolling area
        self.xScrollbar = tkinter.ttk.Scrollbar(self, orient='horizontal')
        self.yScrollbar = tkinter.ttk.Scrollbar(self)
        self.scrollCanvas = tkinter.Canvas(self)
        self.scrollCanvas.config(
            relief='flat', borderwidth=0, highlightthickness=0)
        self.scrollWindow = tkinter.ttk.Frame(self.scrollCanvas, borderwidth=0)
        # placing scrollbar and  canvas into frame and the scrollFrame into canvas
        self.xScrollbar.grid(column=0, row=1, sticky="NESW", columnspan=2)
        self.yScrollbar.grid(column=1, row=0, sticky="NESW")
        self.scrollCanvas.grid(column=0, row=0, columnspan=1, rowspan=1,
                               sticky="NESW", padx=0, pady=0, ipadx=0, ipady=0)
        self.scrollWindowItemId = self.scrollCanvas.create_window(
            0, 0, window=self.scrollWindow, anchor='nw')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        # accociating scrollbar comands to canvas scroling
        self.xScrollbar.config(command=self.scrollCanvas.xview)
        self.yScrollbar.config(command=self.scrollCanvas.yview)
        self.scrollCanvas.config(
            xscrollcommand=self.xScrollbar.set, yscrollcommand=self.yScrollbar.set)
        # self.yScrollbar.lift(self.scrollWindow) # put to first plan
        # self.xScrollbar.lift(self.scrollWindow)
        self.scrollCanvas.bind('<Configure>', self._configure_scrollCanvas)
        ##self.scrollWindow.bind('<Configure>', self._configure_scrollWindow)
        self.scrollWindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollWindow.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.scrollCanvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.scrollCanvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.scrollCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _configure_scrollWindow(self, event):
        print("_configure_scrollWindow:")
        print("    event", "w=", event.width, "h", event.height)
        print("    scrollWindow", "w=", self.scrollWindow.winfo_width(),
              ", h=", self.scrollWindow.winfo_height())
        print("    scrollWindow reqwidth and reqheight", "w=",
              self.scrollWindow.winfo_reqwidth(), ", h=", self.scrollWindow.winfo_reqheight())
        print("    scrollCanvas", "w=", self.scrollCanvas.winfo_width(),
              ", h=", self.scrollCanvas.winfo_height())

    def _configure_scrollCanvas(self, event):
        # =======================================================================
        # print("_configure_scrollCanvas:")
        # print("    event", "w=", event.width, "h", event.height)
        # print("    scrollCanvas", "w=", self.scrollCanvas.winfo_width(), ", h=", self.scrollCanvas.winfo_height())
        # print("    scrollWindow", "w=", self.scrollWindow.winfo_width(), ", h=", self.scrollWindow.winfo_height())
        # print("    scrollWindow reqwidth and reqheight", "w=", self.scrollWindow.winfo_reqwidth(), ", h=", self.scrollWindow.winfo_reqheight())
        # =======================================================================
        ##canvasWidth, canvasHeight = (self.scrollCanvas.winfo_width(), self.scrollCanvas.winfo_height())
        canvasWidth, canvasHeight = (event.width, event.height)
        windowReqWidth, windowReqHeight = (
            self.scrollWindow.winfo_reqwidth(), self.scrollWindow.winfo_reqheight())
        if canvasWidth < windowReqWidth:
            if canvasHeight < windowReqHeight:
                # canvasWidth < windowReqWidth and canvasHeight < windowReqHeight
                self.scrollCanvas.config(
                    width=windowReqWidth, height=windowReqHeight)
                self.scrollCanvas.itemconfig(
                    self.scrollWindowItemId, width=windowReqWidth, height=windowReqHeight)
                ##self.scrollCanvas.config(scrollregion='0 0 %s %s' % (windowReqWidth, windowReqHeight))
                self.scrollCanvas.config(
                    scrollregion=self.scrollCanvas.bbox("all"))
                self.xScrollbar.grid()
                self.yScrollbar.grid()

            else:
                # canvasWidth < windowReqWidth and windowReqHeight <= canvasHeight
                self.scrollCanvas.config(width=windowReqWidth)
                self.scrollCanvas.itemconfig(
                    self.scrollWindowItemId, width=windowReqWidth, height=canvasHeight)
                ##self.scrollCanvas.config(scrollregion='0 0 %s %s' % (windowReqWidth, canvasHeight))
                self.scrollCanvas.config(
                    scrollregion=self.scrollCanvas.bbox("all"))
                self.xScrollbar.grid()
                self.tk.call("grid", "remove", self.yScrollbar)
        else:  # windowReqWidth <= canvasWidth
            if canvasHeight < windowReqHeight:
                # windowReqWidth <= canvasWidth and canvasHeight < windowReqHeigh
                self.scrollCanvas.config(height=windowReqHeight)
                self.scrollCanvas.itemconfig(
                    self.scrollWindowItemId, width=canvasWidth, height=windowReqHeight)
                ##self.scrollCanvas.config(scrollregion='0 0 %s %s' % (canvasWidth, windowReqHeight))
                self.scrollCanvas.config(
                    scrollregion=self.scrollCanvas.bbox("all"))
                self.tk.call("grid", "remove", self.xScrollbar)
                self.yScrollbar.grid()
            else:
                # windowReqWidth <= canvasWidth and windowReqHeight <= canvasHeight
                self.scrollCanvas.itemconfig(
                    self.scrollWindowItemId, width=canvasWidth, height=canvasHeight)
                self.scrollCanvas.config(
                    scrollregion=self.scrollCanvas.bbox("all"))
                self.tk.call("grid", "remove", self.xScrollbar)
                self.tk.call("grid", "remove", self.yScrollbar)

    def getScrollWindow(self):
        return self.scrollWindow


ScrolledWindow()
