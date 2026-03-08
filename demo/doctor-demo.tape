Output "docs/assets/doctor-demo.gif"

Set Shell "bash"
Set FontSize 22
Set Width 1200
Set Height 900
Set Theme "Builtin Solarized Dark"
Set TypingSpeed 90ms
Set Padding 24

Type "cd /workspace"
Enter
Sleep 1400ms
Type "python3 -m venv /tmp/doctor-demo-venv"
Enter
Sleep 2600ms
Type "source /tmp/doctor-demo-venv/bin/activate"
Enter
Sleep 1200ms
Type "python -m pip install -q -e ."
Enter
Sleep 3200ms

Type "python demo/prepare_doctor_demo_fixture.py"
Enter
Sleep 2200ms

Type "azure-functions doctor --path examples/v2/http-trigger --profile minimal"
Enter
Sleep 3200ms

Type "azure-functions doctor --path demo/.preview/broken-http-trigger --profile minimal"
Enter
Sleep 4200ms
