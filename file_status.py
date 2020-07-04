class FileStatus(object):
    def __init__(self):
        super().__init__()
        self.filedir = ''
        self.filename = '未命名'
        self.is_saved = False
        self.is_untitle = True
        self.is_openFile = False
        self.is_saveFlag_setted = False

    def set_openStatus(self, filename):
        self.filedir = filename
        self.filename = filename.split('/')[-1]
        self.is_untitle = False
        self.is_saved = True
        self.is_openFile = True
        self.is_saveFlag_setted = False

    def set_TextChanged(self):
        self.is_saved = False

    def set_saveStatus(self):
        self.is_saveFlag_setted = False
        self.is_saved = True
