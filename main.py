import os
import io
import sys
import base64
import vlc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFrame 
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout ,QSlider ,QLabel , QShortcut 
from PyQt5.QtWidgets import QPushButton,  QDesktopWidget, QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QMovie, QKeySequence
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import timedelta
from ctypes import cryptography





from PyQt5.QtGui import QCursor, QGuiApplication




################################### SET GUI ##########################
class zmplayer(QtWidgets.QMainWindow):



    def __init__(self):
        super().__init__()
        
        
        # Set up the user interface
        self.setWindowTitle("Zoom Player")
        self.setGeometry(100, 100, 810, 600)
        self.setFixedSize(810, 600)


          # Set the fixed size of the main window
        #self.setFixedSize(800, 600)
        

        
        icon = QtGui.QIcon("images.png")
        self.setWindowIcon(icon)

        self.video_opened = False
        
        
        self.timer = qtc.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateUI)
        
          # Set up timer to check for bottom screen hover
        self.hover_timer = qtc.QTimer(self)
        self.hover_timer.setInterval(100) # set the interval to check for hover
        self.hover_timer.timeout.connect(self.check_hover)

    
        

        


  

       #show video on ui 
        self.vlc_widget = QtWidgets.QFrame(self)
        self.vlc_widget.setGeometry(17, 30, 780, 500)
        self.vlc_widget.setStyleSheet("margin-left: 20px; margin-right: 20px;")
        self.palette = self.vlc_widget.palette()
        self.palette.setColor (qtg.QPalette.Window,
                             qtg.QColor(0,0,0))
        self.vlc_widget.setPalette(self.palette)
        self.vlc_widget.setAutoFillBackground(True)
        

        self.vlc_widget.show()
        self.player.set_hwnd(self.vlc_widget.winId())
       
      



  


######set seekbar
    #Position Slider
        self.positionslider = qtw.QSlider(qtc.Qt.Horizontal, self)
        self.positionslider.setToolTip("Seek (Left/Right)")
        self.positionslider.setMaximum(100000.0)
        self.positionslider.setTickPosition(qtw.QSlider.TicksBelow)
        self.positionslider.setTickInterval(2000)
        self.positionslider.sliderMoved.connect(self.setPosition)
        self.positionslider.setGeometry(QtCore.QRect(90, 540, 450, 30))

        
        

        self.volumeslider = qtw.QSlider(qtc.Qt.Horizontal, self)
        #self.volumeslider.setTickPosition(qtw.QSlider.TicksBelow)
        #self.volumeslider.setTickInterval(2000)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.player.audio_get_volume())
        self.volumeslider.setToolTip("Volume (up-down/scroll)")
        self.volumeslider.sliderMoved.connect(self.setVolume)
        self.volumeslider.setGeometry(QtCore.QRect(630, 540, 100, 30))
        self.volumeslider.show()
        self.key = Fernet.generate_key()
         
    

     
        
 
        #show time
        self.playback_time_label = QLabel("00:00:00", self)
        self.playback_time_label.setGeometry(QtCore.QRect(400, 540, 360, 20))
        self.playback_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.playback_time_label.setStyleSheet("font-size: 13px;")
        self.playback_time_label.show()
      
            #Volume slider
        



        self.play_button = QPushButton("Play", self)
        self.play_button.setToolTip("play/puse (space)")
        self.play_button.clicked.connect(self.play_pause)
        self.play_button.setGeometry(20, 540, 60, 30)
     
        
        self.full_button = QPushButton("Full Screen", self)
        self.full_button.setToolTip("Full Screen (F)")
        self.full_button.clicked.connect(self.fullvid)
        self.full_button.setGeometry(735, 540, 65, 30)

   
    
   




    

        # Create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        Audiolist = menubar.addMenu("Audio")
        #self.Audiolist.triggered.connect(self.show_audio_selection_dialog)
        
        developer = menubar.addMenu("About")
        


        aul = QtWidgets.QAction("Select Audio Track", self)
        aul.triggered.connect(self.show_audio_selection_dialog)
        Audiolist.addAction(aul)

    
        dev = QtWidgets.QAction("Help", self)
        dev.triggered.connect(self.show_help_dialog)
        developer.addAction(dev)


        open_video_action = QtWidgets.QAction("Open video", self)
        open_video_action.setShortcut("Ctrl+V")
        open_video_action.triggered.connect(self.open_video)
        file_menu.addAction(open_video_action)

        # Add a "Open" action to the file menu
        open_action = QtWidgets.QAction("Open Subtitle file", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_subtitle)
        file_menu.addAction(open_action)


        en_action = QtWidgets.QAction("Encrypt Subtitle file", self)
        en_action.setShortcut("Ctrl+E")
        en_action.triggered.connect(self.show_encrypt_dialog)
        file_menu.addAction(en_action)

   #### shortcuts ####
    

        self.shortcut = QShortcut(QKeySequence("space"), self)
        self.shortcut.activated.connect(self.play_pause)

        self.shortcut = QShortcut(QKeySequence("F"), self)
        self.shortcut.activated.connect(self.fullvid)

        self.shortcut = QShortcut(QKeySequence("Escape"), self)
        self.shortcut.activated.connect(self.fullvid)


        self.shortcut = QShortcut(QKeySequence("Left"), self)
        self.shortcut.activated.connect(self.move_video_left)
         
        self.shortcut = QShortcut(QKeySequence("Right"), self)
        self.shortcut.activated.connect(self.move_video_right)


        self.shortcut = QShortcut(QKeySequence("up"), self)
        self.shortcut.activated.connect(self.volume_up)
         
        self.shortcut = QShortcut(QKeySequence("down"), self)
        self.shortcut.activated.connect(self.volume_down)

     
        self.show()

   
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            vol = self.player.audio_get_volume()
            if vol < 100:
                vol = min(vol + 5, 100)
                self.setVolume(vol)
        else:
            vol = self.player.audio_get_volume()
            if vol > 0:
                vol = max(vol - 5, 0)
                self.setVolume(vol)
    
    pass
 

 
     

    def open_video(self):
       options = QtWidgets.QFileDialog.Options()
       options |= QtWidgets.QFileDialog.ReadOnly
       file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Video", "", "All Files (*)", options=options)
       if file_name:
            
          self.player.set_media(self.instance.media_new(file_name))
          self.timer.start()
          self.on_video_opened()
        
        #  self.player.play()
          self.play_pause()
          self.video_opened = True
          self.timer.start()
         

       else:
            self.player.set_media(self.instance.media_new(file_name))
            print("Unsupported Format")
    pass      
           

    def open_subtitle(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly


        filter_str = "Subtitle (*.esub);;All Files (*)"
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Subtitle", "", filter_str, options=options)  
        

        if not file_name:
            # The user cancelled the file open dialog, so don't do anything
            return
            
        try:

            file_ext = os.path.splitext(file_name)[1]

            if file_ext == ".esub":
                print("esub")
                # Read the encrypted file

                with open(file_name, 'rb') as f:
                    encrypted_data = f.read()

       decrypted_data = fernet.decrypt(encrypted_data)
                



                subtitle = vlc.Media(decrypted_data)

                

                self.player.add_slave(vlc.MediaSlaveType.subtitle, subtitle.get_mrl(), b_select=True)
             
               
                
  
                   


            elif file_ext in (".ass", ".srt", ".vtt"):

               
               subtitle = vlc.Media(file_name)

               self.player.add_slave(vlc.MediaSlaveType.subtitle, subtitle.get_mrl(), b_select=True)

            
            

        except Exception as e:
            # Handle any errors that occur while trying to add the subtitle track
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return
    pass

            
           

    
    pass

    def setVolume(self, Volume):
        self.player.audio_set_volume(Volume)
    pass

    def stop_video(self):
     self.player.stop()
     self.player.release()
    pass
         
    def play_pause(self):
        """Toggle play/pause status
        """
        if self.player.is_playing():
            self.player.pause()
            self.play_button.setText("Play")
            self.isPaused = True
        else:
            if self.player.play() == -1:
                self.open_video()
                return
            self.player.play()
            self.play_button.setText("Pause")
            self.timer.start()
           
            self.isPaused = False
          

    pass
    

       def PausePlay(self):
    
        if self.player.is_playing():
          self.player.pause()
          self.play_button.setText("Play")
          self.isPaused = True
    pass
   

    
    def setsub2(self):
     ###set sub##
      
           self.player.video_set_subtitle_file()
 
                  
    pass 

    
    


    
    def on_video_opened(self):
        self.timer.start()
      

    pass
    




    def updateUI(self):
          time = self.player.get_time()
          formatted_time = timedelta(milliseconds=time)
          formatted_time = str(formatted_time).split(".")[0]
          self.positionslider.setValue(self.player.get_position() * 100000.0)
          self.playback_time_label.setText(formatted_time)
          self.volumeslider.setValue(self.player.audio_get_volume())

          if not self.player.is_playing():
    
           self.timer.stop()


    pass
    
   


    

    
    

  def show_help_dialog(self):
        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle("Help")
        dialog.setTextFormat(QtCore.Qt.RichText)
       dialog.setText("Developer: Sahan Induvara (zaanind)<br><br>"
                   "&emsp;GitHub: <a href='https://github.com/zaanind/zoomplayer/issues'>https://github.com/zaanind/zoomplayer/issues</a><br>"    
                   "&emsp;GitHub Wiki (tutorials): <a href='https://github.com/zaanind/zoomplayer/wiki'>https://github.com/zaanind/zoomplayer/wiki</a><br><br>"                  
                                 
                   "Contact: <br><br>"
                   "&emsp;Email: zaanind@gmail.com<br>"
                    "&emsp;Facebook Id: <a href='https://fb.com/zaanind'>https://fb.com/zaanind</a><br>"
                  
                   "&emsp;Telegram: <a href='https://t.me/zaanind'>https://t.me/zaanind</a><br>"
                   "&emsp;Facebook Page: <a href='https://www.facebook.com/zoomwebsite'>https://www.facebook.com/zoomwebsite</a><br>"
                   "Website: <a href='https://www.zoom.lk'>https://www.zoom.lk</a>")
        dialog.exec_()
    pass


    def show_audio_selection_dialog(self):
        audio_tracks = list(self.player.audio_get_track_description())
        dialog = AudioSelectionDialog(audio_tracks, self)

        audio_tracks = self.player.audio_get_track_description()
        dialog = AudioSelectionDialog(audio_tracks, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            track_id = dialog.get_selected_audio_track()
            if track_id is not None:
                self.player.audio_set_track(track_id)
    
    pass



    def show_encrypt_dialog(self):
            dialog = EncryptDialog(self)
      #  dialog.finished.connect(dialog.deleteLater)
            dialog.show()
    pass




class EncryptDialog(QDialog):
    def __init__(self, parent=None):
        super(EncryptDialog, self).__init__(parent)
        self.setWindowTitle("Encrypt File")
           # Create widgets for file selection and encryption key input
        self.file_label = QLabel("File to Encrypt:")
        self.file_edit = QtWidgets.QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        self.eout = QLabel("Output Dir")
        self.eoutedit = QtWidgets.QLineEdit()

        self.browseout_button = QPushButton("Browse")
        self.browseout_button.clicked.connect(self.browse_file_out)



        # Create button to start encryption
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_file)
        

        # Create layout for widgets
        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.eout)
        layout.addWidget(self.eoutedit)
        layout.addWidget(self.browseout_button)
       
        layout.addWidget(self.encrypt_button)
        
        self.setLayout(layout)

    
    def browse_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File to Encrypt", "", "All Files (*.*)")      
        if filename:
            self.file_edit.setText(filename)


    def browse_file_out(self):
        # Create a file dialog to get the save directory path
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        save_filename = QtWidgets.QFileDialog.getExistingDirectory(self, "Save Encrypted File To", options=options)


        # Check if the user clicked cancel or did not select a directory
        if not save_filename:
            return 
        if save_filename:
                file_name_forsave = "encryptedsub.esub"
                save_filename_fixed = save_filename + "/" + file_name_forsave
                self.eoutedit.setText(save_filename_fixed)
    


  
    def encrypt_file(self):
        # Replace "your_secret_key_here" with your own key
        

        cipher = Fernet(self.tbdr)



        # Read the contents of the file to encrypt
        with open(self.file_edit.text(), "rb") as f:
            data = f.read()

        

        # Encrypt the file data
        encrypted_data = cipher.encrypt(data)

        # Write the encrypted data to a new file

        save_filename = self.eoutedit.text()

       
        if save_filename:
            f.write(encrypted_data)
              to (save_filename)
                QtWidgets.QMessageBox.information(self, "Encryption Complete", "File has been encrypted and saved successfully.")

    


class AudioSelectionDialog(QtWidgets.QDialog):
    def __init__(self, audio_tracks, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Audio Track")
        layout = QtWidgets.QVBoxLayout(self)
        self.list_widget = QtWidgets.QListWidget(self)
        layout.addWidget(self.list_widget)
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        layout.addWidget(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)






    ##run
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = zmplayer()



