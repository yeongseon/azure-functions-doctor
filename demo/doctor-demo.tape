Output "docs/assets/doctor-demo.gif"

Set Shell "bash"
Set FontSize 22
Set Width 1200
Set Height 900
Set Theme "Builtin Solarized Dark"
Set TypingSpeed 55ms
Set Padding 24

Type "cd /workspace"
Enter
Sleep 900ms
Type "python3 -m venv /tmp/doctor-demo-venv"
Enter
Sleep 1800ms
Type "source /tmp/doctor-demo-venv/bin/activate"
Enter
Sleep 700ms
Type "python -m pip install -q -e ."
Enter
Sleep 2200ms

Type "python demo/preview.py"
Enter
Sleep 3200ms
