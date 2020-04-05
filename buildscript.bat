REM cd ../..&&buildscript&&cd __pyinst__\dist&&counter -f ..\..\sessions\session_edcfac715c4ad4a1a39c.pickle

REM rm __pyinst__/dist __pyinst__/build -vfr
rm __pyinst__/*.exe -r
pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --clean --onefile --noupx counter.py -i __pyinst__/counter.ico
mv __pyinst__/dist/counter.exe __pyinst__/
pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --clean --onefile --noupx configGen.py
mv __pyinst__/dist/configGen.exe __pyinst__/
REM pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --clean --onefile --noupx upgrader.py
REM mv __pyinst__/dist/upgrader.exe __pyinst__/

cp config.json __pyinst__/dist/config.json