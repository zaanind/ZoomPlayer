# define name of installer
Name "zoom player Installer"
OutFile "installer.exe"
 
# define installation directory
InstallDir "$PROGRAMFILES\zoom player"
 
# For removing Start Menu shortcut in Windows 7
RequestExecutionLevel admin
 
# start default section
Section
 
    # set the installation directory as the destination for the following actions
    SetOutPath $INSTDIR
	
	  SetOutPath "$INSTDIR"
    File "zoom player\zoom player.exe"
    File "zoom player\images.ico"
    File "zoom player\images.png"
    File "zoom player\loading.gif"
	File "zoom player\vlc.exe"
	File "zoom player\axvlc.dll"
    File "zoom player\libvlc.dll"
    File "zoom player\npvlc.dll"
    File "zoom player\vlc.exe"
    File "zoom player\libvlccore.dll"
	
	


    # create the uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
 
    # create a shortcut named "new shortcut" in the start menu programs directory
    # point the new shortcut at the program uninstaller
	CreateShortcut "$DESKTOP\Zoom Player.lnk" "$INSTDIR\zoom player.exe"
	
    CreateShortcut "$SMPROGRAMS\zoom player\zoom player.lnk" "$INSTDIR\zoom player.exe"
	
	
		 SetOutPath "$INSTDIR\plugins"
	File /r "zoom player\plugins\*" 
	
SectionEnd
 
# uninstaller section start
Section "uninstall"
 
    # Remove the link from the start menu
    Delete "$SMPROGRAMS\zoom player\zoom player.lnk"
	Delete "$DESKTOP\zoom player.lnk"
	
    RMDir "$SMPROGRAMS\zoom player"
    Delete "$INSTDIR\zoom player.exe"
    Delete "$INSTDIR\images.ico"
    Delete "$INSTDIR\images.png"
    Delete "$INSTDIR\loading.gif"
	Delete "$INSTDIR\axvlc.dll"
	Delete "$INSTDIR\libvlc.dll"
	Delete "$INSTDIR\npvlc.dll"
	Delete "$INSTDIR\vlc.exe"
	Delete "$INSTDIR\libvlccore.dll"
	RMDir /r "$INSTDIR\plugins"
 
 
 
    # Delete the uninstaller
    Delete $INSTDIR\uninstall.exe
 
    RMDir $INSTDIR
# uninstaller section end
SectionEnd