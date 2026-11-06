import pathlib
import subprocess
import sys

ROOT = pathlib.Path(r"C:\Users\su\Desktop\JR2CityHall")
WORK = ROOT / "assignment_work"
README = ROOT / "README.md"
OUT = WORK / "test_out"
OUT.mkdir(exist_ok=True)

text = README.read_text(encoding="utf-8")
cases = []
for section in text.split("### Sample case ")[1:]:
    if "**Input**" not in section or "**Expected output**" not in section:
        continue
    num = section.split("\n", 1)[0].strip()
    inp = section.split("**Input**", 1)[1].split("```", 2)[1]
    inp = "\n".join(l for l in inp.splitlines() if l.strip()) + "\n"
    exp = section.split("**Expected output**", 1)[1].split("```", 2)[1]
    cases.append((num, inp, exp))
print("cases found:", len(cases))

failures = 0
report = []
for num, std_input, expected in cases:
    expected_lines = [l.strip() for l in expected.strip().splitlines() if l.strip()]
    input_file = OUT / ("case%s.in" % num)
    input_file.write_text(std_input, encoding="utf-8", newline="\n")
    with open(input_file, "r", encoding="utf-8") as handle:
        result = subprocess.run(
            ["java", "-cp", "src", "Main"],
            cwd=str(WORK), stdin=handle, capture_output=True, text=True,
            encoding="utf-8", errors="strict", timeout=60,
        )
    output = result.stdout
    (OUT / ("case%s.out" % num)).write_text(output, encoding="utf-8", newline="\n")

    # every expected line must appear in the console output, in order
    position = 0
    missing = []
    for want in expected_lines:
        found = output.find(want, position)
        if found < 0:
            missing.append(want)
        else:
            position = found + len(want)

    if result.returncode != 0 or missing:
        failures += 1
        report.append("case %s: FAIL rc=%s missing=%s stderr=%s"
                      % (num, result.returncode, missing[:5], result.stderr[-300:]))
    else:
        report.append("case %s: OK" % num)

(WORK / "test_summary.txt").write_text("\n".join(report), encoding="utf-8", newline="\n")
print("\n".join(report))
print("failures:", failures)
sys.exit(1 if failures else 0)
