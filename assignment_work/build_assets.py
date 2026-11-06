"""Build every figure and console capture used by the assignment report."""

import os
import pathlib
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(r"C:\Users\su\Desktop\JR2CityHall")
WORK = ROOT / "assignment_work"
SRC = WORK / "src"
OUT = WORK / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Console replay: run the program and echo the typed input
# ---------------------------------------------------------------------------


def replay(input_text):
    lines = [l for l in input_text.splitlines() if l.strip()]
    proc = subprocess.Popen(
        ["java", "-cp", str(SRC), "Main"],
        cwd=str(WORK),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    fd = proc.stdout.fileno()
    transcript = ""
    index = 0
    while True:
        chunk = os.read(fd, 1)
        if not chunk:
            break
        transcript += chunk.decode("utf-8", errors="replace")
        if transcript.endswith(":- ") and index < len(lines):
            transcript += lines[index] + "\n"
            proc.stdin.write((lines[index] + "\n").encode("utf-8"))
            proc.stdin.flush()
            index += 1
    proc.stdin.close()
    proc.wait(timeout=30)
    return transcript


BANNER_PREFIXES = (
    "Smart Delivery Fleet Management System (SDFMS)",
    "c = create fleet",
    "d = delete driver",
    "u = undo, r = redo",
)


def tidy(transcript):
    """Keep the first menu block, drop the repeated menu blocks."""
    rows = transcript.replace("\r\n", "\n").split("\n")
    kept = []
    shown_menu = False
    for line in rows:
        if any(line.startswith(p) for p in BANNER_PREFIXES):
            if not shown_menu and line.startswith("Smart Delivery"):
                shown_menu = True
                kept.append(line)
            continue
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return kept


# ---------------------------------------------------------------------------
# 2. Render a transcript as a console window image
# ---------------------------------------------------------------------------

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\consola.ttf",
    r"C:\Windows\Fonts\cour.ttf",
]


def mono_font(size):
    for path in FONT_CANDIDATES:
        if pathlib.Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render_console(lines, title, path, font_size=13):
    font = mono_font(font_size)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    char_w = max(probe.textlength("M", font=font), 1)
    line_h = font_size + 6
    text_w = max(probe.textlength(l, font=font) for l in lines) if lines else 100
    width = int(text_w) + 44
    title_h = 34
    height = title_h + len(lines) * line_h + 26

    img = Image.new("RGB", (width, height), "#0f1419")
    draw = ImageDraw.Draw(img)
    # title bar
    draw.rectangle([0, 0, width, title_h], fill="#1b2a3a")
    for i, colour in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        draw.ellipse([12 + i * 18, 11, 24 + i * 18, 23], fill=colour)
    draw.text((66, 8), title, font=mono_font(13), fill="#d7e3ef")

    y = title_h + 12
    for line in lines:
        colour = "#d6dCE6"
        if line.startswith("Please enter command") or line.startswith("Enter fleet type") \
                or line.startswith("Role (1 =") or line.startswith("Please input") \
                or line.startswith("Fleet ID:-") or line.startswith("Fleet Name:-"):
            colour = "#7fb3d5"
        elif line.strip() in ("Delivery van fleet is created.",
                              "Refrigerated truck fleet is created.",
                              "Driver is added.", "Driver is deleted.",
                              "Driver role is updated.", "Fleet name is updated.",
                              "Current fleet is changed to F001."):
            colour = "#9ee493"
        elif line.startswith("Command (") or line.startswith("Undo List") \
                or line.startswith("Redo List") or line.startswith("-- End"):
            colour = "#ffd479"
        elif line.startswith(("Fleet ", "Driver ")) and "not found" in line:
            colour = "#ff8f8f"
        elif line.strip() in ("Driver is deleted", "Invalid command!"):
            colour = "#ff8f8f"
        draw.text((22, y), line, font=font, fill=colour)
        y += line_h

    img.save(path)
    return path


# ---------------------------------------------------------------------------
# 3. Class diagram / pattern diagram helpers
# ---------------------------------------------------------------------------


def class_box(ax, x, y, w, h, title, stereo=None, attrs=None, ops=None,
              abstract=False, title_size=10.0, body_size=8.4):
    attrs = attrs or []
    ops = ops or []
    header = 22 if not stereo else 32
    line = 12.2
    height = header + line * (len(attrs) + len(ops)) + (8 if attrs and ops else 0)
    patch = Rectangle((x, y), w, height, facecolor="white", edgecolor="#243b53",
                      linewidth=1.3, zorder=2)
    ax.add_patch(patch)
    # divider under the name compartment
    ax.plot([x, x + w], [y + height - header, y + height - header],
            color="#243b53", linewidth=1.1, zorder=3)
    ty = y + height - 15
    if stereo:
        ax.text(x + w / 2, y + height - 11, stereo, ha="center", va="center",
                fontsize=8.2, style="italic", color="#3a4a5c", zorder=4)
        ty = y + height - 24
    display = title
    ax.text(x + w / 2, ty, display, ha="center", va="center", fontsize=title_size,
            fontweight="bold" if not abstract else "bold",
            style="italic" if abstract else "normal", color="#102a43", zorder=4)

    yy = y + height - header - 10
    for item in attrs:
        ax.text(x + 8, yy, item, ha="left", va="center", fontsize=body_size,
                color="#334e68", zorder=4)
        yy -= line
    if attrs and ops:
        ax.plot([x, x + w], [yy + line / 2, yy + line / 2], color="#243b53",
                linewidth=0.7, zorder=3)
    for item in ops:
        ax.text(x + 8, yy, item, ha="left", va="center", fontsize=body_size,
                color="#334e68", zorder=4)
        yy -= line
    return (x, y, w, height)


def arrow(ax, p1, p2, kind="inherit", label=None, dashed=False, rad=0.0,
          label_offset=(0, 0), fontsize=8):
    style = "-|>" if kind == "inherit" else ("->" if kind == "assoc" else "-")
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=13,
        linewidth=1.1, color="#243b53",
        linestyle="dashed" if dashed else "solid",
        connectionstyle="arc3,rad=%s" % rad, zorder=1,
        shrinkA=0, shrinkB=0))
    if label:
        mx = (p1[0] + p2[0]) / 2 + label_offset[0]
        my = (p1[1] + p2[1]) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fontsize,
                color="#486581", zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


def canvas(width, height):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------------------
# 4. Figure 1 - domain model and command hierarchy
# ---------------------------------------------------------------------------


def figure_domain():
    fig, ax = canvas(15.5, 11.0)

    driver = class_box(ax, 3, 74, 27, 0, "Driver",
                       attrs=["- driverID: String", "- driverName: String",
                              "- role: int"],
                       ops=["+ getDriverID(): String", "+ getName(): String",
                            "+ getRole(): int", "+ setRole(role: int)"])
    memento = class_box(ax, 43, 82, 24, 0, "Memento", stereo="«interface»")
    fname = class_box(ax, 70, 80, 27, 0, "FleetNameMemento",
                      attrs=["- fleetID: String", "- fleetName: String"])
    drole = class_box(ax, 70, 66, 27, 0, "DriverRoleMemento",
                      attrs=["- driverID: String", "- role: int"])

    vfleet = class_box(ax, 3, 40, 31, 0, "VehicleFleet", abstract=True,
                       attrs=["- fleetID: String", "- fleetName: String",
                              "- drivers: AbstractList"],
                       ops=["+ addDriver(d: Driver): void",
                            "+ dropDriver(d: Driver): void",
                            "+ getFleetID(): String",
                            "+ getName(): String",
                            "+ setName(n: String): void",
                            "+ findDriver(id: String): Driver",
                            "+ createFleetNameMemento(): Memento",
                            "+ restoreFleetName(m: Memento): void",
                            "+ updateDriverRole(): void  {abstract}",
                            "+ showFleet(): void          {abstract}"])

    repo = class_box(ax, 40, 44, 27, 0, "FleetRepository",
                     attrs=["- fleets: Vector<VehicleFleet>",
                            "- currentFleet: VehicleFleet"],
                     ops=["+ findFleet(id: String): VehicleFleet",
                          "+ addFleet(f: VehicleFleet): void",
                          "+ removeFleet(f: VehicleFleet): void",
                          "+ getCurrentFleet(): VehicleFleet"])

    cmd = class_box(ax, 70, 40, 28, 0, "Command", stereo="«interface»",
                    ops=["+ execute(): void", "+ undo(): void",
                         "+ redo(): void",
                         "+ getDescription(): String",
                         "+ isUndoable(): boolean"])

    abcmd = class_box(ax, 70, 22, 28, 0, "AbstractCommand", abstract=True,
                      attrs=["- commandCode: String",
                             "# context: CommandContext"],
                      ops=["+ execute(): void  {abstract}",
                           "+ undo(): void", "+ redo(): void"])

    cmds = class_box(ax, 66, 3, 34, 0, "Concrete commands (12)",
                     attrs=["CreateFleetCommand, SetCurrentFleetCommand,",
                            "AddDriverCommand, ModifyDriverRoleCommand,",
                            "DeleteDriverCommand, ShowFleetCommand,",
                            "DisplayAllFleetsCommand, ChangeFleetNameCommand,",
                            "UndoCommand, RedoCommand,",
                            "ShowUndoRedoListCommand, ExitCommand"])

    manager = class_box(ax, 40, 72, 26, 0, "CommandManager",
                        attrs=["- undoList: Vector<Command>",
                               "- redoList: Vector<Command>"],
                        ops=["+ execute(c: Command): void",
                             "+ undo(): void", "+ redo(): void",
                             "+ showLists(): void"])

    dvan = class_box(ax, 3, 8, 26, 0, "DeliveryVanFleet",
                     ops=["+ showFleet(): void",
                          "+ showFleetSummary(): void",
                          "+ getRoleName(role: int): String",
                          "+ getRolePrompt(): String"])
    dtruck = class_box(ax, 31, 8, 30, 0, "RefridgeratedTruckFleet",
                       ops=["+ showFleet(): void",
                            "+ showFleetSummary(): void",
                            "+ getRoleName(role: int): String",
                            "+ getRolePrompt(): String"])

    # inheritance / realisation
    arrow(ax, (16, dvan[1] + dvan[3]), (16, vfleet[1]), "inherit")
    arrow(ax, (46, dtruck[1] + dtruck[3]), (26, vfleet[1]), "inherit")
    arrow(ax, (84, abcmd[1] + abcmd[3]), (84, cmd[1]), "inherit")
    arrow(ax, (83, cmds[1] + cmds[3]), (81, abcmd[1]), "inherit")
    arrow(ax, (73, fname[1]), (63, memento[1] + 6), "inherit", dashed=True)
    arrow(ax, (78, drole[1] + drole[3]), (62, memento[1] + 4), "inherit", dashed=True)

    # associations
    arrow(ax, (30, 80), (20, vfleet[1] + vfleet[3] + 2), "assoc", "1..*", dashed=False,
          rad=-0.15, label_offset=(6, 0))
    arrow(ax, (38, 60), (34, 56), "assoc", "contains", rad=0.0, label_offset=(4, 6))
    arrow(ax, (53, 64), (52, 62), "assoc", "", dashed=False)
    arrow(ax, (60, 40), (66, 34), "assoc", "receiver", label_offset=(4, 8))
    arrow(ax, (40, 88), (34, 62), "assoc", "uses", rad=0.2, label_offset=(-6, 4))

    fig.savefig(OUT / "fig1_domain.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Figure 2 - factory package
# ---------------------------------------------------------------------------


def figure_factory():
    fig, ax = canvas(15.0, 9.5)

    absf = class_box(ax, 34, 82, 32, 0, "SDFMSAbstractFactory", stereo="«interface»",
                     ops=["+ createFleet(code: String, id: String)",
                          "+ createDriver(id: String, name: String, role: int)",
                          "+ createCommand(code: String): Command",
                          "+ isValidFleetType(code: String): boolean"])
    impl = class_box(ax, 34, 56, 32, 0, "SDFMSFactory",
                     attrs=["- fleetFactories: FleetFactoryRegistry",
                            "- driverFactory: DriverFactory",
                            "- commandFactory: CommandFactory"])

    reg = class_box(ax, 3, 56, 27, 0, "FleetFactoryRegistry",
                    attrs=["- factories: Map<String, FleetFactory>"],
                    ops=["+ register(f: FleetFactory): void",
                         "+ getFactory(code: String): FleetFactory",
                         "+ isSupported(code: String): boolean"])

    ff = class_box(ax, 3, 32, 27, 0, "FleetFactory", stereo="«interface»",
                   ops=["+ getTypeCode(): String",
                        "+ getTypeLabel(): String",
                        "+ createFleet(id: String): VehicleFleet"])
    vanf = class_box(ax, 2, 10, 24, 0, "DeliveryVanFleetFactory",
                     ops=["+ createFleet(id): VehicleFleet"])
    refrig = class_box(ax, 28, 10, 27, 0, "RefridgeratedTruckFleetFactory",
                       ops=["+ createFleet(id): VehicleFleet"])

    df = class_box(ax, 62, 32, 25, 0, "DriverFactory", stereo="«interface»",
                   ops=["+ createDriver(id, name, role)"])
    dstd = class_box(ax, 61, 10, 26, 0, "StandardDriverFactory",
                     ops=["+ createDriver(id, name, role)"])

    cf = class_box(ax, 62, 56, 25, 0, "CommandFactory", stereo="«interface»",
                   ops=["+ createCommand(code: String)"])
    cimpl = class_box(ax, 61, 32, 0, 0, "")

    scf = class_box(ax, 62, 32, 24, 0, "SDFMSCommandFactory",
                    attrs=["- context: CommandContext"],
                    ops=["+ createCommand(code: String)"])

    arrow(ax, (50, impl[1] + impl[3]), (50, absf[1]), "inherit")
    arrow(ax, (34, 62), (30, 62), "assoc", "uses", label_offset=(0, 6))
    arrow(ax, (16, reg[1]), (16, ff[1] + ff[3]), "assoc", "1..*", label_offset=(5, 3))
    arrow(ax, (14, vanf[1] + vanf[3]), (14, ff[1]), "inherit")
    arrow(ax, (41, refrig[1] + refrig[3]), (22, ff[1]), "inherit")
    arrow(ax, (74, dstd[1] + dstd[3]), (74, df[1]), "inherit")
    arrow(ax, (74, scf[1] + scf[3]), (74, cf[1]), "inherit")
    arrow(ax, (66, 56), (74, 46), "assoc", "uses", label_offset=(6, 2))

    fig.savefig(OUT / "fig2_factory.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 6. Figure 3 - Command pattern collaboration
# ---------------------------------------------------------------------------


def figure_command():
    fig, ax = canvas(14.5, 7.0)
    ax.set_ylim(0, 60)

    def node(x, y, w, h, title, sub, colour):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6",
                                    facecolor=colour, edgecolor="#243b53",
                                    linewidth=1.2, zorder=2))
        ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="#102a43", zorder=3)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center",
                fontsize=9, color="#334e68", zorder=3)

    node(3, 38, 22, 13, "Client", "SDFMSApplication", "#e8f1fb")
    node(3, 8, 22, 13, "Receiver", "VehicleFleet, Driver,\nFleetRepository", "#eaf6ec")
    node(36, 38, 28, 13, "Invoker", "CommandManager\n(undo / redo lists)", "#fff4e0")
    node(36, 8, 28, 13, "Command «interface»", "Command, AbstractCommand", "#f3e8fb")
    node(74, 8, 23, 13, "ConcreteCommand", "12 command classes", "#f3e8fb")

    arrow(ax, (25, 44), (36, 44), "assoc", "1. create", label_offset=(0, 5))
    arrow(ax, (50, 38), (50, 21), "assoc", "2. execute()", label_offset=(2, 0), rad=0.0)
    arrow(ax, (36, 15), (25, 15), "assoc", "3. action()", label_offset=(0, 5))
    arrow(ax, (74, 15), (64, 15), "assoc", "", dashed=False)
    arrow(ax, (22, 38), (20, 21), "assoc", "4. create / store", label_offset=(8, 0),
          dashed=True)

    ax.text(50, 55, "Command pattern: the request is wrapped in an object, so undo, redo and the",
            ha="center", fontsize=9.5, color="#334e68")
    ax.text(50, 51, "history lists can treat every user function in exactly the same way.",
            ha="center", fontsize=9.5, color="#334e68")

    fig.savefig(OUT / "fig3_command.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. Figure 4 - Memento collaboration
# ---------------------------------------------------------------------------


def figure_memento():
    fig, ax = canvas(14.5, 7.6)
    ax.set_ylim(0, 70)

    lanes = [(16, "Caretaker\nChangeFleetNameCommand"),
             (50, "Originator\nVehicleFleet"),
             (84, "Memento\nFleetNameMemento")]

    for x, label in lanes:
        ax.add_patch(FancyBboxPatch((x - 13, 62), 26, 8,
                                    boxstyle="round,pad=0.4",
                                    facecolor="#e8f1fb", edgecolor="#243b53",
                                    linewidth=1.2, zorder=2))
        ax.text(x, 66, label, ha="center", va="center", fontsize=9.5,
                color="#102a43", zorder=3)
        ax.plot([x, x], [10, 62], linestyle="--", color="#8fa3b8", linewidth=1.0)

    def step(y, x1, x2, text):
        arrow(ax, (x1, y), (x2, y), "event", "", rad=0.0)
        ax.text((x1 + x2) / 2, y + 2.2, text, ha="center", va="center", fontsize=9,
                color="#334e68")

    step(54, 16, 50, "1. createFleetNameMemento()")
    step(46, 50, 84, "2. new FleetNameMemento(fleetID, fleetName)")
    step(38, 84, 50, "3. memento object")
    step(30, 50, 16, "4. keep in command field")
    step(22, 16, 50, "5. undo(): restoreFleetName(memento)")
    step(14, 50, 84, "6. read saved name back")

    ax.text(50, 6, "The command never sees the internal fields of the fleet; the memento is "
                   "an opaque snapshot that only VehicleFleet can read.",
            ha="center", fontsize=9, color="#334e68")

    fig.savefig(OUT / "fig4_memento.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 8. Console captures for the test cases
# ---------------------------------------------------------------------------


def capture(name, input_text, title):
    transcript = replay(input_text)
    lines = tidy(transcript)
    pages = []
    chunk = 38
    parts = [lines[i:i + chunk] for i in range(0, len(lines), chunk)] or [[""]]
    for i, part in enumerate(parts, start=1):
        suffix = "" if len(parts) == 1 else " (%d/%d)" % (i, len(parts))
        path = OUT / ("cap_%s%s.png" % (name, "" if len(parts) == 1 else "_%d" % i))
        render_console(part, title + suffix, path)
        pages.append(path)
    (OUT / ("cap_%s.txt" % name)).write_text("\n".join(lines), encoding="utf-8",
                                            newline="\n")
    return pages


CASES = {
    "tc01": ("c\nv\nF001\nCENTRAL EXPRESS\nx\n", "TC01 - create a delivery van fleet"),
    "tc02": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\n"
             "a\nd002, Jamie Lee\n2\nx\n", "TC02 - add drivers to the fleet"),
    "tc03": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\n"
             "a\nd002, Jamie Lee\n2\nsf\nx\n", "TC03 - show the current fleet"),
    "tc04": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\n"
             "a\nd002, Jamie Lee\n2\nsf\nc\nr\nF102\nFROST LINE\nsa\nx\n",
             "TC04 - create the refrigerated truck fleet"),
    "tc05": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\n"
             "a\nd002, Jamie Lee\n2\nsf\nc\nr\nF102\nFROST LINE\nsa\n"
             "a\nd101, Morgan Wong\n1\na\nd102, Taylor Lam\n2\nx\n",
             "TC05 - add drivers to the refrigerated fleet"),
    "tc06": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\nx\n", "TC06 - show the current refrigerated fleet"),
    "tc07": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nx\n", "TC07 - set the current fleet by id"),
    "tc08": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nx\n",
             "TC08 - display all fleets after switching"),
    "tc09": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nm\nd001\n2\nsf\nx\n",
             "TC09 - modify a driver role"),
    "tc10": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nm\nd001\n2\nsf\nd\nd002\nsf\nx\n",
             "TC10 - delete a driver"),
    "tc11": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nm\nd001\n2\nsf\nd\nd002\nsf\n"
             "cn\nMETRO EXPRESS\nsf\nx\n", "TC11 - change the name of the current fleet"),
    "tc12": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nm\nd001\n2\nsf\nd\nd002\nsf\n"
             "cn\nMETRO EXPRESS\nsf\nl\nx\n", "TC12 - show the undo and redo lists"),
    "tc13": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nm\nd001\n2\nsf\nd\nd002\nsf\n"
             "cn\nMETRO EXPRESS\nsf\nl\nu\nu\nu\nsf\nx\n", "TC13 - undo three commands"),
    "tc14": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nm\nd001\n2\nsf\nd\nd002\nsf\n"
             "cn\nMETRO EXPRESS\nsf\nl\nu\nu\nu\nsf\nr\nr\nr\nsf\nx\n",
             "TC14 - redo three commands"),
    "tc15": ("c\nv\nF001\nCENTRAL EXPRESS\na\nd001, Alex Chan\n1\na\nd002, Jamie Lee\n2\n"
             "sf\nc\nr\nF102\nFROST LINE\nsa\na\nd101, Morgan Wong\n1\n"
             "a\nd102, Taylor Lam\n2\nsf\ns\nF001\nsa\nm\nd001\n2\nsf\nd\nd002\nsf\n"
             "cn\nMETRO EXPRESS\nsf\nl\nu\nu\nu\nsf\nr\nr\nr\nsf\ns\nF999\nd\nd999\nq\nx\nx\n",
             "TC15 - error handling and exit"),
    "tc16": ("sf\na\nx\n", "TC16 - commands that need a current fleet"),
    "tc17": ("c\nv\nF001\nCENTRAL EXPRESS\nc\nv\nF001\nSECOND\nc\nq\nF900\nBAD\n"
             "c\nv\nF900\nNIGHT LINE\na\nd001, Alex Chan\n1\n"
             "a\nd001, Ben Wong\n1\nx\n", "TC17 - duplicate ids and invalid inputs"),
    "tc18": ("c\nv\nF001\nCENTRAL EXPRESS\nu\nu\nu\nr\nr\nl\nx\n",
             "TC18 - undo and redo with an empty or exhausted history"),
}


def main():
    figure_domain()
    figure_factory()
    figure_command()
    figure_memento()
    made = []
    for name, (stdin, title) in CASES.items():
        made.append((name, capture(name, stdin, title)))
    print("figures:", [p.name for p in OUT.glob("fig*.png")])
    for name, pages in made:
        print(name, [p.name for p in pages])


if __name__ == "__main__":
    main()
