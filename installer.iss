; Inno Setup Script for DNS Manager Pro
; Professional Windows Installer
; Install Inno Setup from: https://jrsoftware.org/isdl.php
; Build command: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

#define MyAppName "DNS Manager Pro"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Ali Jabbary"
#define MyAppURL "https://alijabbary.com"
#define MyAppGitHub "https://github.com/ali-kin4/DNSManager"
#define MyAppExeName "DNSManagerPro.exe"
#define MyAppId "{{A3F5B8C1-2D4E-4F6A-9B7C-1E8D5A9F2C6B}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppGitHub}/issues
AppUpdatesURL={#MyAppGitHub}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=dist\installer
OutputBaseFilename=DNSManagerPro-Setup-v{#MyAppVersion}
SetupIconFile=logo.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Advanced DNS Configuration Tool
VersionInfoCopyright=Copyright (C) 2025 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

; Visuals (commented out - use default Inno Setup images)
; WizardImageFile=compiler:WizModernImage-IS.bmp
; WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "startupicon"; Description: "Run at Windows startup"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\DNSManagerPro.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.svg"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser

[UninstallDelete]
Type: filesandordirs; Name: "{app}\backup"
Type: files; Name: "{app}\dns_configs.json"
Type: files; Name: "{app}\*.log"

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  OldVersion: String;
begin
  Result := True;

  // Check if an older version is installed
  if RegQueryStringValue(HKEY_LOCAL_MACHINE,
     'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1',
     'DisplayVersion', OldVersion) then
  begin
    if MsgBox('Version ' + OldVersion + ' of {#MyAppName} is already installed.' + #13#13 +
              'Do you want to uninstall it and continue with the installation?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Uninstall the old version
      if RegQueryStringValue(HKEY_LOCAL_MACHINE,
         'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1',
         'UninstallString', OldVersion) then
      begin
        Exec(RemoveQuotes(OldVersion), '/VERYSILENT', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      end;
    end
    else
    begin
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Add to Windows Firewall exceptions (optional)
    // Exec('netsh', 'advfirewall firewall add rule name="{#MyAppName}" dir=in action=allow program="' + ExpandConstant('{app}\{#MyAppExeName}') + '" enable=yes', '', SW_HIDE, ewNoWait, ResultCode);
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  if MsgBox('Do you want to keep your DNS configurations?', mbConfirmation, MB_YESNO) = IDYES then
  begin
    // Keep dns_configs.json by creating a backup
    FileCopy(ExpandConstant('{app}\dns_configs.json'),
             ExpandConstant('{userappdata}\{#MyAppName}\dns_configs_backup.json'), False);
  end;
end;
