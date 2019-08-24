from sys import argv, exit
import subprocess
import webbrowser
from os import getcwd, popen, path, remove, startfile
import re
import shutil
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QGridLayout, QApplication, QPushButton, QMainWindow, QFrame,
                             QLabel, QComboBox, QCheckBox, QAbstractButton)
from PyQt5.QtGui import QPalette, QImage, QBrush, QIcon, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize


class HoverButton(QPushButton):

    def __init__(self, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: transparent; color: grey; font: 22pt Univers Condensed")

    def enterEvent(self, event):
        self.setStyleSheet("background-color: transparent; color: white; font: 22pt Univers Condensed")

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: transparent; color: grey; font: 22pt Univers Condensed")


class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()


class SettingsLabel(QLabel):
    def __init__(self, parent=None):
        super(SettingsLabel, self).__init__(parent)
        self.setStyleSheet("color: white; font: 15px Arial")


class Launcher(QMainWindow):

    def __init__(self):
        super().__init__()
        self.LAUNCHER_DIRECTORY = getcwd()
        self.initUI()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            self.launchGame()
        elif e.key() == Qt.Key_F5:
            self.deleteShadersCache()

    def initBG(self):
        # Background
        img_bg = QImage(self.LAUNCHER_DIRECTORY + "\\launcher\\bg.png")
        palette_bg = QPalette()
        palette_bg.setBrush(10, QBrush(img_bg))  # 10 = Windowrole
        self.setPalette(palette_bg)

    def initMainButtons(self):
        # Main buttons
        btn_play = HoverButton('ENTER THE ZONE')
        btn_play.clicked.connect(lambda: self.launchGame())
        btn_options = HoverButton('OPTIONS')
        btn_options.clicked.connect(lambda: self.toggleFrame(self.frame_options))
        btn_wiki = HoverButton('WIKI')
        btn_wiki.clicked.connect(lambda: webbrowser.open('http://wiki.stalker-anomaly.com/subdom/wiki/index.php?title=Main_Page'))
        btn_exit = HoverButton('QUIT')
        btn_exit.clicked.connect(QApplication.instance().quit)
        # Menu buttons' frame
        frame_main_buttons = QFrame(self)
        frame_main_buttons.setGeometry(660, 210, 250, 140)
        grid_buttons = QGridLayout(frame_main_buttons)
        grid_buttons.addWidget(btn_play)
        grid_buttons.addWidget(btn_options, 1, 0)
        grid_buttons.addWidget(btn_wiki, 2, 0)
        grid_buttons.addWidget(btn_exit, 3, 0)

    def initSocMediaButtons(self):
        # Social media buttons/icons
        btn_moddb = QPushButton('')  # MODDB's Anomaly page
        icon_moddb = QIcon(self.LAUNCHER_DIRECTORY + '\\launcher\\moddb.png')
        btn_moddb.setIconSize(QSize(80, 40))
        btn_moddb.setIcon(icon_moddb)
        btn_moddb.clicked.connect(lambda: webbrowser.open('https://www.moddb.com/mods/stalker-anomaly'))
        btn_discord = QPushButton('')  # Discord's link
        icon_discord = QIcon(self.LAUNCHER_DIRECTORY + '\\launcher\\discord.png')
        btn_discord.setIconSize(QSize(40, 40))
        btn_discord.setIcon(icon_discord)
        btn_discord.clicked.connect(lambda: webbrowser.open('https://discord.gg/DQ8M2GB'))
        btn_vk = QPushButton('')  # VK site
        icon_vk = QIcon(self.LAUNCHER_DIRECTORY + '\\launcher\\vk.png')
        btn_vk.setIconSize(QSize(40, 40))
        btn_vk.setIcon(icon_vk)
        btn_vk.clicked.connect(lambda: webbrowser.open('https://vk.com/anomaly_mod'))
        btn_fb = QPushButton('')  # Facebook site
        icon_fb = QIcon(self.LAUNCHER_DIRECTORY + '\\launcher\\fb.png')
        btn_fb.setIconSize(QSize(40, 40))
        btn_fb.setIcon(icon_fb)
        btn_fb.clicked.connect(lambda: webbrowser.open('https://www.facebook.com/Stalker-Anomaly-2355538658067205/'))
        btn_pda = QPushButton('')  # goto appdata for logs
        icon_pda = QIcon(self.LAUNCHER_DIRECTORY + '\\launcher\\pda.png')
        btn_pda.setIconSize(QSize(40, 40))
        btn_pda.setIcon(icon_pda)
        btn_pda.clicked.connect(lambda: self.openLogsFolder())
        # Social media frame (bottom right)
        frame_media = QFrame(self)
        frame_media.setGeometry(620, 430, 340, 60)
        frame_media.setStyleSheet('background-color: transparent')
        grid_media = QGridLayout(frame_media)
        grid_media.addWidget(btn_pda, 0, 0)
        grid_media.addWidget(btn_discord, 0, 1)
        grid_media.addWidget(btn_vk, 0, 2)
        grid_media.addWidget(btn_fb, 0, 3)
        grid_media.addWidget(btn_moddb, 0, 4)
        grid_media.setColumnStretch(4, 5)

    def initOptionsMenu(self, f_ud, f_cd, f_ld):

        # Creating the options menu
        self.frame_options = QFrame(self)
        self.frame_options.setGeometry(55, 40, 541, 413)
        self.frame_options.setStyleSheet('color: white')
        label_bg = QLabel(self.frame_options)
        pixmap_options = QPixmap(self.LAUNCHER_DIRECTORY + '\\launcher\\options2.png')
        label_bg.setPixmap(pixmap_options)
        self.frame_options.hide()
        # Save button
        icon_save_def = QPixmap(self.LAUNCHER_DIRECTORY + '\\launcher\\save_def.png')
        icon_save_highlighted = QPixmap(self.LAUNCHER_DIRECTORY + '\\launcher\\save_high.png')
        icon_save_pressed = QPixmap(self.LAUNCHER_DIRECTORY + '\\launcher\\save_press.png')
        btn_savechanges = PicButton(icon_save_def, icon_save_highlighted, icon_save_pressed)
        btn_savechanges.setParent(self.frame_options)
        btn_savechanges.clicked.connect(lambda: self.saveCurrentSettings(ref_arr, arr_options_array, f_ud, f_cd, f_ld))
        btn_savechanges.setGeometry(380, 370, 133, 25)

        # Sub menus bar, General and Graphics should be updated to PicButton for v2.
        # Currently, those 2 buttons are part of the background 'options2.png'
        frame_categories = QFrame(self.frame_options)
        frame_categories.setGeometry(0, -2, 185, 37)
        frame_categories.setStyleSheet('background-color: transparent')
        btn_general_options = QPushButton('General')
        btn_general_options.setStyleSheet('background-color: transparent; color: #b5b5b5; font: 17px Arial')
        btn_graphics_options = QPushButton('Graphics')
        btn_graphics_options.setStyleSheet('background-color: transparent; color: #3e3e3e; font: 17px Arial')
        grid_categories = QGridLayout(frame_categories)
        grid_categories.addWidget(btn_general_options, 0, 0)
        grid_categories.addWidget(btn_graphics_options, 0, 1)

        # Tips frame
        frame_tips = QFrame(self.frame_options)
        frame_tips.setGeometry(10, 392, 400, 50)
        label_tip = SettingsLabel('Save before launching the game to apply changes.')
        label_tip.setStyleSheet('color:grey; font: 12px Arial')
        label_tip.setParent(frame_tips)

        # Settings frame
        frame_settings = QFrame(self.frame_options)
        frame_settings.setGeometry(5, 45, 382, 362)
        grid_settings = QGridLayout(frame_settings)
        # Creating settings options
        label_resolution = SettingsLabel('Resolution')
        dropdwnmenu_resolution = QComboBox(frame_settings)
        dropdwnmenu_resolution.setStyleSheet("background-color: #313031; color: white")
        dropdwnmenu_resolution.addItem("800x600")
        dropdwnmenu_resolution.addItem("832x624")
        dropdwnmenu_resolution.addItem("1024x768")
        dropdwnmenu_resolution.addItem("1280x720")
        dropdwnmenu_resolution.addItem("1280x768")
        dropdwnmenu_resolution.addItem("1280x800")
        dropdwnmenu_resolution.addItem("1280x960")
        dropdwnmenu_resolution.addItem("1280x1024")
        dropdwnmenu_resolution.addItem("1360x768")
        dropdwnmenu_resolution.addItem("1360x1024")
        dropdwnmenu_resolution.addItem("1366x768")
        dropdwnmenu_resolution.addItem("1440x900")
        dropdwnmenu_resolution.addItem("1600x900")
        dropdwnmenu_resolution.addItem("1680x1050")
        dropdwnmenu_resolution.addItem("1920x1080")
        label_fullscreen = SettingsLabel('Fullscreen')
        dropdwnmenu_fullscreen = QComboBox(frame_settings)
        dropdwnmenu_fullscreen.setStyleSheet("background-color: #313031; color: white")
        dropdwnmenu_fullscreen.addItem("Fullscreen")
        dropdwnmenu_fullscreen.addItem("Fullscreen Borderless")
        dropdwnmenu_fullscreen.addItem("Windowed")
        label_renderer = SettingsLabel('Renderer')
        dropdwnmenu_renderer = QComboBox(frame_settings)
        dropdwnmenu_renderer.setStyleSheet("background-color: #313031; color: white")
        dropdwnmenu_renderer.addItem("DirectX 8")
        dropdwnmenu_renderer.addItem("DirectX 9")
        dropdwnmenu_renderer.addItem("DirectX 10")
        dropdwnmenu_renderer.addItem("DirectX 11")
        label_shadowmaps = SettingsLabel('Shadowmaps')
        dropdwnmenu_shadowmaps = QComboBox(frame_settings)
        dropdwnmenu_shadowmaps.setStyleSheet("background-color: #313031; color: white")
        dropdwnmenu_shadowmaps.addItem("1024 (Might cause visual bugs!)")
        dropdwnmenu_shadowmaps.addItem("1536")
        dropdwnmenu_shadowmaps.addItem("2048")
        dropdwnmenu_shadowmaps.addItem("4096")
        dropdwnmenu_shadowmaps.addItem("8192")
        dropdwnmenu_shadowmaps.setCurrentIndex(1)
        label_debugmode = SettingsLabel('Debug mode')
        chkbox_debug = QCheckBox(frame_settings)
        label_sndprefetch = SettingsLabel('Sound prefetch')
        chkbox_sndprefetch = QCheckBox(frame_settings)
        label_noprefetch = SettingsLabel('No prefetch')
        chkbox_noprefetch = QCheckBox(frame_settings)
        label_discordrpc = SettingsLabel('Discord Rich Presence')
        chkbox_discordrpc = QCheckBox(frame_settings)
        label_avx = SettingsLabel('Support for AVX CPU')
        chkbox_avx = QCheckBox(frame_settings)
        label_wipecache = SettingsLabel('Delete Shaders Cache')
        chkbox_wipecache = QCheckBox(frame_settings)

        # Putting the labels+boxes in the grid
        grid_settings.addWidget(label_resolution, 0, 0)
        grid_settings.addWidget(dropdwnmenu_resolution, 0, 1)
        grid_settings.addWidget(label_fullscreen, 1, 0)
        grid_settings.addWidget(dropdwnmenu_fullscreen, 1, 1)
        grid_settings.addWidget(label_renderer, 2, 0)
        grid_settings.addWidget(dropdwnmenu_renderer, 2, 1)
        grid_settings.addWidget(label_shadowmaps, 3, 0)
        grid_settings.addWidget(dropdwnmenu_shadowmaps, 3, 1)
        grid_settings.addWidget(label_debugmode, 4, 0)
        grid_settings.addWidget(chkbox_debug, 4, 1)
        grid_settings.addWidget(label_sndprefetch, 5, 0)
        grid_settings.addWidget(chkbox_sndprefetch, 5, 1)
        grid_settings.addWidget(label_noprefetch, 6, 0)
        grid_settings.addWidget(chkbox_noprefetch, 6, 1)
        grid_settings.addWidget(label_discordrpc, 7, 0)
        grid_settings.addWidget(chkbox_discordrpc, 7, 1)
        grid_settings.addWidget(label_avx, 8, 0)
        grid_settings.addWidget(chkbox_avx, 8, 1)
        grid_settings.addWidget(label_wipecache, 9, 0)
        grid_settings.addWidget(chkbox_wipecache, 9, 1)

        # Setting up options references.
        arr_vid_mode = ['800x600', '832x624', '1024x768', '1280x720', '1280x768', '1280x800', '1280x960',
                        '1280x1024', '1360x768', '1360x1024', '1366x768', '1440x900', '1600x900', '1680x1050',
                        '1920x1080']
        arr_rndr = ["renderer_r1", "renderer_r2", "renderer_r3", "renderer_r4"]
        arr_smaps = ["-smap1024", "-smap1536", "-smap2048", "-smap4096",
                     "-smap8192"]  # I could rip the number off the rest of the string, but that would just take processing time to save a tiny bit of memory.
        arr_options_array = [arr_vid_mode, arr_rndr, arr_smaps]

        # Array with references to the menus and checkboxes to be updated/saved.
        ref_arr = [dropdwnmenu_resolution, dropdwnmenu_fullscreen, dropdwnmenu_renderer,
                   dropdwnmenu_shadowmaps, chkbox_debug, chkbox_sndprefetch, chkbox_noprefetch,
                   chkbox_discordrpc, chkbox_avx, chkbox_wipecache]

        self.updateOptions(ref_arr, arr_options_array, f_ud, f_cd, f_ld)

    def openSettingsFile(self, path_file, path_backup):

        if not path.exists(path_file):
            shutil.copy(path_backup, path_file)
        file = open(path_file)
        file_data = file.read()
        file.close()
        return file_data

    def saveCurrentSettings(self, reference_array, array_options, file_user_data, file_commandline_data, file_launcher_data):

        index_res = reference_array[0].currentIndex()
        repl_res = array_options[0][index_res]
        pattern_res = re.compile('vid_mode \d{2}\d*x\d{2}\d*', re.IGNORECASE)
        file_user_data = re.sub(pattern_res, 'vid_mode ' + repl_res, file_user_data)

        index_rndr = reference_array[2].currentIndex()
        repl_rndr = array_options[1][index_rndr]
        pattern_rndr = re.compile('renderer \w+\d\.*\d*', re.IGNORECASE)
        file_user_data = re.sub(pattern_rndr, 'renderer ' + repl_rndr, file_user_data)

        index_smap = reference_array[3].currentIndex()
        repl_smap = array_options[2][index_smap]
        matchobj_shadowmaps = re.search('-smap\d{3}\d*', file_commandline_data)  # -smap2048
        if type(matchobj_shadowmaps) == re.Match:
            file_commandline_data = re.sub('-smap\d{3}\d*', repl_smap, file_commandline_data)
        else:
            file_commandline_data += '\n' + repl_smap

        index_fscreen = reference_array[1].currentIndex()
        if index_fscreen == 0:  # Fullscreen
            file_user_data = re.sub('rs_fullscreen \w\w\w*', 'rs_fullscreen on', file_user_data)
            file_user_data = re.sub('rs_borderless \d', 'rs_borderless 0', file_user_data)
        elif index_fscreen == 1:  # Fullscreen borderless
            file_user_data = re.sub('rs_fullscreen \w\w\w*', 'rs_fullscreen on', file_user_data)
            file_user_data = re.sub('rs_borderless \d', 'rs_borderless 1', file_user_data)
        elif index_fscreen == 2:  # Windowed
            file_user_data = re.sub('rs_fullscreen \w\w\w*', 'rs_fullscreen off', file_user_data)
            file_user_data = re.sub('rs_borderless \d', 'rs_borderless 1', file_user_data)

        if reference_array[4].isChecked():  # debug
            matchobj_check_dbg = re.search('-dbg', file_commandline_data)
            if type(matchobj_check_dbg) != re.Match:
                file_commandline_data += '\n-dbg'
        elif not reference_array[4].isChecked():
            file_commandline_data = re.sub('\n-dbg', '', file_commandline_data)

        if reference_array[5].isChecked():  # sound prefetch
            matchobj_check_prefetchsounds = re.search('-prefetch_sounds', file_commandline_data)
            if type(matchobj_check_prefetchsounds) != re.Match:
                file_commandline_data += '\n-prefetch_sounds'
        elif not reference_array[5].isChecked():
            file_commandline_data = re.sub('\n-prefetch_sounds', '', file_commandline_data)

        if reference_array[6].isChecked():  # no prefetch
            matchobj_check_noprefetch = re.search('-no_prefetch', file_commandline_data)
            if type(matchobj_check_noprefetch) != re.Match:
                file_commandline_data += '\n-no_prefetch'
        elif not reference_array[6].isChecked():
            file_commandline_data = re.sub('\n-no_prefetch', '', file_commandline_data)

        if reference_array[7].isChecked():  # discord rpc
            file_user_data = re.sub('discord_status \d', 'discord_status 1', file_user_data)
        elif not reference_array[7].isChecked():
            file_user_data = re.sub('discord_status \d', 'discord_status 0', file_user_data)

        if reference_array[8].isChecked():  # avx support
            file_launcher_data = re.sub('avx_support \d', 'avx_support 1', file_launcher_data)
        elif not reference_array[8].isChecked():
            file_launcher_data = re.sub('avx_support \d', 'avx_support 0', file_launcher_data)

        if reference_array[9].isChecked():  # wipe shaders cache
            file_launcher_data = re.sub('wipe_shaders \d', 'wipe_shaders 1', file_launcher_data)
        elif not reference_array[9].isChecked():
            file_launcher_data = re.sub('wipe_shaders \d', 'wipe_shaders 0', file_launcher_data)

        # delete user.ltx to create a new one
        if path.exists(self.LAUNCHER_DIRECTORY + '\\appdata\\user.ltx'):
            remove(self.LAUNCHER_DIRECTORY + '\\appdata\\user.ltx')
        file_tosave_user = open(self.LAUNCHER_DIRECTORY + '\\appdata\\user.ltx', 'w')
        file_tosave_user.write(file_user_data)
        file_tosave_user.close()

        # delete commandline.txt to create a new one
        if path.exists(self.LAUNCHER_DIRECTORY + '\\commandline.txt'):
            remove(self.LAUNCHER_DIRECTORY + '\\commandline.txt')
        file_tosave_commandline = open(self.LAUNCHER_DIRECTORY + '\\commandline.txt', 'w')
        file_tosave_commandline.write(file_commandline_data)
        file_tosave_commandline.close()

        # delete launcher_data.txt to create a new one
        if path.exists(self.LAUNCHER_DIRECTORY + '\\launcher_data.txt'):
            remove(self.LAUNCHER_DIRECTORY + '\\launcher_data.txt')
        file_tosave_launcher_data = open(self.LAUNCHER_DIRECTORY + '\\launcher_data.txt', 'w')
        file_tosave_launcher_data.write(file_launcher_data)
        file_tosave_launcher_data.close()

    def updateOptions(self, reference_array, options_array, file_user_data, file_commandline_data, file_launcher_data):

        # reading user.ltx -> resolution, putting user's settings by default
        matchobj_resolution = re.search('vid_mode \d{2}\d*x\d{2}\d*', file_user_data)  # vid_mode 1366x768
        line_resolution = matchobj_resolution.group().split(" ")
        self.loadUserLTXSetting(options_array[0], reference_array[0], line_resolution[1])

        # reading user.ltx -> fullscreen state, !!DEFAULT: FULLSCREEN
        matchobj_fullscreen = re.search('rs_fullscreen \w\w\w*', file_user_data)  # rs_fullscreen off
        line_fullscreen = matchobj_fullscreen.group().split(" ")
        # reading user.ltx -> borderless state
        matchobj_borderless = re.search('rs_borderless \d', file_user_data)  # rs_borderless 0
        line_borderless = matchobj_borderless.group().split(" ")
        # updating fullscreen settings
        if line_fullscreen[1] == "on":
            if line_borderless[1] == '1':
                reference_array[1].setCurrentIndex(1)
            else:
                reference_array[1].setCurrentIndex(0)
        else:
            reference_array[1].setCurrentIndex(2)

        # reading user.ltx -> renderer; CAN RECYCLE FUNCTION FOR VMA/RENDERER
        matchobj_renderer = re.search('renderer \w+\d.*\d*', file_user_data)  # renderer renderer_r2.5
        line_renderer = matchobj_renderer.group().split(" ")
        self.loadUserLTXSetting(options_array[1], reference_array[2], line_renderer[1])

        # reading commandline.txt -> smap amount
        matchobj_shadowmaps = re.search('-smap\d{3}\d*', file_commandline_data)  # -smap2048
        if type(matchobj_shadowmaps) != re.Match:
            line_shadowmaps = options_array[2][0]
        else:
            line_shadowmaps = matchobj_shadowmaps.group()
        self.loadUserLTXSetting(options_array[2], reference_array[3], line_shadowmaps)

        # commandline.txt -> -dbg
        self.loadCommandlineSetting(file_commandline_data, reference_array[4], '-dbg')

        # commandline.txt -> -soundprefetch
        self.loadCommandlineSetting(file_commandline_data, reference_array[5], '-prefetch_sounds')

        # commandline.txt -> -no_prefetch
        self.loadCommandlineSetting(file_commandline_data, reference_array[6], '-no_prefetch')

        # user.ltx -> discord rich presence
        matchobj_discordrpc = re.search('discord_status \d', file_user_data)  # discord_status 1
        line_discordrpc = matchobj_discordrpc.group().split(" ")[1]
        if line_discordrpc == '0':
            reference_array[7].setChecked(False)
        else:
            reference_array[7].setChecked(True)

        # check if AVX setting is on or off
        matchobj_avx = re.search('avx_support \d', file_launcher_data)  # avx
        line_avx = matchobj_avx.group().split(" ")[1]
        if line_avx == '0':
            reference_array[8].setChecked(False)
        else:
            reference_array[8].setChecked(True)

        matchobj_wipecache = re.search('wipe_shaders \d', file_launcher_data)  # wipe shaders cache
        line_wipecache = matchobj_wipecache.group().split(" ")[1]
        if line_wipecache == '0':
            reference_array[9].setChecked(False)
        else:
            reference_array[9].setChecked(True)

    def loadCommandlineSetting(self, data_commline, ref_arr, lookfor):
        matchobj = re.search(lookfor, data_commline)  # -dbg
        if type(matchobj) is re.Match:
            line = matchobj.group()
        else:  # no match
            line = ''
        if line == lookfor:
            ref_arr.setChecked(True)
        elif line == "":
            ref_arr.setChecked(False)

    def toggleFrame(self, frame):
        if not frame.isHidden():
            frame.hide()
        else:
            frame.show()

    def openLogsFolder(self):
        popen('start explorer "%s" ' % self.LAUNCHER_DIRECTORY + '\\appdata')

    def launchGame(self):
        file_user_data = self.openSettingsFile(self.LAUNCHER_DIRECTORY + '\\appdata\\user.ltx',
                                               self.LAUNCHER_DIRECTORY + '\\launcher\\user_backup.ltx')

        file_launcher_data = self.openSettingsFile(self.LAUNCHER_DIRECTORY + '\\launcher_data.txt',
                                                   self.LAUNCHER_DIRECTORY + '\\launcher\\launcher_data_backup.txt')

        matchobj_renderer = re.search('renderer \w+\d.*\d*', file_user_data) # renderer
        line_renderer = matchobj_renderer.group().split(" ")[1]
        matchobj_avx = re.search('avx_support \d', file_launcher_data)  # avx
        line_avx = matchobj_avx.group().split(" ")[1]
        matchobj_wipecache = re.search('wipe_shaders \d', file_launcher_data)  # wipe shaders cache
        line_wipecache = matchobj_wipecache.group().split(" ")[1]

        if line_renderer == 'renderer_r1':
            target = self.LAUNCHER_DIRECTORY + '\\bin\\AnomalyDX8'
        elif line_renderer == 'renderer_r2':
            target = self.LAUNCHER_DIRECTORY + '\\bin\\AnomalyDX9'
        elif line_renderer == 'renderer_r3':
            target = self.LAUNCHER_DIRECTORY + '\\bin\\AnomalyDX10'
        else:
            target = self.LAUNCHER_DIRECTORY + '\\bin\\AnomalyDX11'

        if line_avx == '1':
            target += 'AVX'

        if line_wipecache == '1':
            self.deleteShadersCache()

        startfile(target)

    def loadUserLTXSetting(self, arr, opt, match):
        index = 0
        while index < len(arr):
            if arr[index] == match:
                opt.setCurrentIndex(index)
                index += len(arr)
            index += 1

    def deleteShadersCache(self):
        path_dir = self.LAUNCHER_DIRECTORY + '\\appdata\\shaders_cache'
        if path.exists(path_dir) and path.isdir(path_dir):
            shutil.rmtree(path_dir)

    def center(self):
        window_space = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_space.moveCenter(screen_center)
        self.move(window_space.topLeft())

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)     # borderless mode
        self.setGeometry(0, 0, 962, 493)    # set the size of the Launchers window to fit the image size

        file_user_data = self.openSettingsFile(self.LAUNCHER_DIRECTORY + '\\appdata\\user.ltx',
                                               self.LAUNCHER_DIRECTORY + '\\launcher\\user_backup.ltx')

        file_commandline_data = self.openSettingsFile(self.LAUNCHER_DIRECTORY + '\\commandline.txt',
                                                      self.LAUNCHER_DIRECTORY + '\\launcher\\commandline_backup.txt')

        file_launcher_data = self.openSettingsFile(self.LAUNCHER_DIRECTORY + '\\launcher_data.txt',
                                                      self.LAUNCHER_DIRECTORY + '\\launcher\\launcher_data_backup.txt')

        self.initBG()
        self.initMainButtons()
        self.initSocMediaButtons()
        self.initOptionsMenu(file_user_data, file_commandline_data, file_launcher_data)
        self.center()
        self.show()


# Runs app
if __name__ == '__main__':
    app = QApplication(argv)
    launcher = Launcher()
    exit(app.exec_())





