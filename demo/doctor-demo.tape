Output "docs/assets/doctor-demo.gif"

Set Shell "bash"
Set FontSize 22
Set Width 1200
Set Height 900
Set Theme "Builtin Solarized Dark"
Set TypingSpeed 55ms
Set Padding 24

Hide
Type "python3 -m venv /tmp/doctor-demo-venv"
Enter
Type "/tmp/doctor-demo-venv/bin/pip install -q --upgrade pip"
Enter
Type "/tmp/doctor-demo-venv/bin/pip install -q -e /vhs"
Enter
Type "clear"
Enter
Show

Type "cd /vhs"
Enter
Sleep 700ms

Type "/tmp/doctor-demo-venv/bin/python demo/render_doctor_output.py"
Enter
Sleep 3200ms
