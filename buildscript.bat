rm __pyinst__/dist __pyinst__/build -vfr
pyinstaller --distpath __pyinst__/dist --workpath __pyinst__/build -y --log-level DEBUG --clean --onefile --noupx __pyinst__/counter.spec