REM cd ../..&&buildscript&&cd __pyinst__\dist&&counter -f ..\..\sessions\session_edcfac715c4ad4a1a39c.pickle

REM rm __pyinst__/dist __pyinst__/build -vfr
pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level TRACE --clean --onefile --noupx __pyinst__/counter.spec
cp config.json __pyinst__/dist/config.json