from tkinter import *
from tkinter import filedialog, messagebox
import csv
import matplotlib
import sys
import os

matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from sys import platform as _platform
import configparser
from ColorTheme import color_theme
import cross_platform_config

__version__ = '1.51'


class GradeAnalyzer_GUI(Frame):
    def __init__(self, root, masterroot, listbox, statusbar, status1, status2, background, configtheme):
        super().__init__(root, width=cross_platform_config.config.FRAME_WIDTH, bg=background)
        self.root = root
        self.masterroot = masterroot
        self.listbox = listbox
        self.statusbar = statusbar
        self.status1 = status1
        self.status2 = status2
        self.configtheme = configtheme
        self.filename = ''
        self.numberofdata = 0
        self.lineorders = ['-', ':', '-.', '--', '-', ':', '-.', '--', '-', ':', '-.', '--', '-', ':', '-.', '--']
        self.colororders = ['blue', 'red', 'green', 'yellow', 'magenta', 'yellow', 'black', 'blue', 'red', 'green',
                            'cyan', 'magenta',
                            'cyan', 'black']

        self.year = 2018
        self.phyclass = 'Phys106'
        self.numberofsections = 0
        self.numberofstudents = 0
        self.listofsections = []
        self.lowercut = 0
        self.highercut = 100
        self.lowercut2 = 0
        self.highercut2 = 100
        self.percentlowercut = 0
        self.percenthighercut = 50

        self.checkhw, self.checkgp, self.checkgpfull, self.checkquiz, self.checkpart, self.checklab \
            = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()

        self.grades = []
        self.percentages = []

        # Define all columns as lists
        self.lastnames, self.firstnames, self.UINs, self.availables, self.sections, \
        self.quiz1s, self.gp1s, self.hw1s, self.part1s, self.lab1s, \
        self.quiz2s, self.gp2s, self.hw2s, self.part2s, self.lab2s, \
        self.quiz3s, self.gp3s, self.hw3s, self.part3s, self.lab3s, \
        self.quiz4s, self.gp4s, self.hw4s, self.part4s, self.lab4s, \
        self.quiz5s, self.gp5s, self.hw5s, self.part5s, self.lab5s, \
        self.quiz6s, self.gp6s, self.hw6s, self.part6s, self.lab6s, \
        self.quiz7s, self.gp7s, self.hw7s, self.part7s, self.lab7s, \
        self.quiz8s, self.gp8s, self.hw8s, self.part8s, self.lab8s, \
        self.quiz9s, self.gp9s, self.hw9s, self.part9s, self.lab9s, \
        self.quiz10s, self.gp10s, self.hw10s, self.part10s, self.lab10s \
            = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], \
              [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], \
              [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

        self.things_to_collect = ["quiz{}s", "gp{}s", "hw{}s", "part{}s", "lab{}s"]

        self.quizlist, self.gplist, self.hwlist, self.partlist, self.lablist = [], [], [], [], []

        self.numberofblankentries = 0
        self.curvetype = IntVar()
        self.legend = None
        self.entered = 0
        self.considering = []
        self.smoothingfactor = 1
        self.showsecondcurve = 0
        self.curve_already_showing = 0

        self.text = "Welcome to Grade Analyzer. Press Ctrl + L for help."
        if _platform == "darwin":
            self.text = "Welcome to Grade Analyzer. Press ⌘ + L for help."

        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        self.config = configparser.ConfigParser()
        self.config.read('configuration.ini')
        self.config_theme = str(configtheme.get())

        # Set the color scheme for the frame
        self.bg = color_theme(self.config_theme).bg
        self.fg = color_theme(self.config_theme).fg
        self.bg_toolbar = color_theme(self.config_theme).bg_toolbar
        self.facecolor = color_theme(self.config_theme).facecolor
        self.warningcolor1 = color_theme(self.config_theme).warningcolor1
        self.warningcolor2 = color_theme(self.config_theme).warningcolor2
        self.warningcolor3 = color_theme(self.config_theme).warningcolor3

        self.frame0 = Frame(self, height=20, bg=self.bg_toolbar)
        self.frame0.pack(side=TOP, fill=X, expand=1)

        def mouseon(event, tip):
            self.status1.config(text=tip)

        def mouseleave(event):
            self.status1.config(text=self.text)

        def widget_instructions(widget, instruction):
            widget.bind("<Enter>", lambda event, arg=instruction: mouseon(event, arg))
            widget.bind("<Leave>", mouseleave)

        buttonopen = Button(self.frame0, text="Open(⌘+O)", command=self.openfromfile, highlightbackground=self.bg_toolbar,
                            width=9)
        buttonopen.pack(side=LEFT)
        widget_instructions(buttonopen, "Open a .csv grades file from local. ")

        buttonclear = Button(self.frame0, text="Clear(⌘+C)", command=self.clearalldata, highlightbackground=self.bg_toolbar,
                             width=9)
        buttonclear.pack(side=LEFT)
        widget_instructions(buttonclear, "Clear all data and graph. ")

        buttonsave = Button(self.frame0, text="Save graph(⌘+S)", command=self.save_graph, highlightbackground=self.bg_toolbar,
                             width=13)
        buttonsave.pack(side=LEFT)
        widget_instructions(buttonsave, "Save the graph. ")

        self.buttonshow2 = Button(self.frame0, text="Show Second Curve", command=self.showcurve_2nd,
                             highlightbackground=self.bg_toolbar, width=16)
        widget_instructions(self.buttonshow2, "Show the result as a second curve using twin x axis. ")

        self.buttonshow = Button(self.frame0, text="Show Curve(⏎)", command=self.showcurve, highlightbackground=self.bg_toolbar,
                            width=14)
        self.buttonshow.pack(side=RIGHT)
        widget_instructions(self.buttonshow, "Show the result. ")

        self.entry_00 = Entry(self.frame0, highlightbackground=self.bg_toolbar, width=4, justify=RIGHT)
        self.entry_00.pack(side=RIGHT)
        self.Acutype = Radiobutton(self.frame0, text="Accumulation", variable=self.curvetype, value=2, fg=self.warningcolor3,
                              bg=self.bg_toolbar)
        self.Acutype.pack(side=RIGHT)
        self.Acutype.select()
        widget_instructions(self.Acutype, "Accumulated percentages from 0 and up. ")
        self.Distype = Radiobutton(self.frame0, text="Distribution", fg=self.warningcolor3, bg=self.bg_toolbar, variable=self.curvetype,
                              value=1)
        self.Distype.pack(side=RIGHT)
        widget_instructions(self.Distype, "Grade distributions with a few points interval. ")

        self.filepath = Label(self.frame0, text="", bg=self.bg_toolbar, fg=self.fg, width=100)
        self.filepath.pack(side=LEFT, fill=X)
        self.hidingtoolbar = 0

        def reveal_toolbar():
            if self.hidingtoolbar == 1:
                self.filepath.pack_forget()
                buttonclear.pack(side=LEFT)
                buttonopen.pack(side=LEFT)
                buttonsave.pack(side=LEFT)
                self.buttonshow.pack(side=RIGHT)
                if self.curve_already_showing == 1:
                    self.buttonshow2.pack(side=RIGHT)
                self.entry_00.pack(side=RIGHT)
                self.Acutype.pack(side=RIGHT)
                self.Distype.pack(side=RIGHT)
                self.filepath.pack(side=LEFT, fill=X)
                self.hidingtoolbar = 0

        def mouseclickfilepath(event):
            if self.hidingtoolbar == 0:
                buttonclear.pack_forget()
                buttonopen.pack_forget()
                buttonsave.pack_forget()
                self.buttonshow.pack_forget()
                if self.curve_already_showing == 1:
                    self.buttonshow2.pack_forget()
                self.entry_00.pack_forget()
                self.Acutype.pack_forget()
                self.Distype.pack_forget()
                self.hidingtoolbar = 1
            elif self.hidingtoolbar == 1:
                reveal_toolbar()

        def mouseonfilepath(event):
            self.filepath.config(fg=self.warningcolor2)

        def mouseleavefilepath(event):
            self.filepath.config(fg=self.fg)
            reveal_toolbar()

        self.filepath.bind("<Enter>", mouseonfilepath)
        self.filepath.bind("<Leave>", mouseleavefilepath)
        self.filepath.bind("<Button-1>", mouseclickfilepath)

        if _platform == "win32" or _platform == "win64":
            buttonopen.config(text='Open(Ct+O)')
            buttonclear.config(text='Clear(Ct+C)')
            buttonsave.config(text='Save graph(Ct+S)')
            self.buttonshow.config(text='Show Curve(Enter)')

        self.frame3 = Frame(self, width=300, bg=self.bg)
        self.frame3.pack(side=RIGHT, fill=Y, expand=0)

        Label(self.frame3, text='Year:', fg=self.fg, bg=self.bg, width=13, anchor=E).grid(row=0, column=0, sticky=E)
        Label(self.frame3, text='Class:', fg=self.fg, bg=self.bg, width=13, anchor=E).grid(row=1, column=0,
                                                                                               sticky=E)
        Label(self.frame3, text='# of Sections:', fg=self.fg, bg=self.bg, width=13, anchor=E).grid(row=2, column=0,
                                                                                                       sticky=E)
        Label(self.frame3, text='# of Students:', fg=self.fg, bg=self.bg, width=13, anchor=E).grid(row=3, column=0,
                                                                                                       sticky=E)

        self.year1 = Label(self.frame3, text='', fg=self.fg, bg=self.bg, width=9, anchor=W)
        self.year1.grid(row=0, column=1, columnspan=1, sticky=E)
        self.class1 = Label(self.frame3, text='', fg=self.fg, bg=self.bg, width=9, anchor=W)
        self.class1.grid(row=1, column=1, columnspan=1, sticky=E)
        self.sections1 = Label(self.frame3, text='', fg=self.fg, bg=self.bg, width=9, anchor=W)
        self.sections1.grid(row=2, column=1, columnspan=1, sticky=E)
        self.students1 = Label(self.frame3, text='', fg=self.fg, bg=self.bg, width=9, anchor=W)
        self.students1.grid(row=3, column=1, columnspan=1, sticky=E)

        label_cut = Label(self.frame3, text='-' * 40, width=30, fg=self.fg, bg=self.bg)
        label_cut.grid(row=4, column=0, columnspan=3, sticky=W)

        label_31 = Label(self.frame3, text='Lower Cut:', width=13, anchor=E, fg=self.fg, bg=self.bg)
        label_32 = Label(self.frame3, text='Higher Cut:', width=13, anchor=E, fg=self.fg, bg=self.bg)
        label_33 = Label(self.frame3, text='% Lower Cut:', width=13, anchor=E, fg=self.fg, bg=self.bg)
        label_332 = Label(self.frame3, text='% Higher Cut:', width=13, anchor=E, fg=self.fg, bg=self.bg)
        self.entry_31 = Entry(self.frame3, highlightbackground=self.bg, width=8)
        self.entry_32 = Entry(self.frame3, highlightbackground=self.bg, width=8)
        self.entry_33 = Entry(self.frame3, highlightbackground=self.bg, width=8)
        self.entry_332 = Entry(self.frame3, highlightbackground=self.bg, width=8)
        label_31.grid(row=5, column=0, sticky=E)
        label_32.grid(row=6, column=0, sticky=E)
        label_33.grid(row=7, column=0, sticky=E)
        label_332.grid(row=8, column=0, sticky=E)
        self.entry_31.grid(row=5, column=1)
        self.entry_32.grid(row=6, column=1)
        self.entry_33.grid(row=7, column=1)
        self.entry_332.grid(row=8, column=1)
        self.entry_31.insert(0, self.lowercut)
        self.entry_32.insert(0, self.highercut)
        self.entry_33.insert(0, self.percentlowercut)
        self.entry_332.insert(0, self.percenthighercut)

        def CUT():
            self.lowercut = float(self.entry_31.get())
            self.highercut = float(self.entry_32.get())
            self.percentlowercut = float(self.entry_33.get())
            self.percenthighercut = float(self.entry_332.get())
            self.gradeplot.set_xlim([self.lowercut, self.highercut])
            self.gradeplot.set_ylim([self.percentlowercut, self.percenthighercut])
            self.canvas.show()

        def zoomall():
            self.entry_31.delete(0, END)
            self.entry_32.delete(0, END)
            self.entry_33.delete(0, END)
            self.entry_332.delete(0, END)
            self.entry_31.insert(0, 0)
            self.entry_32.insert(0, 100)
            self.entry_33.insert(0, 0)
            self.entry_332.insert(0, 50)
            CUT()

        def CUT2():
            self.lowercut2 = float(self.entry_312.get())
            self.highercut2 = float(self.entry_322.get())
            self.gradeplot_2nd.set_xlim([self.lowercut2, self.highercut2])
            self.canvas.show()

        button34 = Button(self.frame3, text="Zoom all", command=zoomall, highlightbackground=self.bg, width=8)
        button34.grid(row=9, column=1)
        widget_instructions(button34, "Zoom out the graph to original boundaries. ")
        button35 = Button(self.frame3, text="CUT", command=CUT, highlightbackground=self.bg, anchor=W, width=3)
        button35.grid(row=9, column=2, sticky=W)
        widget_instructions(button35, "Trim the graph using the numbers on the left.")

        self.label_312 = Label(self.frame3, text='2nd X Lower Cut:', width=13, anchor=E, fg=self.fg, bg=self.bg)
        self.label_322 = Label(self.frame3, text='2nd X Higher Cut:', width=13, anchor=E, fg=self.fg, bg=self.bg)
        self.entry_312 = Entry(self.frame3, highlightbackground=self.bg, width=8)
        self.entry_322 = Entry(self.frame3, highlightbackground=self.bg, width=8)

        self.button352 = Button(self.frame3, text="CUT'", command=CUT2, highlightbackground=self.bg, anchor=W, width=3)

        label_cut2 = Label(self.frame3, text='-' * 40, width=30, fg=self.fg, bg=self.bg)
        label_cut2.grid(row=12, column=0, columnspan=3, sticky=W)

        label_s1 = Label(self.frame3, text='Smoothing Factor:', width=13, anchor=E, fg=self.fg, bg=self.bg)
        label_s1.grid(row=13, column=0, columnspan=1, sticky=E)
        widget_instructions(label_s1, "The bigger the smoothing factor, less accurate the curves are. Default is 1. ")

        self.entry_s1 = Entry(self.frame3, highlightbackground=self.bg, width=8)
        self.entry_s1.grid(row=13, column=1)
        self.entry_s1.insert(0, self.smoothingfactor)

        checkbutton1 = Checkbutton(self.frame3, text="Homework", fg=self.fg, bg=self.bg,
                                   highlightbackground=self.bg, variable=self.checkhw)
        checkbutton1.grid(row=14, column=1, columnspan=2, sticky=W)
        checkbutton1.select()

        checkbutton2 = Checkbutton(self.frame3, text="Group Problems", fg=self.fg, bg=self.bg,
                                   highlightbackground=self.bg, variable=self.checkgp)
        checkbutton2.grid(row=15, column=1, columnspan=2, sticky=W)
        checkbutton3 = Checkbutton(self.frame3, text="Group Problems(15)", fg=self.fg, bg=self.bg,
                                   highlightbackground=self.bg, variable=self.checkgpfull)
        checkbutton3.grid(row=16, column=1, columnspan=2, sticky=W)
        checkbutton3.select()

        checkbutton4 = Checkbutton(self.frame3, text="Quiz", fg=self.fg, bg=self.bg, highlightbackground=self.bg,
                                   variable=self.checkquiz)
        checkbutton4.grid(row=17, column=1, columnspan=2, sticky=W)
        checkbutton4.select()
        checkbutton5 = Checkbutton(self.frame3, text="Participation", fg=self.fg, bg=self.bg,
                                   highlightbackground=self.bg, variable=self.checkpart)
        checkbutton5.grid(row=18, column=1, columnspan=2, sticky=W)
        checkbutton5.select()
        checkbutton6 = Checkbutton(self.frame3, text="Lab", fg=self.fg, bg=self.bg, highlightbackground=self.bg,
                                   variable=self.checklab)
        checkbutton6.grid(row=19, column=1, columnspan=2, sticky=W)
        checkbutton6.select()

        self.frame2 = Frame(self, bg=self.bg)
        self.frame2.pack(side=BOTTOM, fill=X, expand=1)

        self.frame1 = Frame(self, bg=self.bg)
        self.frame1.pack(side=LEFT, fill=BOTH, expand=1)

        if _platform == "darwin" or _platform == "linux" or _platform == "linux2":
            self.gradefigure = Figure(figsize=(7, 4.7), dpi=100)
        elif _platform == "win32" or _platform == "win64":
            self.frame1.config(height=700)
            self.gradefigure = Figure(figsize=(7, 7), dpi=100)
        self.gradefigure.subplots_adjust(left=0.08, bottom=0.12, right=0.92, top=0.95)
        self.gradefigure.patch.set_facecolor(self.facecolor)
        self.gradeplot = self.gradefigure.add_subplot(111)

        self.gradeplot.plot(self.grades, self.percentages)
        self.gradeplot.set_xlim([self.lowercut, self.highercut])
        self.gradeplot.set_ylim([self.percentlowercut, self.percenthighercut])
        self.gradeplot.set_xlabel('Grades')
        self.gradeplot.set_ylabel('Percentage (%)')
        self.gradeplot.grid(True)
        self.gradeplot.set_facecolor(self.facecolor)

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.gradefigure, self.frame1)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame1)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        def openfromfile_event(event):
            self.openfromfile()

        def showcurve_event(event):
            self.showcurve()

        def clearalldata_event(event):
            self.clearalldata()

        def help_event(event):
            self.help()

        def save_graph_event(event):
            self.save_graph()

        if _platform == "darwin" or _platform == "linux" or _platform == "linux2":
            masterroot.bind('<Command-o>', openfromfile_event)  # key must be binded to the tk window(unknown reason)
            masterroot.bind('<Return>', showcurve_event)
            masterroot.bind('<Command-c>', clearalldata_event)
            masterroot.bind('<Command-s>', save_graph_event)
            masterroot.bind('<Command-l>', help_event)
        elif _platform == "win32" or _platform == "win64":
            masterroot.bind('<Control-o>', openfromfile_event)  # key must be binded to the tk window(unknown reason)
            masterroot.bind('<Return>', showcurve_event)
            masterroot.bind('<Control-c>', clearalldata_event)
            masterroot.bind('<Control-s>', save_graph_event)
            masterroot.bind('<Control-l>', help_event)

        self.pack(side=TOP, fill=BOTH, expand=1)

    def help(self):
        self.addlog("Grade Analyzer v. {}".format(__version__), self.warningcolor3)
        self.addlog('IMPORTANT: A valid .csv file: When downloading the file from Blackboard, choose "Comma". ')
        self.addlog("Open a .csv file first, then choose the type of grades you want to add to the total.")
        self.addlog('Then choose the range of labs you want to show at the top right corner. '
                    'Click "Show curve" to show the result.')
        self.addlog("You can show two curves with different totals at the same time. "
                    "However, currently the relative position of the two curves are not adjustable. ")
        self.listbox.insert(END, '*' * 60)

    def showcurve(self):
        self.smoothingfactor = float(self.entry_s1.get())

        if self.filename == '':
            self.addlog("Please open a file first!", self.warningcolor2)
            return
        if self.checkgp.get() == 1 and self.checkgpfull.get() == 1:
            self.addlog("Cannot choose gp and gp(15) at the same time!", self.warningcolor2)
            return
        totalgrade = self.checkhw.get() * 10 + self.checkgp.get() * 15 + self.checkgpfull.get() * 15 + self.checkquiz.get() * 15 \
                     + self.checkpart.get() * 10 + self.checklab.get() * 50

        minnumber = int(self.entry_00.get()[0])
        if len(self.entry_00.get()) == 3:
            maxnumber = int(self.entry_00.get()[-1])
        else:
            maxnumber = int(self.entry_00.get()[-2:None])

        self.grades = np.arange(0, totalgrade + self.smoothingfactor,
                                self.smoothingfactor)  # That  + in np.arange is essential! Otherwise
        # totalgrade cannot be reached.
        self.numberofdata = 0

        for section in self.listofsections:
            self.grade = []
            self.percentages = []
            for i in range(0, len(self.grades)):
                self.percentages.append(0)
            studentnumber = 0
            for i in range(0, len(self.lastnames)):
                if self.availables[i] == "Yes" and self.sections[i] == section:
                    studentnumber += 1
                    hw = 0
                    gp = 0
                    quiz = 0
                    part = 0
                    lab = 0
                    for number in range(minnumber, maxnumber + 1):
                        hw += self.hwlist[number - 1][i]
                        gp += self.gplist[number - 1][i]
                        quiz += self.quizlist[number - 1][i]
                        part += self.partlist[number - 1][i]
                        lab += self.lablist[number - 1][i]
                    grade = (self.checkhw.get() * hw + self.checkgp.get() * gp + self.checkquiz.get() * quiz
                             + self.checkpart.get() * part + self.checklab.get() * lab) / (
                                    maxnumber - minnumber + 1) \
                            + self.checkgpfull.get() * 15
                    self.grade.append(grade)

            for grade in self.grade:
                for i in range(0, len(self.grades)):
                    if self.grades[i + 1] >= grade >= self.grades[i]:
                        self.percentages[i] += 1 / studentnumber * 100
                        break
            if self.curvetype.get() == 2:       # Accumulate
                for i in range(1, len(self.grades)):
                    self.percentages[i] += self.percentages[i - 1]
            if self.showsecondcurve == 0:
                self.lowercut = totalgrade - 20
                self.highercut = totalgrade
                self.entry_31.delete(0, END)
                self.entry_31.insert(0, self.lowercut)
                self.entry_32.delete(0, END)
                self.entry_32.insert(0, self.highercut)
                if self.curvetype.get() == 2:
                    self.percenthighercut = 100
                    self.entry_332.delete(0, END)
                    self.entry_332.insert(0, self.percenthighercut)
                self.gradeplot.plot(self.grades, self.percentages, self.lineorders[self.numberofdata],
                                    color=self.colororders[self.numberofdata], label=section)
                self.gradeplot.set_xlim([self.lowercut, self.highercut])
                self.gradeplot.set_ylim([self.percentlowercut, self.percenthighercut])
                self.gradeplot.set_xlabel('Grades')
                self.gradeplot.set_ylabel('Percentage (%)')
                self.gradeplot.grid(True)

                self.legend = self.gradeplot.legend(loc='lower right', shadow=True)
                frame = self.legend.get_frame()
                frame.set_facecolor('0.90')

                # Set the fontsize
                for label in self.legend.get_texts():
                    label.set_fontsize('medium')

                for label in self.legend.get_lines():
                    label.set_linewidth(1.5)
            elif self.showsecondcurve == 1:
                self.lowercut2 = totalgrade - 20
                self.highercut2 = totalgrade
                self.entry_312.delete(0, END)
                self.entry_312.insert(0, self.lowercut2)
                self.entry_322.delete(0, END)
                self.entry_322.insert(0, self.highercut2)
                if self.curvetype.get() == 2:
                    self.percenthighercut = 100
                    self.entry_332.delete(0, END)
                    self.entry_332.insert(0, self.percenthighercut)
                self.gradeplot_2nd.plot(self.grades, self.percentages, self.lineorders[self.numberofdata],
                                    color=self.colororders[self.numberofdata], label=section)
                self.gradeplot_2nd.set_xlim([self.lowercut2, self.highercut2])
                self.gradeplot_2nd.set_ylim([self.percentlowercut, self.percenthighercut])
                self.gradeplot_2nd.grid(True)

            self.canvas.show()
            self.numberofdata += 1

        self.addlog("Showing result from {} to {}. ".format(minnumber, maxnumber))

        if self.curve_already_showing == 0:
            self.buttonshow.pack_forget()
            self.entry_00.pack_forget()
            self.Acutype.pack_forget()
            self.Distype.pack_forget()

            self.filepath.pack_forget()
            self.buttonshow.pack(side=RIGHT)
            self.buttonshow2.pack(side=RIGHT)
            self.entry_00.pack(side=RIGHT)
            self.Acutype.pack(side=RIGHT)
            self.Distype.pack(side=RIGHT)
            self.filepath.pack(side=LEFT, fill=X)

        self.curve_already_showing = 1

    def showcurve_2nd(self):
        self.showsecondcurve = 1

        self.gradeplot_2nd = self.gradeplot.twiny()
        self.gradeplot_2nd.set_xlabel('Second Grades')

        self.label_312.grid(row=10, column=0, sticky=E)
        self.label_322.grid(row=11, column=0, sticky=E)
        self.entry_312.grid(row=10, column=1)
        self.entry_322.grid(row=11, column=1)
        self.button352.grid(row=11, column=2, sticky=W)
        self.entry_312.insert(0, self.lowercut2)
        self.entry_322.insert(0, self.highercut2)

        self.showcurve()
        self.showsecondcurve = 0

    def openfromfile(self):
        file = filedialog.askopenfile(mode='r', defaultextension=".csv")
        if file is None:  # askopenasfile return `None` if dialog closed with "cancel".
            return
        self.filename = file.name

        i = -1
        while self.filename[i] != '/':
            i -= 1
        self.filename = self.filename[i + 1:None]

        if self.filename[-4:None] != ".csv" and self.filename[-4:None] != ".CSV":
            self.addlog('{} format is not supported. Please select a .CSV file to open.'.format(self.filename[-4:None]),
                        self.warningcolor1)
            return

        self.filepath.config(text=self.filename)

        if self.filename[3:5] == '20':
            if "fall" in self.filename:
                self.year1.config(text="{} Fall".format(self.filename[3:7]))
            elif "spring" in self.filename:
                self.year1.config(text="{} Spring".format(self.filename[3:7]))
            if 'phys.106' in self.filename:
                self.class1.config(text='Phys 106')
            elif 'phys.108' in self.filename:
                self.class1.config(text='Phys 108')
        # Preload the file and roughly calculate total number of labs.

        def find_column(row, string):
            for num in range(0, 30):
                if str(row[num])[0:len(string)] == string:
                    return num
            self.addlog("Error! {} column is not found. ".format(string), self.warningcolor1)

        with open(file.name, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            try:
                for row in reader:
                    if str(row[0])[-11:None] == '"Last Name"':
                        row_firstname = find_column(row, 'First Name')
                        row_UIN = find_column(row, 'Student ID')
                        row_available = find_column(row, 'Availability')
                        row_section = find_column(row, 'Section')
                        start_column = find_column(row, 'Quiz 1')
                    else:
                        try:
                            self.lastnames.append(str(row[0]))
                            self.firstnames.append(str(row[row_firstname]))
                            self.UINs.append(str(row[row_UIN]))
                            self.availables.append(str(row[row_available]))
                            self.sections.append(str(row[row_section]))

                            column = start_column
                            # From Ryan Sellers
                            for x in range(1, 11):
                                for collectable in self.things_to_collect:
                                    getattr(self, collectable.format(x)).append(float(row[column]))
                                    column += 1

                        except ValueError:
                            pass
            except UnicodeDecodeError:
                self.addlog('Invalid .csv file! Delimiter is not "Comma".', self.warningcolor1)
                self.addlog('IMPORTANT: A valid .csv file: When downloading the file from Blackboard, choose "Comma" '
                            'and DO NOT include hidden information. ')
                self.addlog('*' * 60)
                return
        file.close()

        # Find out the last lab entered.
        found_empty = 0
        for x in range(1, 11):
            if getattr(self, "quiz{}s".format(x)) == []:
                found_empty = 1
                if x == 1:
                    self.addlog("File is empty. ", self.warningcolor1)
                    return
                else:
                    self.entered = x - 1
                    break

        if found_empty == 0:
            self.entered = 10

        # Load the file again knowing how many labs are there.
        self.lastnames, self.firstnames, self.UINs, self.availables, self.sections, \
        self.quiz1s, self.gp1s, self.hw1s, self.part1s, self.lab1s, \
        self.quiz2s, self.gp2s, self.hw2s, self.part2s, self.lab2s, \
        self.quiz3s, self.gp3s, self.hw3s, self.part3s, self.lab3s, \
        self.quiz4s, self.gp4s, self.hw4s, self.part4s, self.lab4s, \
        self.quiz5s, self.gp5s, self.hw5s, self.part5s, self.lab5s, \
        self.quiz6s, self.gp6s, self.hw6s, self.part6s, self.lab6s, \
        self.quiz7s, self.gp7s, self.hw7s, self.part7s, self.lab7s, \
        self.quiz8s, self.gp8s, self.hw8s, self.part8s, self.lab8s, \
        self.quiz9s, self.gp9s, self.hw9s, self.part9s, self.lab9s, \
        self.quiz10s, self.gp10s, self.hw10s, self.part10s, self.lab10s \
            = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], \
              [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], \
              [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

        with open(file.name, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            try:
                for row in reader:
                    if str(row[0])[-11:None] == '"Last Name"':
                        continue
                    else:
                        try:
                            self.lastnames.append(str(row[0]))
                            self.firstnames.append(str(row[row_firstname]))
                            self.UINs.append(str(row[row_UIN]))
                            self.availables.append(str(row[row_available]))
                            self.sections.append(str(row[row_section]))

                            def check_blank(cell, thelist):
                                if cell != '':
                                    thelist.append(float(cell))
                                else:
                                    self.numberofblankentries += 1
                                    thelist.append(0)

                            column = start_column

                            for n in range(1, self.entered + 1):
                                for collectable in self.things_to_collect:
                                    check_blank(row[column], getattr(self, collectable.format(n)))
                                    column += 1

                        except ValueError:
                            pass
            except UnicodeDecodeError:
                self.addlog("Invalid csv file! ", self.warningcolor1)
                return
        file.close()

        for n in range(1, self.entered + 1):
            self.quizlist.append(getattr(self, self.things_to_collect[0].format(n)))
            self.gplist.append(getattr(self, self.things_to_collect[1].format(n)))
            self.hwlist.append(getattr(self, self.things_to_collect[2].format(n)))
            self.partlist.append(getattr(self, self.things_to_collect[3].format(n)))
            self.lablist.append(getattr(self, self.things_to_collect[4].format(n)))
            if len(self.quiz1s) == len(getattr(self, self.things_to_collect[0].format(n))) \
                    == len(getattr(self, self.things_to_collect[1].format(n))) == len(getattr(self, self.things_to_collect[2].format(n))) \
                    == len(getattr(self, self.things_to_collect[3].format(n))) == len(getattr(self, self.things_to_collect[4].format(n))):
                pass
            else:
                self.addlog("Found problem in the csv file in lab {}! Some entries are invalid. ".format(n),
                            self.warningcolor1)
                return

        for avalability in self.availables:
            if avalability == "Yes":
                self.numberofstudents += 1
        self.students1.config(text='{}/{}'.format(self.numberofstudents, len(self.lastnames)))

        for section in self.sections:
            if section not in self.listofsections and not section == "":
                self.listofsections.append(section)
                self.numberofsections += 1
        self.listofsections = sorted(self.listofsections)
        self.sections1.config(text='{}'.format(self.numberofsections))

        self.addlog('Added data {}'.format(self.filename), self.warningcolor3)
        self.addlog('Totally {} labs. '.format(self.entered))
        if self.numberofblankentries == 0:
            self.addlog('Found 0 blank entry.')
        elif self.numberofblankentries == 1:
            self.addlog('Found 1 blank entry. Blank entries are considered as zero. ')
        else:
            self.addlog('Found {} blank entries. Blank entries are considered as zero. '.format(self.numberofblankentries))

        self.entry_00.insert(0, '1-{}'.format(self.entered))

        if self.numberofsections > 12:
            self.addlog('Too many sections, code need to be modified.', self.warningcolor1)
            return

    def save_graph(self):
        saveascsv = filedialog.asksaveasfilename(defaultextension='.png')
        if saveascsv is None:
            return
        self.gradefigure.savefig(saveascsv, dpi=300)

        self.addlog('Saved the file to: {}'.format(saveascsv))

    def clearalldata(self):
        clearornot = messagebox.askquestion("CAUTION!", "Clear everything (including all data, "
                                                        "settings and graphs)?", icon='warning')
        if clearornot == 'yes':
            self.pack_forget()
            self.__init__(self.root, self.masterroot, self.listbox, self.statusbar, self.status1, self.status2,
                          self.bg, self.configtheme)
            self.addlog('*' * 60)
        else:
            pass

    def addlog(self, string, fgcolor="default"):
        self.listbox.insert(END, string)
        self.listbox.yview(END)

        if fgcolor != "default":
            i = 0
            while True:
                try:
                    self.listbox.itemconfig(i, bg=color_theme(self.config_theme).bg_log)
                    i += 1
                except:
                    self.listbox.itemconfig(i - 1, fg=fgcolor)
                    break


def main():
    root = Tk()

    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))  # Change the working directory to current directory.

    # Load the configuration file
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    config_theme = config["Settings"]["colortheme"]
    config_theme_var = IntVar()
    config_theme_var.set(config["Settings"]["colortheme"])

    w = cross_platform_config.config.FRAME_WIDTH  # width for the Tk root
    h = cross_platform_config.config.FRAME_HEIGHT  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2)
    y = (hs / 4) - (h / 4)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.wm_title("Grade Analyzer v. {}".format(__version__))
    # root.iconbitmap("icon.icns")
    root.configure(background=color_theme(config_theme).bg)

    # Status bar #
    statusbar = Frame(root, bg=color_theme(config_theme).bg, bd=1, relief=RIDGE)

    authorLabel = Label(statusbar, text='© 12,2017 Peihong Man.', fg=color_theme(config_theme).fg,
                        bg=color_theme(config_theme).bg, bd=1, relief=RIDGE,
                        padx=4.2, width=21)
    authorLabel.pack(side=LEFT)
    authorLabel.pack_propagate(0)

    status1 = Label(statusbar, fg=color_theme(config_theme).fg, bg=color_theme(config_theme).bg, bd=1, relief=RIDGE)
    if _platform == "darwin" or _platform == "linux" or _platform == "linux2":
        status1.config(text='Welcome to Grade Analyzer. Press ⌘ + L for help. ')
    elif _platform == "win32" or _platform == "win64":
        status1.config(text='Welcome to Grade Analyzer. Press Control + L for help. ')
    status1.pack(side=LEFT, fill=X, expand=True)
    status1.pack_propagate(0)
    status2 = Label(statusbar, text='v. {}'.format(__version__), fg=color_theme(config_theme).fg,
                    bg=color_theme(config_theme).bg, bd=1, relief=RIDGE, width=21)
    status2.pack(side=RIGHT)

    statusbar.pack(side=BOTTOM, fill=X)

    # Log frame #
    logFrame = Frame(root, height=100, bd=0, highlightthickness=0, bg='white')
    logFrame.pack(side=BOTTOM, fill=X, expand=False)
    logFrame.pack_propagate(0)

    scrollbar = Scrollbar(logFrame, bg=color_theme(config_theme).bg_log,
                          highlightbackground=color_theme(config_theme).bg_log,
                          troughcolor=color_theme(config_theme).bg_log)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(logFrame, fg=color_theme(config_theme).fg, bg=color_theme(config_theme).bg_log, bd=0,
                      selectbackground=color_theme(config_theme).bg_toolbar, highlightthickness=0,
                      yscrollcommand=scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    GradeAnalyzer_GUI(root, root, listbox, statusbar, status1, status2, color_theme(config_theme).bg, config_theme_var)

    listbox.delete(0, END)
    listbox.insert(END, '*' * 60)
    listbox.insert(END, 'Welcome to Grade Analyzer!')
    listbox.insert(END, 'This is the log file.')
    listbox.insert(END, 'Click to copy to the clipboard.')
    listbox.insert(END, '*' * 60)
    listbox.yview(END)

    root.mainloop()


if __name__ == '__main__':
    main()
