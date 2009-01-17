# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import time
from anki.sound import Recorder, play
from ankiqt.ui.utils import saveGeom, restoreGeom

def getAudio(parent, string=""):
    "Record and return filename"
    # record first
    r = Recorder()
    mb = QMessageBox(parent)
    restoreGeom(mb, "audioRecorder")
    mb.setWindowTitle("Anki")
    mb.setIconPixmap(QPixmap(":/icons/media-record.png"))
    but = QPushButton(_("  Stop"))
    but.setIcon(QIcon(":/icons/media-playback-stop.png"))
    #but.setIconSize(QSize(32, 32))
    mb.addButton(but, QMessageBox.RejectRole)
    mb.show()
    t = time.time()
    r.start()
    QApplication.instance().processEvents()
    while not mb.clickedButton():
        txt =_("Recording...<br>Time: %0.1f")
        mb.setText(txt % (time.time() - t))
        QApplication.instance().processEvents()
    # ensure at least a second captured
    saveGeom(mb, "audioRecorder")
    while time.time() - t < 1:
        time.sleep(0.1)
    r.stop()
    # process
    r.postprocess()
    return r.file()

def recordNoiseProfile(parent):
    r = Recorder()
    mb = QMessageBox(parent)
    mb.show()
    f = time.time() + 8
    r.start()
    while f > time.time():
        mb.setText("Sampling silence...%0.1f" % f - time.time())
        QApplication.instance().processEvents()
    r.stop()