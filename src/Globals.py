__author__ = 'Nathan'

from PySide import QtGui

class Globals:
    large_font = QtGui.QFont("Times", 30)
    large_bold_font = QtGui.QFont("Times", 30, QtGui.QFont.Bold)

    medium_font = QtGui.QFont("Times", 20)
    medium_bold_font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)

    small_font = QtGui.QFont("Times", 10)
    small_bold_font = QtGui.QFont("Times", 10, QtGui.QFont.Bold)

    window_width = 1300
    window_height = 800