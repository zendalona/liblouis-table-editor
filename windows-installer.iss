[Setup]
AppName=Liblouis-Table-Editor
AppVersion=1.0.0
AppPublisher=zendalona
DefaultDirName={autopf}\Liblouis-Table-Editor
DefaultGroupName=Liblouis-Table-Editor
OutputBaseFilename=Liblouis-Table-Editor-Setup
SetupIconFile=src\assets\icons\icon.ico
WizardImageFile=src\assets\images\welcome.bmp
WizardSmallImageFile=src\assets\images\wizardsmallicon.bmp
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
Source: "src\assets\icons\icon.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Liblouis-Table-Editor"; Filename: "{app}\LiblouisTableEditor.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall Liblouis-Table-Editor"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Liblouis-Table-Editor"; Filename: "{app}\LiblouisTableEditor.exe"; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\LiblouisTableEditor.exe"; Description: "Launch Liblouis-Table-Editor"; Flags: nowait postinstall skipifsilent

[Messages]
WelcomeLabel1=Welcome to the Liblouis-Table-Editor Setup Wizard
WelcomeLabel2=This wizard will guide you through the installation of Liblouis-Table-Editor.
FinishedLabel=Setup has finished installing Liblouis-Table-Editor on your computer. The application may be launched by selecting the installed shortcuts.
ExitSetupMessage=Setup is not complete. If you exit now, the program will not be installed.