import os
import leo.core.leoGlobals as g
from leo.core.leoQt import QtCore, QtGui, QtWidgets, QtConst, QtWebKit, QtWebKitWidgets

def _path_from_pos(c, p):
    """_path_from_pos - get folder for position

    FIXME: should be in Leo core somewhere.

    :param possition p: position
    :return: path
    :rtype: str
    """
    p = p.copy()

    def atfile(p):
        word0 = p.h.split()[0]
        return (
            word0 in g.app.atFileNames|set(['@auto']) or
            word0.startswith('@auto-')
        )
    
    aList = g.get_directives_dict_list(p)
    path = c.scanAtPathDirectives(aList)
    while c.positionExists(p):
        if atfile(p):  # see if it's a @<file> node of some sort
            nodepath = p.h.split(None, 1)[-1]
            nodepath = g.os_path_join(path, nodepath)
            if not g.os_path_isdir(nodepath):  # remove filename
                nodepath = g.os_path_dirname(nodepath)
            if g.os_path_isdir(nodepath):  # append if it's a directory
                path = nodepath
            break
        p.moveToParent()
    
    return path
class LEP_WebKitView(QtWebKitWidgets.QWebView):
    """LEP_WebKitView - Web Kit View
    """
    lep_type = "HTML"
    lep_name = "Web Kit View"
    def __init__(self, c=None, lep=None, *args, **kwargs):
        """set up"""
        super(LEP_WebKitView, self).__init__(*args, **kwargs)
        self.c = c
        self.lep = lep

    def new_position(self, p):
        """new_position - update for new position

        :param Leo position p: new position
        """
        owd = os.getcwd()
        path = _path_from_pos(self.c, p)
        os.chdir(path)
        g.es(path)
        if self.lep.recurse:
            self.setHtml(g.getScript(self.c, p, useSelectedText=False, useSentinels=False))
        else:
            self.setHtml(p.b)
        os.chdir(owd)
    def update_position(self, p):
        """update_position - update for current position

        :param Leo position p: current position
        """
        self.new_position(p)


