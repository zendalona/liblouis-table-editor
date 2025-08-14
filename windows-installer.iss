[Setup]
AppName=Liblouis-Table-Editor
AppVersion=1.0.0
AppPublisher=zendalona
DefaultDirName={autopf}\Liblouis-Table-Editor
DefaultGroupName=Liblouis-Table-Editor
OutputBaseFilename=Liblouis-Table-Editor-Setup
SetupIconFile=src\liblouis_table_editor\assets\icons\icon.ico
WizardImageFile=src\liblouis_table_editor\assets\images\welcome.bmp
WizardSmallImageFile=src\liblouis_table_editor\assets\images\wizardsmallicon.bmp
LicenseFile=INSTALLER-LICENSE.txt
UninstallDisplayIcon={app}\LiblouisTableEditor.exe
UninstallDisplayName=Liblouis-Table-Editor
AppMutex=LiblouisTableEditor
DisableDirPage=no
DisableProgramGroupPage=no
AllowNoIcons=yes
OutputDir=installer
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\LiblouisTableEditor\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
Source: "src\liblouis_table_editor\assets\icons\icon.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Liblouis-Table-Editor"; Filename: "{app}\LiblouisTableEditor.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall Liblouis-Table-Editor"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Liblouis-Table-Editor"; Filename: "{app}\LiblouisTableEditor.exe"; IconFilename: "{app}\icon.ico"

[Registry]
; Register file associations for .cti files
Root: HKCR; Subkey: ".cti"; ValueType: string; ValueName: ""; ValueData: "LiblouisTableFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: ".cti"; ValueType: string; ValueName: "Content Type"; ValueData: "application/x-liblouis-table"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "LiblouisTableFile"; ValueType: string; ValueName: ""; ValueData: "Liblouis Table File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "LiblouisTableFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\icon.ico"
Root: HKCR; Subkey: "LiblouisTableFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\LiblouisTableEditor.exe"" ""%1"""

; Register file associations for .ctb files
Root: HKCR; Subkey: ".ctb"; ValueType: string; ValueName: ""; ValueData: "LiblouisTableFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: ".ctb"; ValueType: string; ValueName: "Content Type"; ValueData: "application/x-liblouis-table"; Flags: uninsdeletevalue

; Register file associations for .utb files
Root: HKCR; Subkey: ".utb"; ValueType: string; ValueName: ""; ValueData: "LiblouisTableFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: ".utb"; ValueType: string; ValueName: "Content Type"; ValueData: "application/x-liblouis-table"; Flags: uninsdeletevalue

; Add "Open with Liblouis Table Editor" context menu
Root: HKCR; Subkey: "LiblouisTableFile\shell\open"; ValueType: string; ValueName: ""; ValueData: "&Open with Liblouis Table Editor"
Root: HKCR; Subkey: "LiblouisTableFile\shell\open"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\LiblouisTableEditor.exe,0"

; Add to "Open With" list for text files
Root: HKCR; Subkey: "Applications\LiblouisTableEditor.exe"; ValueType: string; ValueName: ""; ValueData: "Liblouis Table Editor"
Root: HKCR; Subkey: "Applications\LiblouisTableEditor.exe"; ValueType: string; ValueName: "FriendlyAppName"; ValueData: "Liblouis Table Editor"
Root: HKCR; Subkey: "Applications\LiblouisTableEditor.exe\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\icon.ico"
Root: HKCR; Subkey: "Applications\LiblouisTableEditor.exe\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\LiblouisTableEditor.exe"" ""%1"""
Root: HKCR; Subkey: "Applications\LiblouisTableEditor.exe\SupportedTypes"; ValueType: string; ValueName: ".cti"; ValueData: ""
Root: HKCR; Subkey: "Applications\LiblouisTableEditor.exe\SupportedTypes"; ValueType: string; ValueName: ".ctb"; ValueData: ""
Root: HKCR; Subkey: "Applications\LiblouisTableEditor.exe\SupportedTypes"; ValueType: string; ValueName: ".utb"; ValueData: ""

[Run]
Filename: "{app}\LiblouisTableEditor.exe"; Description: "Launch Liblouis-Table-Editor"; Flags: nowait postinstall skipifsilent

[Messages]
WelcomeLabel1=Welcome to the Liblouis-Table-Editor Setup Wizard
WelcomeLabel2=This wizard will guide you through the installation of Liblouis-Table-Editor.
FinishedLabel=Setup has finished installing Liblouis-Table-Editor on your computer. The application may be launched by selecting the installed shortcuts.
ExitSetupMessage=Setup is not complete. If you exit now, the program will not be installed.