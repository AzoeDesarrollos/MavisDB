
name "PyMavis Custom DataBase"
OutFile "instalar.exe"
BrandingText "PyMavisCustomDataBase (installer by NSIS)"
InstallDir $DESKTOP

PageEx directory
	Caption "PMCDB: Directorio de instalación"
	DirText "PMCDB se instalará en el siguiente directorio. Para seleccionar un directorio diferente, haga clic en Buscar y elija un directorio distinto." "Destino" "Buscar" "Seleccione el directorio donde se realizará la instalación de PMCDB"
PageExEnd

PageEx instfiles
	Caption "PMCDB: Instalando componentes"
PageExEnd

Section "PMCDB"
    SetOutPath $INSTDIR
    WriteUninstaller Desisntalar.exe
    File "main.exe"
    File "leeme.txt"
    File "python37.dll"

    SetOutPath $INSTDIR\lib
    File /r lib\*.*

    CreateDirectory $INSTDIR\data
    CreateShortcut "PMCDB.lnk" "$INSTDIR\main.exe"
SectionEnd

Section "Uninstall"
	Delete $INSTDIR\Desisntalar.exe ; delete self
	RMDir /r $INSTDIR
SectionEnd