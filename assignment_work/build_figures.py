"""Draw the class diagram and the three pattern diagrams."""

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = pathlib.Path(__file__).resolve().parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

EDGE = "#243b53"
TITLE_COL = "#102a43"
BODY_COL = "#334e68"
NOTE_COL = "#486581"

TITLE_SIZE = 9.4
BODY_SIZE = 7.5
NOTE_SIZE = 8.2
LINE = 1.30
HEADER = 2.7
STEREO_H = 1.55
MIN_H = 4.6
PAD_BOTTOM = 0.95


def uml(ax, x, top, w, title, stereo=None, attrs=(), ops=(), abstract=False):
    n = len(attrs) + len(ops)
    h = HEADER + STEREO_H * (1 if stereo else 0) + n * LINE
    if attrs and ops:
        h += 0.6
    h += PAD_BOTTOM
    h = max(h, MIN_H)
    bottom = top - h

    ax.add_patch(Rectangle((x, bottom), w, h, facecolor="white", edgecolor=EDGE,
                           linewidth=1.2, zorder=2))
    name_y = top - HEADER / 2 - 0.1
    if stereo:
        ax.text(x + w / 2, top - 1.0, stereo, ha="center", va="center",
                fontsize=6.6, style="italic", color=NOTE_COL, zorder=4)
        name_y = top - 2.25
    ax.text(x + w / 2, name_y, title, ha="center", va="center",
            fontsize=TITLE_SIZE, fontweight="bold", color=TITLE_COL,
            style="italic" if abstract else "normal", zorder=4)

    # divider below the name compartment
    ax.plot([x, x + w], [top - HEADER - STEREO_H * (1 if stereo else 0)] * 2,
            color=EDGE, linewidth=1.0, zorder=3)

    yy = top - HEADER - STEREO_H * (1 if stereo else 0) - 0.95
    for item in attrs:
        ax.text(x + 1.0, yy, item, ha="left", va="center", fontsize=BODY_SIZE,
                color=BODY_COL, zorder=4)
        yy -= LINE
    if attrs and ops:
        ax.plot([x + 0.8, x + w - 0.8], [yy + LINE / 2 + 0.12] * 2, color=EDGE,
                linewidth=0.6, zorder=3)
        yy -= 0.35
    for item in ops:
        ax.text(x + 1.0, yy, item, ha="left", va="center", fontsize=BODY_SIZE,
                color=BODY_COL, zorder=4)
        yy -= LINE
    return dict(x=x, top=top, w=w, h=h, bottom=bottom,
                left=(x, bottom + h / 2), right=(x + w, bottom + h / 2),
                mid=(x + w / 2, bottom + h / 2),
                topmid=(x + w / 2, top), bottommid=(x + w / 2, bottom))


def link(ax, p1, p2, head="inherit", label=None, dashed=False, rad=0.0,
         offset=(0, 0), size=NOTE_SIZE):
    style = {"inherit": "-|>", "arrow": "->", "none": "-"}[head]
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=11,
                                 linewidth=1.0, color=EDGE,
                                 linestyle="dashed" if dashed else "solid",
                                 connectionstyle="arc3,rad=%s" % rad,
                                 shrinkA=0, shrinkB=0, zorder=1))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + offset[0], (p1[1] + p2[1]) / 2 + offset[1],
                label, ha="center", va="center", fontsize=size, color=NOTE_COL,
                zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


def new_canvas(w_in, h_in):
    fig, ax = plt.subplots(figsize=(w_in, h_in))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h_in / w_in)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax, 100 * h_in / w_in


def figure_domain():
    fig, ax, TOP = new_canvas(15.5, 11.2)
    TOPY = TOP - 1.5

    driver = uml(ax, 1, TOPY, 21, "Driver",
                 attrs=["- driverID: String", "- driverName: String", "- role: int"],
                 ops=["+ getDriverID()", "+ getName()", "+ setRole(role)"])
    memento = uml(ax, 24.5, TOPY, 13, "Memento", stereo="«interface»")
    fname = uml(ax, 40, TOPY, 19, "FleetNameMemento",
                attrs=["- fleetID: String", "- fleetName: String"])
    drole = uml(ax, 61, TOPY, 19, "DriverRoleMemento",
                attrs=["- driverID: String", "- role: int"])

    vfleet = uml(ax, 1, 57, 30, "VehicleFleet", abstract=True,
                 attrs=["- fleetID: String", "- fleetName: String",
                        "- drivers: AbstractList"],
                 ops=["+ addDriver(d: Driver)", "+ dropDriver(d: Driver)",
                      "+ getFleetID()", "+ getName()", "+ setName(n)",
                      "+ findDriver(id): Driver",
                      "+ createFleetNameMemento()",
                      "+ createDriverRoleMemento(id)",
                      "+ updateDriverRole()  «abstract»",
                      "+ showFleet()  «abstract»"])

    repo = uml(ax, 34, 57, 24, "FleetRepository",
               attrs=["- fleets: Vector", "- currentFleet"],
               ops=["+ findFleet(id)", "+ addFleet(f)",
                    "+ removeFleet(f)", "+ getCurrentFleet()"])

    manager = uml(ax, 61, 57, 26, "CommandManager",
                  attrs=["- undoList: Vector", "- redoList: Vector"],
                  ops=["+ execute(c: Command)", "+ undo()", "+ redo()",
                       "+ showLists()"])

    command = uml(ax, 61, 41, 26, "Command", stereo="«interface»",
                  ops=["+ execute()", "+ undo()", "+ redo()",
                       "+ getDescription()", "+ isUndoable()"])

    abcmd = uml(ax, 61, 27, 26, "AbstractCommand", abstract=True,
                attrs=["- commandCode: String", "# context: CommandContext"],
                ops=["+ execute()  «abstract»", "+ undo()", "+ redo()"])

    cmds = uml(ax, 61, 16.2, 34, "Concrete commands (12)",
               attrs=["CreateFleetCommand / SetCurrentFleetCommand",
                      "AddDriverCommand / ModifyDriverRoleCommand",
                      "DeleteDriverCommand / ChangeFleetNameCommand",
                      "ShowFleetCommand / DisplayAllFleetsCommand",
                      "UndoCommand / RedoCommand",
                      "ShowUndoRedoListCommand / ExitCommand"])

    dvan = uml(ax, 1, 33, 20, "DeliveryVanFleet",
               ops=["+ showFleet()", "+ showFleetSummary()",
                    "+ getRoleName(role)", "+ getRolePrompt()"])
    dtruck = uml(ax, 22.5, 33, 25, "RefridgeratedTruckFleet",
                 ops=["+ showFleet()", "+ showFleetSummary()",
                      "+ getRoleName(role)", "+ getRolePrompt()"])

    link(ax, dvan["topmid"], (11, vfleet["bottom"]), "inherit")
    link(ax, dtruck["topmid"], (25, vfleet["bottom"]), "inherit")
    link(ax, manager["bottommid"], command["topmid"], "none", "uses", dashed=True)
    link(ax, abcmd["topmid"], command["bottommid"], "inherit")
    link(ax, cmds["topmid"], (76, abcmd["bottom"]), "inherit")

    link(ax, (11, vfleet["top"]), (11, driver["bottom"]), "arrow", "1..*",
         offset=(2.4, 0))
    link(ax, vfleet["right"], repo["left"], "arrow", "manages", offset=(0, 1.2))
    link(ax, fname["bottommid"], memento["right"], "inherit", dashed=True)
    link(ax, drole["bottommid"], memento["right"], "inherit", dashed=True)
    link(ax, (28, vfleet["top"]), (31, memento["bottom"]), "none", "creates",
         dashed=True, rad=0.15, offset=(4.4, 0))

    ax.text(24, 13.5,
            "The command objects are also the caretakers of the\n"
            "mementos; CommandManager keeps the two history lists.",
            ha="center", fontsize=NOTE_SIZE, color=NOTE_COL)

    fig.savefig(OUT / "fig1_domain.png", dpi=220, facecolor="white",
                bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def figure_factory():
    fig, ax, TOP = new_canvas(15.0, 8.6)
    TOPY = TOP - 1.5

    absf = uml(ax, 33, TOPY, 33, "SDFMSAbstractFactory", stereo="«interface»",
               ops=["+ createFleet(code, id): VehicleFleet",
                    "+ createDriver(id, name, role): Driver",
                    "+ createCommand(code): Command",
                    "+ isValidFleetType(code): boolean"])
    impl = uml(ax, 33, 42.0, 33, "SDFMSFactory",
               attrs=["- fleetFactories: FleetFactoryRegistry",
                      "- driverFactory: DriverFactory",
                      "- commandFactory: CommandFactory"])

    reg = uml(ax, 1, TOPY, 27, "FleetFactoryRegistry",
              attrs=["- factories: Map<String, FleetFactory>"],
              ops=["+ register(f: FleetFactory)", "+ getFactory(code)",
                   "+ isSupported(code)"])

    ff = uml(ax, 1, 40, 27, "FleetFactory", stereo="«interface»",
             ops=["+ getTypeCode(): String", "+ getTypeLabel(): String",
                  "+ createFleet(id): VehicleFleet"])
    vanf = uml(ax, 1, 28, 26, "DeliveryVanFleetFactory",
               ops=["+ createFleet(id): VehicleFleet"])
    refrig = uml(ax, 1, 17, 27, "RefridgeratedTruckFleetFactory",
                 ops=["+ createFleet(id): VehicleFleet"])

    cf = uml(ax, 71, TOPY, 26, "CommandFactory", stereo="«interface»",
             ops=["+ createCommand(code)"])
    scf = uml(ax, 71, 42.0, 26, "SDFMSCommandFactory",
              attrs=["- context: CommandContext"],
              ops=["+ createCommand(code)"])
    df = uml(ax, 71, 30, 26, "DriverFactory", stereo="«interface»",
             ops=["+ createDriver(id, name, role)"])
    dstd = uml(ax, 71, 19, 26, "StandardDriverFactory",
               ops=["+ createDriver(id, name, role)"])

    link(ax, impl["topmid"], absf["bottommid"], "inherit")
    link(ax, (33, 48.5), (28, 48.5), "arrow", "uses", offset=(0, 1.2))
    link(ax, reg["bottommid"], ff["topmid"], "arrow", "1..*", offset=(2.5, 0.7))
    link(ax, vanf["topmid"], (12, ff["bottom"]), "inherit")
    link(ax, refrig["topmid"], (17, ff["bottom"]), "inherit")
    link(ax, (66, 39.5), (71, 46.5), "arrow", "uses", offset=(0.6, 1.4))
    link(ax, scf["topmid"], cf["bottommid"], "inherit")
    link(ax, dstd["topmid"], df["bottommid"], "inherit")
    link(ax, (66, 34.5), (71, 27.5), "arrow", "uses", offset=(0.4, 1.5))

    fig.savefig(OUT / "fig2_factory.png", dpi=220, facecolor="white",
                bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def figure_command():
    fig, ax, TOP = new_canvas(14.5, 7.4)

    def node(x, top, w, title, sub, colour):
        h = 11.0
        ax.add_patch(FancyBboxPatch((x, top - h), w, h, boxstyle="round,pad=0.5",
                                    facecolor=colour, edgecolor=EDGE,
                                    linewidth=1.1, zorder=2))
        ax.text(x + w / 2, top - 4.0, title, ha="center", va="center",
                fontsize=9.6, fontweight="bold", color=TITLE_COL, zorder=3)
        ax.text(x + w / 2, top - 8.2, sub, ha="center", va="center",
                fontsize=7.8, color=BODY_COL, zorder=3)
        return dict(x=x, top=top, w=w, bottom=top - h,
                    left=(x, top - h / 2), right=(x + w, top - h / 2),
                    mid=(x + w / 2, top - h / 2), topmid=(x + w / 2, top),
                    bottommid=(x + w / 2, top - h))

    client = node(2, 38, 21, "Client", "SDFMSApplication", "#e8f1fb")
    invoker = node(29, 38, 29, "Invoker", "CommandManager\n(undo / redo lists)",
                   "#fff4e0")
    receiver = node(2, 13, 21, "Receiver", "VehicleFleet, Driver,\nFleetRepository",
                    "#eaf6ec")
    command = node(29, 13, 29, "Command «interface»", "Command / AbstractCommand",
                   "#f3e8fb")
    concrete = node(63, 13, 33, "ConcreteCommand", "12 command classes",
                    "#f3e8fb")

    link(ax, client["right"], invoker["left"], "arrow", "1. create",
         offset=(0.5, 1.4))
    link(ax, invoker["bottommid"], command["topmid"], "arrow", "2. execute()",
         offset=(2.4, 0))
    link(ax, command["left"], receiver["right"], "arrow", "3. action()",
         offset=(0, 1.4))
    link(ax, concrete["left"], command["right"], "inherit", "4. implements",
         offset=(0, -2.0))
    link(ax, (33, invoker["bottom"]), (12, receiver["top"]), "arrow",
         "5. undo / redo", dashed=True, rad=-0.2, offset=(-4.0, 0.5))

    ax.text(50, 47.0,
            "Every user function is an object, so the invoker can execute, undo, redo and",
            ha="center", fontsize=NOTE_SIZE, color=NOTE_COL)
    ax.text(50, 43.8,
            "list the commands without knowing what they actually do.",
            ha="center", fontsize=NOTE_SIZE, color=NOTE_COL)

    fig.savefig(OUT / "fig3_command.png", dpi=220, facecolor="white",
                bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def figure_memento():
    fig, ax, TOP = new_canvas(14.5, 7.8)
    TOPY = TOP - 1.0

    lanes = [(17, "Caretaker\nChangeFleetNameCommand"),
             (50, "Originator\nVehicleFleet"),
             (84, "Memento\nFleetNameMemento")]

    for x, label in lanes:
        ax.add_patch(FancyBboxPatch((x - 13, TOPY - 6.5), 26, 6.5,
                                    boxstyle="round,pad=0.35",
                                    facecolor="#e8f1fb", edgecolor=EDGE,
                                    linewidth=1.0, zorder=2))
        ax.text(x, TOPY - 3.25, label, ha="center", va="center", fontsize=8.4,
                color=TITLE_COL, zorder=3)
        ax.plot([x, x], [9, TOPY - 6.5], linestyle="--", color="#8fa3b8",
                linewidth=0.9)

    def step(y, x1, x2, text):
        link(ax, (x1, y), (x2, y), "arrow")
        ax.text((x1 + x2) / 2, y + 1.6, text, ha="center", va="center",
                fontsize=7.8, color=BODY_COL,
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))

    step(32, 17, 50, "1. createFleetNameMemento()")
    step(27.5, 50, 84, "2. new FleetNameMemento(id, name)")
    step(23, 84, 50, "3. memento object")
    step(18.5, 50, 17, "4. keep it in the command")
    step(14, 17, 50, "5. undo(): restoreFleetName(memento)")
    step(10.5, 50, 84, "6. read the saved name")

    ax.text(50, 4.6,
            "The command never touches the internal fields of the fleet: the memento is "
            "opaque and only VehicleFleet can read it.",
            ha="center", fontsize=7.8, color=NOTE_COL)

    fig.savefig(OUT / "fig4_memento.png", dpi=220, facecolor="white",
                bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


if __name__ == "__main__":
    figure_domain()
    figure_factory()
    figure_command()
    figure_memento()
    print("done")
