REM cd ../..&&buildscript&&cd __pyinst__\dist&&counter -f ..\..\sessions\session_edcfac715c4ad4a1a39c.pickle

REM rm __pyinst__/dist __pyinst__/build -vfr
rm __pyinst__/*.exe -r
rem pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --clean --onefile --noupx counter.py -i __pyinst__/counter.ico
REM mv __pyinst__/dist/counter.exe __pyinst__/
rem pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --clean --onefile --noupx configGen.py
REM mv __pyinst__/dist/configGen.exe __pyinst__/
REM pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --clean --onefile --noupx upgrader.py
REM mv __pyinst__/dist/upgrader.exe __pyinst__/

REM ## Using pyenv shit
c:\Users\administrator\.pyenv\pyenv-win\versions\3.8.0\Scripts\pyinstaller.exe --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --onefile --noupx counter.py --hidden-import=jinxed.terminfo.vtwin10
REM -i __pyinst__/counter.ico (disabled because fuck the virus detection)
c:\Users\administrator\.pyenv\pyenv-win\versions\3.8.0\Scripts\pyinstaller.exe --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --onefile --noupx configGen.py

mv __pyinst__/dist/configGen.exe __pyinst__/
mv __pyinst__/dist/counter.exe __pyinst__/

cp config.json __pyinst__/dist/config.json
