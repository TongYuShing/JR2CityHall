"""Build the SDFMS assignment report."""

import pathlib

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BASE = pathlib.Path(__file__).resolve().parent
ASSETS = BASE / "assets"
SRC = BASE / "src"
OUT = BASE.parent / "ITP4507_Assignment_Report.docx"

WEST = "Times New Roman"
EAST = "宋体"
HEI = "黑体"
MONO = "Consolas"

_counter = {"table": 0, "figure": 0}


# ----------------------------------------------------------------------
# low level helpers
# ----------------------------------------------------------------------
def set_font(run, size=None, west=WEST, east=EAST, bold=None, italic=None,
             color=(0, 0, 0)):
    run.font.name = west
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = RGBColor(*color)
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.append(fonts)
    fonts.set(qn("w:ascii"), west)
    fonts.set(qn("w:hAnsi"), west)
    fonts.set(qn("w:eastAsia"), east)
    fonts.set(qn("w:cs"), west)


def style_base(doc, name, west, east, size, bold=False, space_before=0,
               space_after=0, spacing=1.5, align=None, indent_chars=0,
               keep_next=False, color=(0, 0, 0)):
    try:
        st = doc.styles[name]
    except KeyError:
        from docx.enum.style import WD_STYLE_TYPE
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = doc.styles["Normal"]
    st.font.name = west
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.color.rgb = RGBColor(*color)
    rpr = st.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.append(fonts)
    fonts.set(qn("w:ascii"), west)
    fonts.set(qn("w:hAnsi"), west)
    fonts.set(qn("w:eastAsia"), east)
    pf = st.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = spacing
    if align is not None:
        pf.alignment = align
    if indent_chars:
        pf.first_line_indent = Pt(size * indent_chars)
    pf.keep_with_next = keep_next
    return st


def body(doc, text, indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10.5,
         bold_lead=None, space_after=0):
    par = doc.add_paragraph(style="Normal")
    par.paragraph_format.alignment = align
    if not indent:
        par.paragraph_format.first_line_indent = Pt(0)
    par.paragraph_format.space_after = Pt(space_after)
    if bold_lead:
        run = par.add_run(bold_lead)
        set_font(run, size, bold=True)
    run = par.add_run(text)
    set_font(run, size)
    return par


def heading(doc, text, level, page_break=False):
    par = doc.add_paragraph(style="Heading %d" % level)
    run = par.add_run(text)
    set_font(run, {1: 16, 2: 14, 3: 12}[level], west=WEST, east=HEI, bold=True)
    if page_break:
        par.paragraph_format.page_break_before = True
    return par


def caption(doc, kind, text, before=True):
    _counter[kind] += 1
    label = "Table %d " % _counter["table"] if kind == "table" else "Figure %d " % _counter["figure"]
    par = doc.add_paragraph(style="Caption")
    if before:
        par.paragraph_format.space_after = Pt(4)
    run = par.add_run(label + text)
    set_font(run, 9, west=WEST, east=HEI, bold=True)
    return par


def add_field(par, code, placeholder="1"):
    run = par.add_run()
    set_font(run, 10.5)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " %s " % code
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instr, sep, text, end):
        run._r.append(node)


def picture(doc, path, text, width_cm):
    par = doc.add_paragraph()
    par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.first_line_indent = Pt(0)
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.space_after = Pt(2)
    par.paragraph_format.keep_with_next = True
    par.add_run().add_picture(str(path), width=Cm(width_cm))
    caption(doc, "figure", text, before=False)


def cell_shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def table(doc, rows, cap, widths, aligns=None, size=9, header=True):
    caption(doc, "table", cap)
    ncols = len(rows[0])
    tbl = doc.add_table(rows=len(rows), cols=ncols)
    tbl.alignment = 1
    tbl.autofit = False
    tblpr = tbl._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblpr.append(layout)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "404040")
        borders.append(el)
    tblpr.append(borders)

    for i, row in enumerate(rows):
        tr = tbl.rows[i]
        trpr = tr._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        trpr.append(cant)
        if i == 0 and header:
            head = OxmlElement("w:tblHeader")
            trpr.append(head)
        for j, value in enumerate(row):
            cell = tr.cells[j]
            cell.width = Cm(widths[j])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            par = cell.paragraphs[0]
            par.style = doc.styles["Normal"]
            pf = par.paragraph_format
            pf.first_line_indent = Pt(0)
            pf.left_indent = Pt(0)
            pf.right_indent = Pt(0)
            pf.line_spacing = 1.0
            pf.space_before = Pt(1.5)
            pf.space_after = Pt(1.5)
            if i == 0:
                pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cell_shade(cell, "D9D9D9")
            else:
                al = (aligns[j] if aligns else (WD_ALIGN_PARAGRAPH.CENTER if j == 0
                                                 else WD_ALIGN_PARAGRAPH.LEFT))
                pf.alignment = al
            run = par.add_run(str(value))
            set_font(run, size, bold=(i == 0))
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(2)
    par.paragraph_format.first_line_indent = Pt(0)
    return tbl


def code(doc, text, size=8.0):
    par = doc.add_paragraph(style="CodeBlock")
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i:
            par.add_run().add_break(WD_BREAK.LINE)
        run = par.add_run(line if line else " ")
        set_font(run, size, west=MONO, east=EAST)
    return par


def code_file(doc, name, size=7.8):
    par = doc.add_paragraph(style="Normal")
    par.paragraph_format.first_line_indent = Pt(0)
    par.paragraph_format.space_before = Pt(8)
    par.paragraph_format.space_after = Pt(2)
    par.paragraph_format.keep_with_next = True
    run = par.add_run(name)
    set_font(run, 9.5, west=MONO, east=HEI, bold=True)
    code(doc, (SRC / name).read_text(encoding="utf-8").rstrip("\n"), size=size)


def case_block(doc, cid, title, objective, precondition, steps, expected, shots):
    par = doc.add_paragraph(style="Normal")
    par.paragraph_format.first_line_indent = Pt(0)
    par.paragraph_format.space_before = Pt(10)
    par.paragraph_format.space_after = Pt(3)
    par.paragraph_format.keep_with_next = True
    run = par.add_run("%s  %s" % (cid, title))
    set_font(run, 10.5, west=WEST, east=HEI, bold=True)

    rows = [["Item", "Content"],
            ["Objective", objective],
            ["Pre-condition", precondition],
            ["Test steps", steps],
            ["Expected result", expected]]
    table(doc, rows, "", [2.6, 13.1], size=9)
    for shot, shot_cap in shots:
        picture(doc, shot, shot_cap, 13.2)


# ----------------------------------------------------------------------
# document skeleton
# ----------------------------------------------------------------------
doc = Document()

style_base(doc, "Normal", WEST, EAST, 10.5, spacing=1.5,
           align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent_chars=2)
style_base(doc, "Heading 1", WEST, HEI, 16, bold=True, space_before=14,
           space_after=6, spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT,
           keep_next=True)
style_base(doc, "Heading 2", WEST, HEI, 14, bold=True, space_before=11,
           space_after=5, spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT,
           keep_next=True)
style_base(doc, "Heading 3", WEST, HEI, 12, bold=True, space_before=9,
           space_after=4, spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT,
           keep_next=True)
style_base(doc, "Title", WEST, HEI, 18, bold=True, space_before=0,
           space_after=18, spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
style_base(doc, "Caption", WEST, HEI, 9, bold=True, space_before=4,
           space_after=6, spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
style_base(doc, "CodeBlock", MONO, EAST, 8, spacing=1.0,
           align=WD_ALIGN_PARAGRAPH.LEFT)

sect = doc.sections[0]
sect.page_width = Cm(21)
sect.page_height = Cm(29.7)
for side in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sect, side, Cm(2.5))


def toc_line(text, size=10.5, bold=False, space_before=0, space_after=0):
    par = doc.add_paragraph(style="Normal")
    pf = par.paragraph_format
    pf.first_line_indent = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.5
    run = par.add_run(text)
    set_font(run, size, west=WEST, east=HEI if bold else EAST, bold=bold)
    return par


# ----------------------------------------------------------------------
# cover page
# ----------------------------------------------------------------------
toc_line("HONG KONG INSTITUTE OF INFORMATION TECHNOLOGY", 12, True, 36)
toc_line("Higher Diploma in Software Engineering (IT114105)", 11, False, 6)
toc_line("Contemporary Topics in Software Engineering (ITP4507)", 11, False, 2)
toc_line("Assignment One", 11, False, 2, 48)

par = doc.add_paragraph(style="Title")
run = par.add_run("Design and Implementation of the Smart Delivery\u00a0Fleet Management System")
set_font(run, 18, west=WEST, east=HEI, bold=True)

sub = doc.add_paragraph(style="Normal")
sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.paragraph_format.first_line_indent = Pt(0)
sub.paragraph_format.space_after = Pt(40)
run = sub.add_run("A Short Report on the Application of the Command, Factory and Memento "
                  "Design Patterns")
set_font(run, 11, italic=True)

info = [
    ["Programme", "Higher Diploma in Software Engineering (IT114105)"],
    ["Module", "Contemporary Topics in Software Engineering (ITP4507)"],
    ["Assignment", "Assignment One (66.67% of the end-of-module assessment)"],
    ["Student Number", "<Student Number>"],
    ["Student Name", "<Student Name>"],
]
table(doc, info, "", [4.4, 11.3],
      aligns=[WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
toc_line("6 November 2026", 10.5, False, 30)

# cover keeps no page number -------------------------------------------
cover_footer = sect.footer
cover_footer.is_linked_to_previous = False

sect2 = doc.add_section(WD_SECTION.NEW_PAGE)
sect2.page_width = Cm(21)
sect2.page_height = Cm(29.7)
for side in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sect2, side, Cm(2.5))
sect2.footer.is_linked_to_previous = False

# ----------------------------------------------------------------------
# table of contents
# ----------------------------------------------------------------------
par = doc.add_paragraph(style="Normal")
par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
par.paragraph_format.first_line_indent = Pt(0)
par.paragraph_format.space_after = Pt(12)
run = par.add_run("Table of Contents")
set_font(run, 16, west=WEST, east=HEI, bold=True)

par = doc.add_paragraph(style="Normal")
par.paragraph_format.first_line_indent = Pt(0)
par.paragraph_format.line_spacing = 1.0
add_field(par, 'TOC \\o "1-2" \\h \\z \\u',
          "Right-click and choose Update Field to build the table of contents.")

sect3 = doc.add_section(WD_SECTION.NEW_PAGE)
sect3.page_width = Cm(21)
sect3.page_height = Cm(29.7)
for side in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sect3, side, Cm(2.5))
sect3.footer.is_linked_to_previous = False
footer_par = sect3.footer.paragraphs[0]
footer_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer_par.paragraph_format.first_line_indent = Pt(0)
add_field(footer_par, "PAGE", "1")
pg = OxmlElement("w:pgNumType")
pg.set(qn("w:start"), "1")
sect3._sectPr.append(pg)

# ----------------------------------------------------------------------
# 1 introduction
# ----------------------------------------------------------------------
heading(doc, "1 Introduction", 1)
body(doc,
     "The Smart Delivery Logistics Company coordinates delivery work for commercial "
     "customers. Its drivers are organised into vehicle fleets, and the fleet itself, not "
     "the individual driver, decides which roles a driver may take: a delivery van fleet "
     "distinguishes van drivers from courier drivers, while a refrigerated truck fleet "
     "distinguishes refrigerated-truck drivers from cold-chain delivery drivers. The "
     "company now operates two kinds of fleet but expects to add motorcycle-delivery fleets "
     "and electric-cargo-bike fleets in the near future, so the software must be able to "
     "absorb a new fleet type without being redesigned.")
body(doc,
     "The Smart Delivery Fleet Management System (SDFMS) developed for this assignment is a "
     "console application that maintains fleets and their drivers in memory. It offers twelve "
     "functions: create a fleet, set the current fleet, add a driver, modify a driver role, "
     "delete a driver, show the current fleet, display all fleets, change the fleet name, "
     "undo, redo, list the undo and redo lists, and exit the system. Five of these functions "
     "modify data and therefore have to be reversible, and the assignment requires the "
     "reversal of two of them, the driver role and the fleet name, to be implemented with the "
     "Memento pattern. The remaining structural requirements are the Command pattern for "
     "every user function and a factory family for fleets, drivers and commands.")
body(doc,
     "This report explains how the system was designed and why. Section 2 records the "
     "assumptions made about the problem context. Section 3 presents the application design "
     "and the class diagram. Section 4 discusses each design pattern, the roles it plays in "
     "SDFMS and the alternatives that were rejected. Section 5 sets out the test plan, the "
     "eighteen test cases and the captured test results. Section 6 is a short user guide, "
     "Section 7 concludes, and the appendix contains the fully commented source code.")

# ----------------------------------------------------------------------
# 2 assumptions
# ----------------------------------------------------------------------
heading(doc, "2 Assumptions about the Problem Context", 1, page_break=True)
body(doc,
     "The task specification fixes the twelve functions and the three patterns but leaves "
     "many details of the business context open. The following assumptions were made before "
     "the design was drawn up. Each assumption is a deliberate decision that keeps the "
     "implementation small while remaining consistent with the sample run supplied with the "
     "assignment.")
table(doc,
      [["Ref.", "Assumption", "Consequence in the implementation"],
       ["A1", "SDFMS is a single-user console program. Fleets, drivers and history exist only "
              "in main memory for the lifetime of one run; nothing is written to a file or a "
              "database.",
        "The repository is an ordinary object; no persistence layer, transaction handling or "
        "file format is required."],
       ["A2", "A fleet identifier is chosen by the user and must be unique in the system. "
              "Identifiers and names are compared case sensitively and are not trimmed beyond "
              "leading and trailing blanks.",
        "Create-fleet validates the identifier against the repository and rejects a duplicate; "
        "the identifier is the key used by set-current-fleet."],
       ["A3", "A fleet name is free text that must not be empty. Two fleets may share a name "
              "because the identifier, not the name, identifies a fleet.",
        "Only an empty name is rejected. Names appear in the fleet header and can be changed at "
        "any time through the change-fleet-name command."],
       ["A4", "A driver identifier is unique within one fleet, but the same identifier may "
              "appear in a different fleet. A driver record belongs to exactly one fleet.",
        "Add-driver checks the current fleet only. Delete and modify operate on the current "
        "fleet and report a driver that is not there."],
       ["A5", "Driver information is entered as one line of the form 'id, name'. The first "
              "comma separates the two fields, so a name may contain commas, blanks and any "
              "other printable character.",
        "The reader splits the line at the first comma only and rejects a line without a comma "
        "or with an empty field."],
       ["A6", "Role codes are local to a fleet type and are numbered from one in the order the "
              "fleet type defines. A valid code for a delivery van fleet is 1 (van driver) or "
              "2 (courier driver); for a refrigerated truck fleet 1 (refrigerated-truck driver) "
              "or 2 (cold-chain delivery driver).",
        "The role prompt and the role names come from the fleet object, not from a constant "
        "table, so a new fleet type defines its own roles."],
       ["A7", "The user interface is line oriented: one command code, one input value or one "
              "driver record per line. A blank line carries no meaning and is ignored.",
        "The main loop reads and discards blank lines instead of reporting them as invalid "
        "commands, which keeps the output compatible with the sample run."],
       ["A8", "Creating a fleet makes it the current fleet, because the sample run prints "
              "'Current fleet is changed to F001.' immediately after the creation message.",
        "The create command selects the new fleet as a side effect of executing; its undo "
        "removes the fleet and clears the current fleet."],
       ["A9", "The undo and redo lists belong to the whole session rather than to a fleet. "
              "Commands that only read or navigate - set current fleet, show fleet, display "
              "all fleets, list the histories, exit - are not recorded.",
        "Those commands report themselves as not undoable, so the history only contains the "
        "commands that change data, exactly as the nine entries of sample case 12 show."],
       ["A10", "Executing a new undoable command discards the redo list, which is the "
               "conventional behaviour of an undo stack.",
        "The command manager clears the redo list after a successful execution, so an old "
        "redo branch can never be replayed onto a different state."]],
      "Assumptions about the problem context and their effect on the design",
      [1.3, 7.3, 7.1],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY,
              WD_ALIGN_PARAGRAPH.JUSTIFY])

body(doc,
     "Two further constraints come directly from the specification and are treated as "
     "assumptions throughout the design. First, the classes VehicleFleet, DeliveryVanFleet, "
     "RefridgeratedTruckFleet and Driver supplied with the assignment may be extended but "
     "their existing attributes and operations must not be removed or modified; the design "
     "therefore adds behaviour instead of rewriting it. Second, the fleet identifier and the "
     "driver identifier are the only keys the user is expected to remember, so every "
     "operation that needs a fleet or a driver asks for an identifier and reports a missing "
     "one rather than aborting the program.")

# ----------------------------------------------------------------------
# 3 application design
# ----------------------------------------------------------------------
heading(doc, "3 Application Design", 1, page_break=True)
heading(doc, "3.1 Overall Architecture", 2)
body(doc,
     "The program is a single Java application that the supplied run.bat compiles with "
     "'javac *.java'. All classes therefore live in the default package and are stored in one "
     "source directory. Within that directory the code is organised into five collaborating "
     "layers, shown in Table 2. Each layer depends only on the layers below it, which keeps "
     "the console front end replaceable and the domain model free of user-interface detail.")
table(doc,
      [["Layer", "Main classes", "Responsibility"],
       ["Presentation", "SDFMSApplication, ConsoleInput",
        "Prints the menu and the current fleet, reads one input line at a time, parses role "
        "codes and driver records, and dispatches the command code to the factory."],
       ["Invocation", "CommandManager, CommandContext",
        "Executes command objects, keeps the undo and redo lists, and provides the shared "
        "context through which a command reaches the repository, the reader and the factories."],
       ["Application", "Command, AbstractCommand and the twelve command classes",
        "One class per user function. Each class validates its own input, performs the "
        "change, and knows how to reverse it."],
       ["Factory", "SDFMSAbstractFactory, SDFMSFactory, FleetFactoryRegistry, FleetFactory "
                   "and its two implementations, DriverFactory, CommandFactory",
        "Creates fleets, drivers and commands from a code typed by the user, so that no client "
        "class needs to name a concrete product class."],
       ["Domain", "VehicleFleet, DeliveryVanFleet, RefridgeratedTruckFleet, Driver, "
                  "FleetRepository, Memento and the two memento classes",
        "Holds the business data and the rules of a fleet type, and captures and restores "
        "snapshots for the undo mechanism."]],
      "Layers of the SDFMS implementation",
      [2.6, 6.2, 6.9],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.JUSTIFY])

heading(doc, "3.2 The Domain Layer", 2)
body(doc,
     "VehicleFleet keeps the two attributes and the driver collection of the supplied "
     "skeleton and remains abstract. The collection is a Vector, which is one of the two "
     "concrete implementations of AbstractList that the specification allows, and the "
     "declared type remains AbstractList so that the skeleton signature is untouched. Three "
     "operations were added to the class. getDriverList() casts the raw list once, in one "
     "place, and returns a typed List<Driver>; findDriver() and hasDriver() answer the "
     "questions that the commands ask most often - does this fleet already contain a driver, "
     "and which driver object has this identifier.")
body(doc,
     "The class also declares four new abstract operations: getFleetTypeDisplayName(), "
     "getRoleName(int), getRolePrompt() and showFleetSummary(). These operations express what "
     "differs between fleet types: the text in front of a fleet line, the vocabulary of roles, "
     "the prompt that offers the roles, and the single-line form used by 'display all fleets'. "
     "The concrete subclasses DeliveryVanFleet and RefridgeratedTruckFleet implement them "
     "together with the two abstract operations of the skeleton, updateDriverRole() and "
     "showFleet(). Both subclasses print the drivers of each role through one private helper "
     "that prints 'NIL' on the heading line when a role has no driver, which reproduces the "
     "sample output where an empty role appears as 'Van Driver: NIL'.")
body(doc,
     "FleetRepository is a small aggregate that owns the fleets and the current fleet. It "
     "offers findFleet(), containsFleet(), addFleet(), removeFleet() and getCurrentFleet(). "
     "Keeping the current fleet in the repository rather than in a command or in the "
     "application object means that a command can change the selection without the front end "
     "knowing about it, and the menu that is printed before the next prompt can always read "
     "the selection from one place.")
body(doc,
     "The Memento pattern adds the marker interface Memento and two small snapshot classes. "
     "FleetNameMemento stores the fleet identifier and the fleet name; DriverRoleMemento "
     "stores the driver identifier and the role code. Neither class exposes a setter, so the "
     "snapshot can only be read. VehicleFleet is the originator: createFleetNameMemento(), "
     "createDriverRoleMemento(), restoreFleetName() and restoreDriverRole() are its operations, "
     "and the restore operations check that the snapshot belongs to the same fleet or driver "
     "before changing anything.")

heading(doc, "3.3 The Command Layer", 2)
body(doc,
     "The interface Command declares execute(), undo(), redo(), getDescription() and "
     "isUndoable(). The description is the line that the history listing prints, so each "
     "command builds it from its own data - for example 'Change fleet name, F001, METRO "
     "EXPRESS'. AbstractCommand implements the parts that every command shares: it stores the "
     "command code and the CommandContext, leaves execute() and getDescription() abstract, "
     "provides an empty undo() for commands that need no reversal, and implements redo() as a "
     "second execution of the same change.")
body(doc,
     "CommandManager is the invoker. Its execute() runs the command and, when the command "
     "reports itself as undoable, pushes it onto the undo list and clears the redo list. Its "
     "undo() pops the most recent entry, asks it to reverse itself, moves it to the redo list "
     "and prints the confirmation message; redo() performs the symmetric operation. Both "
     "operations print a short message and return when the corresponding list is empty, so the "
     "user is never left without feedback. showLists() prints the two lists in the order "
     "required by the sample output, oldest entry first, each terminated by the end marker.")
body(doc,
     "CommandContext is the service object that every command receives in its constructor. It "
     "holds the repository, the ConsoleInput reader, the command manager, the abstract factory "
     "and the running flag, and it offers getCurrentFleetOrReport(), which prints 'No current "
     "fleet is set!' and returns null when no fleet has been selected. Passing the context "
     "explicitly rather than using static fields keeps the commands testable and makes the "
     "dependencies of a command visible in its constructor.")
body(doc,
     "The twelve command classes are listed in Table 3. Five of them change data and are "
     "undoable; the navigation, reading and history commands are not. The undo mechanisms "
     "differ because the changes differ: a created fleet is removed again, a deleted driver is "
     "put back into the fleet it came from, an added driver is removed, and the two remaining "
     "changes are reversed from a memento.")
table(doc,
      [["Code", "Command class", "Change", "Undoable", "How undo is performed"],
       ["c", "CreateFleetCommand", "Adds a fleet to the repository and selects it", "Yes",
        "Removes the created fleet and clears the selection"],
       ["s", "SetCurrentFleetCommand", "Changes the current fleet", "No", "Not recorded"],
       ["a", "AddDriverCommand", "Adds a driver to the current fleet", "Yes",
        "Removes the driver object that was added"],
       ["m", "ModifyDriverRoleCommand", "Changes the role of a driver", "Yes",
        "Restores the role from DriverRoleMemento"],
       ["d", "DeleteDriverCommand", "Removes a driver from the current fleet", "Yes",
        "Inserts the saved driver object back into the fleet"],
       ["sf", "ShowFleetCommand", "Prints the current fleet", "No", "Not recorded"],
       ["sa", "DisplayAllFleetsCommand", "Prints one line per fleet", "No", "Not recorded"],
       ["cn", "ChangeFleetNameCommand", "Renames the current fleet", "Yes",
        "Restores the name from FleetNameMemento"],
       ["u", "UndoCommand", "Reverses the most recent undoable command", "No",
        "Delegates to the command manager"],
       ["r", "RedoCommand", "Re-applies the most recently undone command", "No",
        "Delegates to the command manager"],
       ["l", "ShowUndoRedoListCommand", "Prints both history lists", "No", "Not recorded"],
       ["x", "ExitCommand", "Prints the closing message and stops the loop", "No",
        "Clears the running flag"]],
      "The twelve command classes and their undo behaviour",
      [1.2, 3.9, 4.8, 1.7, 3.9],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER,
              WD_ALIGN_PARAGRAPH.LEFT])

heading(doc, "3.4 The Factory Layer", 2)
body(doc,
     "Three product families have to be created from a code typed by the user, and each "
     "family has more than one member or is expected to grow. A single abstract factory, "
     "SDFMSAbstractFactory, declares the four operations the rest of the program needs: "
     "createFleet(typeCode, fleetID), createDriver(id, name, role), createCommand(code) and "
     "the two queries isValidFleetType(code) and getFleetTypeLabel(code). SDFMSFactory is the "
     "only implementation; it does not create objects itself but delegates to three smaller "
     "factories that it owns, and is therefore also the composition root of the object graph.")
body(doc,
     "FleetFactory is the per-type factory. Each implementation publishes a type code ('v' or "
     "'r'), a label used in messages ('delivery van fleet', 'refrigerated truck fleet') and a "
     "createFleet() operation. FleetFactoryRegistry keeps the implementations in a "
     "LinkedHashMap keyed by type code, so the order of the two fleets in the message and in "
     "the listing is stable, and a new fleet type is registered by one call without editing "
     "any other class. DriverFactory and its implementation StandardDriverFactory isolate the "
     "creation of Driver objects, and CommandFactory and SDFMSCommandFactory map a command "
     "code to one of the twelve command classes. A code that names no command returns null, "
     "which is how the front end detects an invalid command.")

heading(doc, "3.5 The Presentation Layer", 2)
body(doc,
     "ConsoleInput wraps a single Scanner and does three things. readLine(prompt) prints the "
     "prompt, reads one line, trims it and returns null at end of input; readRole(prompt) "
     "reads a role code and returns -1 when the text is not a number; readDriverInformation() "
     "reads a driver record and splits it at the first comma. Because every prompt is printed "
     "by the same method, the prompts in the output cannot drift from the prompts the "
     "commands expect.")
body(doc,
     "SDFMSApplication holds the three menu lines and the command prompt as named constants "
     "and runs the read-execute loop. Before each prompt it prints the menu and, when a fleet "
     "is current, one extra line 'The current fleet is F001 CENTRAL EXPRESS.' The loop "
     "ignores blank lines, asks the factory for the command object, prints 'Invalid command!' "
     "when the factory returns null, and otherwise lets the command manager execute it. The "
     "loop stops when the exit command clears the running flag or when input ends, so a run "
     "driven by a script always terminates. Main only assembles the objects - repository, "
     "reader, context, manager and factory - and starts the loop, which keeps the wiring in "
     "one visible place.")

heading(doc, "3.6 Class Diagram", 2)
body(doc,
     "Figure 1 shows the complete class model. The upper part contains the domain classes "
     "Driver, VehicleFleet with its two subclasses, FleetRepository, and the three memento "
     "types. The right part contains the command hierarchy: the Command interface, "
     "AbstractCommand, the twelve concrete commands, and CommandManager which holds the two "
     "history lists. Associations are drawn only where an object keeps a reference to another "
     "object: a fleet manages its drivers, the repository manages the fleets, the manager "
     "uses commands, and the two commands that need a snapshot create a memento and keep it "
     "for the lifetime of the command.")
picture(doc, ASSETS / "fig1_domain.png",
        "Class diagram of the SDFMS application", 15.4)
body(doc,
     "Three details of the diagram deserve comment. First, the inheritance arrows from "
     "DeliveryVanFleet and RefridgeratedTruckFleet to VehicleFleet carry the whole "
     "type-specific vocabulary of roles and headings, so no command class knows which fleet "
     "type it is working with. Second, the two memento classes depend on the marker interface "
     "Memento and on nothing else; the command that holds a memento never reads its fields, "
     "which is what keeps the snapshot opaque. Third, the command hierarchy is independent of "
     "the domain hierarchy: the only link between the two halves is the receiver, which a "
     "command reaches through the CommandContext.")

heading(doc, "3.7 Conformance with the Open-Closed Principle", 2)
body(doc,
     "The Open-Closed Principle requires that a module be open for extension but closed for "
     "modification. SDFMS respects it in three places. New fleet types extend VehicleFleet and "
     "implement FleetFactory; nothing in VehicleFleet, in the command classes, in the "
     "repository or in the front end refers to a concrete fleet class. New drivers extend "
     "Driver and implement DriverFactory. New commands add one class, one entry in "
     "SDFMSCommandFactory and one menu letter; the manager, the context and the application "
     "object are untouched because they only know the Command interface.")
body(doc,
     "Table 4 lists the complete set of edits needed to support a motorcycle-delivery fleet "
     "and an electric-cargo-bike fleet. Every edit is an addition; no existing method body has "
     "to change, and the supplied skeleton classes keep their original attributes and "
     "operations.")
table(doc,
      [["Step", "Work for one new fleet type", "Files touched"],
       ["1", "Add a subclass of VehicleFleet that implements the two abstract operations and "
             "the four type-specific operations (display name, two role names, role prompt, "
             "summary line).", "One new class"],
       ["2", "Add a FleetFactory implementation that publishes the type code and the label.",
        "One new class"],
       ["3", "Register the new factory in FleetFactoryRegistry.createDefault() and extend the "
             "type prompt printed by CreateFleetCommand.", "Two existing classes, one line each"],
       ["4", "Extend the fleet type prompt text in the user guide and add test cases.",
        "Documentation and tests only"]],
      "Effort required to add a fleet type",
      [1.4, 11.5, 2.8],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY,
              WD_ALIGN_PARAGRAPH.LEFT])

# ----------------------------------------------------------------------
# 4 design patterns
# ----------------------------------------------------------------------
heading(doc, "4 Discussion of the Design Patterns", 1, page_break=True)
heading(doc, "4.1 The Command Pattern", 2)
body(doc,
     "The Command pattern turns a request into a stand-alone object. Its intent, as stated by "
     "Gamma et al., is to encapsulate a request as an object, thereby letting it be "
     "parameterised, queued, logged and undone. SDFMS needs all four of those properties: the "
     "front end must treat twelve very different functions uniformly, the manager must record "
     "them in a history, the history must be replayed in both directions, and the history "
     "listing must describe each entry. A design in which the front end called a method of the "
     "domain layer for each command would need a switch on the command code, a second switch "
     "in the undo routine and a third table for the descriptions, and every new function would "
     "touch all three.")
body(doc,
     "In SDFMS the client is SDFMSApplication, the invoker is CommandManager, the receiver is "
     "the fleet, the driver or the repository, and the command objects are the twelve classes "
     "of Table 3. Table 5 records the mapping. Figure 2 shows how the participants "
     "collaborate, including the path that a request takes from the command code to the "
     "domain object and the reverse path used by undo.")
table(doc,
      [["Participant", "Class in SDFMS", "Role in the collaboration"],
       ["Client", "SDFMSApplication",
        "Reads the command code, obtains the command object from the factory and passes it to "
        "the invoker; it never calls a domain operation directly."],
       ["Invoker", "CommandManager",
        "Executes the command, keeps the undo and redo lists and decides which commands enter "
        "the history."],
       ["Receiver", "VehicleFleet, Driver, FleetRepository",
        "Owns the data that a command changes; the command calls its operations instead of "
        "manipulating fields."],
       ["Command", "Command, AbstractCommand",
        "Declares execute(), undo(), redo(), getDescription() and isUndoable(), and supplies "
        "the default behaviour shared by all commands."],
       ["ConcreteCommand", "CreateFleetCommand and the other eleven classes",
        "Validates its own input, performs one change, records everything needed to reverse "
        "it and describes itself for the history listing."]],
      "Participants of the Command pattern in SDFMS",
      [2.6, 5.4, 7.7],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.JUSTIFY])
picture(doc, ASSETS / "fig3_command.png",
        "Collaboration of the Command pattern in SDFMS", 14.6)
body(doc,
     "Undo is implemented inside the command, not inside the manager, because only the command "
     "knows what it changed. A command therefore stores the minimum state needed for reversal "
     "as a field: CreateFleetCommand keeps the fleet it created, DeleteDriverCommand keeps the "
     "driver object it removed, AddDriverCommand keeps the driver it inserted, and the two "
     "remaining commands keep a memento. This choice has a useful consequence: the manager "
     "never inspects the state of the application, so the history is correct even when the "
     "current fleet has changed since the command ran.")
body(doc,
     "Two commands also demonstrate that the pattern covers control operations, not only data "
     "operations. UndoCommand and RedoCommand are themselves command objects; they are "
     "created by the same factory, executed by the same manager and printed by the same "
     "listing code. They simply call the manager back, and they report themselves as not "
     "undoable so that an undo of an undo does not appear in the history. ExitCommand follows "
     "the same route: it prints the closing message and clears the running flag, which stops "
     "the loop on its next test rather than terminating the process from inside a command.")
body(doc,
     "The price of the pattern is one class per function and a slightly indirect call path. "
     "For twelve functions the cost is small and it is repaid by the uniformity of the "
     "history code: showLists() prints the undo and redo lists with one statement each, "
     "because every command can describe itself. A macro command that groups several "
     "commands into one history entry, and a command that is executed asynchronously, would "
     "both be additions to the same structure rather than changes to it.")

heading(doc, "4.2 The Factory and Abstract Factory Patterns", 2)
body(doc,
     "Three kinds of object are created from a code that only the user knows at run time: the "
     "fleet, whose class depends on the type code 'v' or 'r'; the driver, which is a simple "
     "product today but may become a family of products; and the command, whose class depends "
     "on the command letter. Creating those objects with new inside the client would spread "
     "the knowledge of concrete classes across the front end and would make the type code "
     "checks and the messages that depend on them impossible to keep consistent. The factory "
     "family centralises that knowledge.")
body(doc,
     "The design uses the Abstract Factory pattern for the top-level decision and the Factory "
     "pattern inside it. SDFMSAbstractFactory is the abstract factory: its four operations "
     "create the three products and answer the two questions about fleet types, so a client "
     "can build a complete set of objects that belong to the same configuration. SDFMSFactory "
     "is the concrete factory; FleetFactory, DriverFactory and CommandFactory are the "
     "per-family factories that it composes, and FleetFactoryRegistry is the table that turns "
     "a type code into the right FleetFactory. Table 6 lists the participants, and Figure 3 "
     "shows the arrangement.")
table(doc,
      [["Participant", "Class in SDFMS", "Responsibility"],
       ["AbstractFactory", "SDFMSAbstractFactory",
        "Declares createFleet, createDriver, createCommand, isValidFleetType and "
        "getFleetTypeLabel."],
       ["ConcreteFactory", "SDFMSFactory",
        "Implements the five operations by delegating to the registry, the driver factory and "
        "the command factory."],
       ["AbstractProduct", "VehicleFleet, Driver, Command",
        "The types that clients see; no client names a concrete product class."],
       ["ConcreteProduct", "DeliveryVanFleet, RefridgeratedTruckFleet, StandardDriverFactory's "
                           "Driver, the twelve command classes",
        "The objects actually returned for a given code."],
       ["Per-family factory", "FleetFactory, DriverFactory, CommandFactory and their "
                              "implementations",
        "Encapsulate one product family each, so a family can be replaced or extended without "
        "affecting the others."],
       ["Registry", "FleetFactoryRegistry",
        "Maps a type code to a FleetFactory; new types are added with one registration call."]],
      "Participants of the Abstract Factory pattern in SDFMS",
      [3.1, 6.1, 6.5],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.JUSTIFY])
picture(doc, ASSETS / "fig2_factory.png",
        "Factory and Abstract Factory structure of SDFMS", 15.0)
body(doc,
     "The abstract factory also carries two queries that a pure factory would not need. "
     "isValidFleetType() lets CreateFleetCommand reject an unknown type before it asks for the "
     "identifier and the name, and getFleetTypeLabel() produces the words of the message "
     "'Delivery van fleet is created.' and the history entry 'Create delivery van fleet, "
     "F001, CENTRAL EXPRESS'. Because both answers come from the FleetFactory that owns the "
     "type code, the message and the history can never disagree with the object that was "
     "actually created - which would not be true if the label were a string constant in the "
     "command.")
body(doc,
     "Three alternatives were considered and rejected. A simple factory with a switch would "
     "have produced the same objects but would have left the knowledge of concrete classes in "
     "one method that every new type must edit, which is exactly what the Open-Closed "
     "Principle forbids. Creating the command objects in the front end would have moved the "
     "code-to-class mapping into the presentation layer. A single factory per product without "
     "a registry would have required CreateFleetCommand to choose between two factory "
     "variables, that is, to know the fleet types by name. The registry removes that last "
     "dependency and is why a third fleet type needs no change in the command.")

heading(doc, "4.3 The Memento Pattern", 2)
body(doc,
     "The Memento pattern captures the internal state of an object so that it can be restored "
     "later, without exposing that state to the code that requests the capture. SDFMS applies "
     "it exactly where the assignment requires it, to the two changes whose previous value "
     "cannot be reconstructed from the command's own parameters: the role of a driver and the "
     "name of a fleet. In both cases the old value belongs to the domain object, and storing a "
     "copy of it in the command would duplicate a field of another object and would let the "
     "command write that field directly.")
body(doc,
     "VehicleFleet is the originator. Its createFleetNameMemento() and "
     "createDriverRoleMemento() read the private fields and return a snapshot object; its "
     "restoreFleetName() and restoreDriverRole() write the fields back after checking that the "
     "snapshot belongs to the same fleet or driver. The snapshots, FleetNameMemento and "
     "DriverRoleMemento, implement the empty marker interface Memento and expose getters "
     "only. The caretaker is the command that requested the snapshot: "
     "ChangeFleetNameCommand keeps a FleetNameMemento and ModifyDriverRoleCommand keeps a "
     "DriverRoleMemento for exactly as long as the command lives in a history list. The "
     "repository and the command manager never hold a memento.")
picture(doc, ASSETS / "fig4_memento.png",
        "Capture and restore of a fleet name with the Memento pattern", 14.4)
body(doc,
     "The sequence in Figure 4 shows the four steps of the change and the two steps of the "
     "undo. When the command executes it first asks the originator for a snapshot, then "
     "performs the change through the originator's own operation, and then keeps the snapshot. "
     "When the manager later calls undo(), the command passes the snapshot back to the "
     "originator, which restores the field. Redo() simply executes the change again, because "
     "the new value is already part of the command; this is why no second snapshot is needed "
     "on the redo path.")
body(doc,
     "The narrow interface is what makes the pattern worth its cost. Because the command only "
     "ever holds a Memento reference and never casts it to a concrete snapshot class, adding a "
     "field to a snapshot - say, the fleet name together with the selected fleet - cannot "
     "change the command's behaviour, and no client can read or forge the state of a fleet. "
     "The alternative of storing the old role as an int field in the command would have "
     "worked for today's two cases but would have broken the encapsulation rule stated in the "
     "specification, because the command would then be able to set a private field of a "
     "driver directly. The alternative of copying the whole fleet object, as a coarse undo "
     "buffer would, is expensive and would have made the identity of the driver objects "
     "ambiguous after a restore.")

heading(doc, "4.4 Collaboration of the Three Patterns", 2)
body(doc,
     "The three patterns meet in one object graph, and it is worth following a single command "
     "from keystroke to history entry. The front end prints the menu and reads 'm'. It asks "
     "SDFMSFactory for the command with that code; the abstract factory asks "
     "SDFMSCommandFactory, which returns a ModifyDriverRoleCommand built with the shared "
     "context. The front end passes that object to CommandManager.execute(). The command "
     "reaches the current fleet through the context, validates the driver identifier, reads "
     "the new role with the prompt supplied by the fleet, asks the fleet for a "
     "DriverRoleMemento, changes the role through the driver object, prints 'Driver role is "
     "updated.' and returns. The manager then checks isUndoable(), which is true, pushes the "
     "command onto the undo list and clears the redo list. Nothing else in the system is "
     "touched, and the order of these steps is what makes the history consistent.")
body(doc,
     "The patterns divide the responsibilities cleanly. The factory decides what object "
     "represents a request; the command decides what the request does and how it is reversed; "
     "the memento decides how the previous state is carried between the two. None of the three "
     "needs to know the other two in detail: the factory returns a Command, the manager calls "
     "the Command interface, and the command uses the originator's memento operations. This is "
     "also why the two history lists can be printed by a single loop over Command objects and "
     "why the twelve commands require no per-command code in the front end.")

heading(doc, "4.5 Extending the System for New Fleet Types", 2)
body(doc,
     "The specification asks that the design be open to motorcycle-delivery fleets and "
     "electric-cargo-bike fleets. The following sketch shows the whole addition for one type; "
     "the second type is the same code with different words. The subclass only supplies the "
     "vocabulary of the new fleet; the factory only supplies the code and the label; the "
     "registry gains one line.")
code(doc,
     "public class MotorcycleFleet extends VehicleFleet {          // new file\n"
     "    public MotorcycleFleet(String fleetID) { super(fleetID); }\n"
     "    public String getFleetTypeDisplayName() { return \"Motorcycle Delivery Fleet\"; }\n"
     "    public String getRoleName(int role) {\n"
     "        return (role == 1) ? \"motorcycle rider\" : \"express courier\";\n"
     "    }\n"
     "    public String getRolePrompt() {\n"
     "        return \"Role (1 = motorcycle rider | 2 = express courier) :- \";\n"
     "    }\n"
     "    public void updateDriverRole() { /* same shape as DeliveryVanFleet */ }\n"
     "    public void showFleet()        { /* prints header, then both roles       */ }\n"
     "    public void showFleetSummary() { System.out.println(describeHeader()); }\n"
     "}\n"
     "\n"
     "public class MotorcycleFleetFactory implements FleetFactory { // new file\n"
     "    public String getTypeCode()  { return \"m\"; }\n"
     "    public String getTypeLabel() { return \"motorcycle delivery fleet\"; }\n"
     "    public VehicleFleet createFleet(String id) { return new MotorcycleFleet(id); }\n"
     "}\n"
     "\n"
     "// FleetFactoryRegistry.createDefault(): one added line\n"
     "register(new MotorcycleFleetFactory());\n", size=8.2)
body(doc,
     "After these three additions the create command accepts 'm', the new fleet appears in "
     "the listing with its own heading, its drivers are prompted with its own roles, and the "
     "history entries read 'Create motorcycle delivery fleet, F900, NIGHT LINE'. No command, "
     "no memento, no manager and no front-end class changes, which is the practical test of "
     "the Open-Closed Principle.")

# ----------------------------------------------------------------------
# 5 test plan and test cases
# ----------------------------------------------------------------------
heading(doc, "5 Test Plan and Test Cases", 1, page_break=True)
heading(doc, "5.1 Test Strategy", 2)
body(doc,
     "Testing was black box and function oriented. Each of the twelve functions was exercised "
     "through the console exactly as a user would, with the input supplied on standard input "
     "so that a run can be repeated and compared. Four kinds of test were used, listed in "
     "Table 7. The functional tests were designed from the specification and from the sample "
     "run rather than from the source code, so that a defect in the design would not be "
     "hidden by a test written to match it.")
table(doc,
      [["Level", "Purpose", "Coverage"],
       ["Functional, positive", "Confirm that each function produces the specified message and "
                                "the specified state.", "All twelve functions, both fleet types"],
       ["Functional, negative", "Confirm that invalid input is reported and that no state "
                                "changes.", "Unknown command, unknown fleet, unknown driver, "
                                             "invalid role, invalid type, duplicate identifier, "
                                             "empty name"],
       ["State-transition", "Confirm that a sequence of commands leaves the data in the "
                            "expected state, including undo and redo of each undoable "
                            "command.", "Undo and redo after create, add, modify, delete and "
                                         "rename; empty and exhausted histories"],
       ["Regression", "Confirm that the fifteen sample cases published with the assignment "
                      "are reproduced exactly.", "All fifteen sample cases, compared line by "
                                                  "line with the published output"]],
      "Levels of testing applied to SDFMS",
      [3.6, 6.5, 5.6],
      aligns=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY,
              WD_ALIGN_PARAGRAPH.JUSTIFY])
body(doc,
     "The tests ran on Windows with JDK 11 against the source directory compiled by run.bat. "
     "Each case below was driven by a script of input lines piped to the program, and the "
     "console window was captured while the case ran; the captures in Section 5.3 are the "
     "actual output of the compiled program and not retyped text. The fifteen regression "
     "cases were additionally checked mechanically: the expected lines of the published "
     "sample output were matched in order against the captured standard output, and all "
     "fifteen matched with no failure. The regression check is not part of the marks but it "
     "is the reason the messages, the capitalisation and the 'NIL' formatting can be trusted.")
body(doc,
     "The cases were also chosen to cover the boundaries that the specification implies. "
     "Table 8 summarises the eighteen cases; the identifiers used in the tables refer to the "
     "records in Section 5.3. Cases TC01 to TC12 build the state that the sample run uses, so "
     "that the later cases can be read against the published output. Cases TC13 to TC15 then "
     "exercise the history in both directions and the error paths; TC16 to TC18 add the "
     "boundaries that the sample run does not reach - an operation with no current fleet, a "
     "duplicate fleet or driver identifier, an invalid fleet type and an empty history.")

heading(doc, "5.2 Test Case Summary", 2)
table(doc,
      [["Case", "Function under test", "Input (one line per value)", "Expected result", "Result"],
       ["TC01", "Create a delivery van fleet", "c, v, F001, CENTRAL EXPRESS, x",
        "Delivery van fleet is created; current fleet is F001", "Pass"],
       ["TC02", "Add two drivers", "a, d001 Alex Chan, 1; a, d002 Jamie Lee, 2",
        "Driver is added twice; both records are stored", "Pass"],
       ["TC03", "Show the current fleet", "sf",
        "Header, then Van Driver with d001 and Courier Driver with d002", "Pass"],
       ["TC04", "Create a refrigerated truck fleet and list fleets", "c, r, F102, FROST LINE; sa",
        "Refrigerated truck fleet is created; both fleets listed in creation order", "Pass"],
       ["TC05", "Add drivers to the refrigerated fleet", "a, d101 Morgan Wong, 1; a, d102 "
                                                        "Taylor Lam, 2",
        "Driver is added twice with the truck roles", "Pass"],
       ["TC06", "Show the refrigerated fleet", "sf",
        "Refrigerated-Truck Driver and Cold-Chain Delivery Driver sections", "Pass"],
       ["TC07", "Set the current fleet by identifier", "s, F001",
        "Changed current fleet to F001", "Pass"],
       ["TC08", "Display all fleets after switching", "sa",
        "Two fleet lines, order unchanged, no driver detail", "Pass"],
       ["TC09", "Modify a driver role", "m, d001, 2",
        "Driver role is updated; d001 moves to Courier Driver", "Pass"],
       ["TC10", "Delete a driver", "d, d002",
        "Driver is deleted; Courier Driver keeps only d001", "Pass"],
       ["TC11", "Change the fleet name", "cn, METRO EXPRESS",
        "Fleet name is updated; header shows the new name", "Pass"],
       ["TC12", "List the undo and redo lists", "l",
        "Nine undo entries in execution order, empty redo list, end markers", "Pass"],
       ["TC13", "Undo three commands", "u, u, u, sf",
        "Name, deletion and role change reversed in reverse order; state matches", "Pass"],
       ["TC14", "Redo three commands", "r, r, r, sf",
        "The three undone commands re-applied in order; state matches", "Pass"],
       ["TC15", "Error handling and exit", "s F999; d d999; q; x",
        "Fleet not found, driver not found, invalid command, closing message", "Pass"],
       ["TC16", "Functions that need a current fleet", "sf; a; x",
        "No current fleet is set! for both commands; program keeps running", "Pass"],
       ["TC17", "Duplicate identifiers and invalid input", "c F001 twice; c with type q; c with "
                                                          "empty name; a d001 twice",
        "Duplicate fleet rejected, invalid fleet type rejected, empty name rejected, duplicate "
        "driver rejected", "Pass"],
       ["TC18", "Undo and redo with an empty history", "u, u, u, r, r, l",
        "No command can be undone / redone; both lists remain empty", "Pass"]],
      "Test case summary",
      [1.4, 4.2, 4.6, 4.5, 1.2],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.CENTER],
      size=8.5)

heading(doc, "5.3 Test Records", 2)
body(doc,
     "Each record states the objective, the precondition, the steps and the expected result, "
     "and is followed by the screen capture of the run. A multi-page capture is split at page "
     "boundaries; the pages are shown in order.")

cases = [
    ("TC01", "Create a delivery van fleet",
     "Confirm that the create command accepts a type code, an identifier and a name, creates "
     "the correct fleet object, selects it and prints the two required messages.",
     "The system has just started; no fleet exists; no current fleet is set.",
     "Type c, then v, then F001, then CENTRAL EXPRESS.",
     "Delivery van fleet is created. Current fleet is changed to F001. The next menu shows "
     "the current fleet line.",
     ["cap_tc01.png"]),
    ("TC02", "Add drivers to the current fleet",
     "Confirm that a driver record is parsed from 'id, name', that the role code is validated "
     "against the fleet type, and that both drivers are stored in the fleet.",
     "Fleet F001 CENTRAL EXPRESS exists and is current; it has no drivers.",
     "Type a with 'd001, Alex Chan' and role 1, then a with 'd002, Jamie Lee' and role 2.",
     "Driver is added. for each record; the history receives two Add driver entries; the "
     "fleet now holds a van driver and a courier driver.",
     ["cap_tc02.png"]),
    ("TC03", "Show the current fleet",
     "Confirm the header format, the role headings and the order of the drivers inside each "
     "role.",
     "F001 holds d001 as a van driver and d002 as a courier driver.",
     "Type sf.",
     "Delivery Van Fleet CENTRAL EXPRESS (F001), then Van Driver with 'd001, Alex Chan', then "
     "Courier Driver with 'd002, Jamie Lee'.",
     ["cap_tc03.png"]),
    ("TC04", "Create a refrigerated truck fleet and display all fleets",
     "Confirm that the second fleet type is created through the same command and that the "
     "listing shows one line per fleet in creation order.",
     "F001 exists and is current.",
     "Type c, then r, then F102, then FROST LINE, then sa.",
     "Refrigerated truck fleet is created. Current fleet is changed to F102. The listing shows "
     "Delivery Van Fleet CENTRAL EXPRESS (F001) and Refrigerated Truck Fleet FROST LINE (F102).",
     ["cap_tc04.png"]),
    ("TC05", "Add drivers to the refrigerated truck fleet",
     "Confirm that the role prompt and the stored role codes follow the refrigerated truck "
     "fleet rather than the delivery van fleet.",
     "F102 FROST LINE is current and empty; F001 keeps its two drivers.",
     "Type a with 'd101, Morgan Wong' and role 1, then a with 'd102, Taylor Lam' and role 2.",
     "The prompt reads 'Role (1 = refrigerated-truck driver | 2 = cold-chain delivery driver)' "
     "and Driver is added. is printed twice.",
     ["cap_tc05_1.png", "cap_tc05_2.png"]),
    ("TC06", "Show the refrigerated truck fleet",
     "Confirm the role headings of the second fleet type and the two-line driver format.",
     "F102 holds d101 with role 1 and d102 with role 2.",
     "Type sf.",
     "Refrigerated Truck Fleet FROST LINE (F102), then Refrigerated-Truck Driver with d101 and "
     "Cold-Chain Delivery Driver with d102.",
     ["cap_tc06_1.png", "cap_tc06_2.png"]),
    ("TC07", "Set the current fleet by identifier",
     "Confirm that the selection changes without touching the data and that the next menu "
     "reflects the new selection.",
     "Two fleets exist; F102 is current.",
     "Type s, then F001.",
     "Changed current fleet to F001. The next menu shows 'The current fleet is F001 CENTRAL "
     "EXPRESS.'",
     ["cap_tc07_1.png", "cap_tc07_2.png"]),
    ("TC08", "Display all fleets after switching the selection",
     "Confirm that the listing is independent of the current fleet and that the selection "
     "survives the command.",
     "F001 is current; both fleets hold drivers.",
     "Type sa.",
     "Two fleet lines in creation order; no driver detail; the menu still shows F001 as "
     "current.",
     ["cap_tc08_1.png", "cap_tc08_2.png"]),
    ("TC09", "Modify the role of a driver",
     "Confirm that the role change is applied to the selected driver only, that the driver "
     "moves to the other role section, and that the history receives a Modify entry.",
     "F001 is current; d001 is a van driver and d002 a courier driver.",
     "Type m, then d001, then role 2, then sf.",
     "Driver role is updated. The next listing shows 'Van Driver: NIL' and courier drivers "
     "d001 and d002.",
     ["cap_tc09_1.png", "cap_tc09_2.png"]),
    ("TC10", "Delete a driver",
     "Confirm that the driver is removed from the current fleet, that the remaining driver "
     "keeps the correct role, and that the deletion is recorded in the history.",
     "F001 is current; d001 is a courier driver and d002 a courier driver.",
     "Type d, then d002, then sf.",
     "Driver is deleted. The listing then shows Courier Driver with d001 only.",
     ["cap_tc10_1.png", "cap_tc10_2.png", "cap_tc10_3.png"]),
    ("TC11", "Change the name of the current fleet",
     "Confirm that the name is changed in the fleet object, that the header and the menu both "
     "show it, and that the history receives a Change fleet name entry.",
     "F001 is current and still named CENTRAL EXPRESS.",
     "Type cn, then METRO EXPRESS, then sf.",
     "Fleet name is updated. The header becomes 'Delivery Van Fleet METRO EXPRESS (F001)' and "
     "the menu line follows.",
     ["cap_tc11_1.png", "cap_tc11_2.png", "cap_tc11_3.png"]),
    ("TC12", "List the undo and redo lists",
     "Confirm the content, the order and the format of both lists after a sequence of nine "
     "undoable commands.",
     "The state produced by TC01 to TC11.",
     "Type l.",
     "Undo List with nine entries in execution order, the end marker, Redo List and its end "
     "marker. The redo list is empty because no command has been undone.",
     ["cap_tc12_1.png", "cap_tc12_2.png", "cap_tc12_3.png"]),
    ("TC13", "Undo three commands",
     "Confirm that undo reverses the three most recent changes in reverse order, that each "
     "reversal prints the confirmation and that the resulting state is correct.",
     "The history of TC12 with nine entries.",
     "Type u three times, then sf.",
     "Change fleet name, Delete driver and Modify driver role are undone in that order; the "
     "fleet is named CENTRAL EXPRESS again and holds d001 as a van driver and d002 as a "
     "courier driver.",
     ["cap_tc13_1.png", "cap_tc13_2.png", "cap_tc13_3.png", "cap_tc13_4.png"]),
    ("TC14", "Redo three commands",
     "Confirm that redo re-applies the undone commands in the original order and restores the "
     "state that the undo had removed.",
     "The state produced by TC13.",
     "Type r three times, then sf.",
     "The three commands are redone in order; the fleet is named METRO EXPRESS and holds d001 "
     "as a courier driver.",
     ["cap_tc14_1.png", "cap_tc14_2.png", "cap_tc14_3.png", "cap_tc14_4.png"]),
    ("TC15", "Error handling and exit",
     "Confirm that each error path prints the specified message, leaves the state unchanged "
     "and keeps the program running until the exit command.",
     "The state produced by TC14.",
     "Type s with F999, d with d999, q, then x.",
     "Fleet F999 is not found!, Driver d999 is not found in the current fleet!, Invalid "
     "command!, then Thank you for using SDFMS. System terminated. and the program ends.",
     ["cap_tc15_1.png", "cap_tc15_2.png", "cap_tc15_3.png", "cap_tc15_4.png"]),
    ("TC16", "Functions that need a current fleet",
     "Confirm that a command which needs a selected fleet reports the missing selection "
     "instead of failing, and that the program continues.",
     "A fresh run with no fleet created.",
     "Type sf, then a, then x.",
     "No current fleet is set! for both commands; no exception, no data change; the exit "
     "message is still printed.",
     ["cap_tc16.png"]),
    ("TC17", "Duplicate identifiers and invalid input",
     "Confirm that the create and add commands validate the identifier, the type code and the "
     "name before changing any state.",
     "F001 CENTRAL EXPRESS exists.",
     "Type c with v, F001, SECOND; c with type q; c with v, F900 and an empty name; c with v, "
     "F900, NIGHT LINE; a with 'd001, Alex Chan' and role 1; a with 'd001, Ben Wong' and role 1.",
     "Fleet F001 already exists!, Invalid fleet type!, Fleet ID and fleet name must not be "
     "empty!, then the fleet is created; the second add reports Driver d001 already exists in "
     "the current fleet!.",
     ["cap_tc17_1.png", "cap_tc17_2.png"]),
    ("TC18", "Undo and redo with an empty or exhausted history",
     "Confirm that undo and redo report an empty list instead of failing, and that the lists "
     "stay empty.",
     "One fleet created and nothing else.",
     "Type u three times, r twice, then l.",
     "No command can be undone. three times, No command can be redone. twice, then an empty "
     "undo list and an empty redo list between their end markers.",
     ["cap_tc18.png"]),
]

for cid, title, objective, precondition, steps, expected, shots in cases:
    shot_list = []
    for i, name in enumerate(shots, start=1):
        cap_text = "%s screen capture" % cid
        if len(shots) > 1:
            cap_text += " (page %d of %d)" % (i, len(shots))
        shot_list.append((ASSETS / name, cap_text))
    case_block(doc, cid, title, objective, precondition, steps, expected, shot_list)

heading(doc, "5.4 Summary of Test Results", 2)
body(doc,
     "All eighteen cases produced the expected result on the first run of the compiled "
     "program; no case had to be repeated after a code change. Table 9 maps each function of "
     "the specification to the cases that cover it, and the last column records the outcome.")
table(doc,
      [["Function of the specification", "Cases", "Result"],
       ["Create a vehicle fleet record", "TC01, TC04, TC17", "Pass"],
       ["Set the current fleet by Fleet ID", "TC07, TC15", "Pass"],
       ["Add a driver to the current fleet", "TC02, TC05, TC16, TC17", "Pass"],
       ["Modify the role of a driver", "TC09, TC13, TC14", "Pass"],
       ["Delete a driver", "TC10, TC13, TC15", "Pass"],
       ["Show the current fleet", "TC03, TC06, TC09, TC13", "Pass"],
       ["Display all fleets", "TC04, TC08", "Pass"],
       ["Change the name of the fleet", "TC11, TC13, TC14", "Pass"],
       ["Undo the last command", "TC13, TC18", "Pass"],
       ["Redo the last undone command", "TC14, TC18", "Pass"],
       ["Show the undo and redo lists", "TC12, TC18", "Pass"],
       ["Exit the system", "TC15, TC16, TC18", "Pass"]],
      "Coverage of the twelve functions by the test cases",
      [9.2, 4.8, 1.7],
      aligns=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.CENTER])
body(doc,
     "The regression run of the fifteen published sample cases was also successful. The "
     "expected lines of each case were matched in order against the captured output and every "
     "line was found in position, including the exact wording of the creation messages, the "
     "capitalisation of the fleet and role headings, the 'NIL' line for an empty role and the "
     "punctuation of the undo and redo messages.")

# ----------------------------------------------------------------------
# 6 user guide
# ----------------------------------------------------------------------
heading(doc, "6 User Guide", 1, page_break=True)
body(doc,
     "The program is compiled and started with the supplied batch file. Place run.bat in the "
     "directory that contains the Java source files and run it from there; the file calls "
     "javac to compile every source file and then java to start the Main class. The program "
     "reads commands from the console and ends when x is entered or when the input ends, so a "
     "script of command lines can also be piped to it.")
code(doc,
     "@echo off\n"
     "javac *.java\n"
     "if errorlevel 1 goto end\n"
     "java Main\n"
     ":end\n", size=8.4)
body(doc,
     "The menu that is printed before each prompt lists the twelve command codes. Table 10 "
     "repeats them with the input that each command expects and the message that confirms "
     "success. Every command reads one value per line; a blank line is ignored.")
table(doc,
      [["Command", "Meaning", "Additional input", "Confirmation message"],
       ["c", "Create a vehicle fleet", "type code (v or r), fleet identifier, fleet name",
        "Vehicle fleet is created; current fleet is changed"],
       ["s", "Set the current fleet", "fleet identifier", "Changed current fleet to <id>."],
       ["a", "Add a driver", "id, name; role code", "Driver is added."],
       ["m", "Modify a driver role", "driver identifier; role code", "Driver role is updated."],
       ["d", "Delete a driver", "driver identifier", "Driver is deleted."],
       ["sf", "Show the current fleet", "none", "Fleet header and drivers by role"],
       ["sa", "Display all fleets", "none", "One line per fleet"],
       ["cn", "Change the fleet name", "new name", "Fleet name is updated."],
       ["u", "Undo the last command", "none", "Command (<description>) is undone."],
       ["r", "Redo the last undone command", "none", "Command (<description>) is redone."],
       ["l", "Show the undo and redo lists", "none", "Both lists with end markers"],
       ["x", "Exit the system", "none", "Thank you for using SDFMS. System terminated."]],
      "Commands of SDFMS and the input they expect",
      [1.9, 4.0, 5.4, 4.4],
      aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
              WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
body(doc,
     "A short session makes the flow clear. The user creates one fleet, adds one driver, "
     "prints the fleet, changes the name and then reverses the change with u.")
code(doc,
     "Please enter command [ c | s | a | m | d | sf | sa | cn | u | r | l | x ] :- c\n"
     "Enter fleet type (v = delivery van | r = refrigerated truck) :- v\n"
     "Fleet ID:- F001\n"
     "Fleet Name:- CENTRAL EXPRESS\n"
     "Delivery van fleet is created.\n"
     "Current fleet is changed to F001.\n"
     "...\n"
     "Please enter command [ c | s | a | m | d | sf | sa | cn | u | r | l | x ] :- cn\n"
     "Please input new name of the current fleet:- METRO EXPRESS\n"
     "Fleet name is updated.\n"
     "...\n"
     "Please enter command [ c | s | a | m | d | sf | sa | cn | u | r | l | x ] :- u\n"
     "Command (Change fleet name, F001, METRO EXPRESS) is undone.\n", size=8.4)
body(doc,
     "Three error cases are worth remembering. An unknown command code prints 'Invalid "
     "command!' and the menu is reprinted. An operation that needs a selected fleet prints "
     "'No current fleet is set!' when no fleet has been created or selected. An unknown "
     "identifier prints either 'Fleet <id> is not found!' or 'Driver <id> is not found in the "
     "current fleet!', and in all three cases the state of the system is unchanged.")

# ----------------------------------------------------------------------
# 7 conclusion
# ----------------------------------------------------------------------
heading(doc, "7 Conclusion", 1, page_break=True)
body(doc,
     "SDFMS meets the functional requirement of the assignment: the twelve functions are "
     "implemented, the five changes that must be reversible are reversible, and the output "
     "follows the sample run for both fleet types, including the error messages and the "
     "history format. The fifteen published sample cases are reproduced line by line and the "
     "eighteen designed cases cover the twelve functions, the negative paths and the history "
     "boundaries.")
body(doc,
     "The design meets the structural requirement as well. Every user function is a Command "
     "object, including undo, redo, the history listing and exit, so the invoker and the front "
     "end treat the twelve functions uniformly. Fleets, drivers and commands are created "
     "through an abstract factory whose per-type FleetFactory objects are held in a registry, "
     "so no client class names a concrete product. The previous role of a driver and the "
     "previous name of a fleet are captured as opaque mementos and restored by the originator, "
     "so the two changes required by the specification are reversed without exposing private "
     "state. Adding a fleet type requires one subclass, one factory and one registration line, "
     "which is the practical evidence that the design obeys the Open-Closed Principle.")
body(doc,
     "The work also shows where the design would have to grow. Nothing is persisted, so a "
     "restart loses the fleets; undo and redo are in memory only and are not shared between "
     "sessions; and the console interface assumes one user. A persistent repository, a "
     "serialisable history and a graphical front end would each be additions behind the "
     "existing interfaces rather than redesigns of the three patterns, which is the property "
     "the assignment set out to test.")

heading(doc, "References", 1)
for text in [
    "[1] E. Gamma, R. Helm, R. Johnson and J. Vlissides. Design Patterns: Elements of "
    "Reusable Object-Oriented Software[M]. Reading, MA: Addison-Wesley, 1994.",
    "[2] R. C. Martin. Design Principles and Design Patterns[EB/OL]. Object Mentor, 2000. "
    "https://web.archive.org/web/20150906155800/http://www.objectmentor.com/resources/"
    "articles/Principles_and_Patterns.pdf.",
    "[3] B. Meyer. Object-Oriented Software Construction[M]. 2nd ed. Upper Saddle River, NJ: "
    "Prentice Hall, 1997.",
    "[4] Oracle. Java Platform, Standard Edition 21 API Specification[EB/OL]. "
    "https://docs.oracle.com/en/java/javase/21/docs/api/index.html.",
]:
    par = doc.add_paragraph(style="Normal")
    pf = par.paragraph_format
    pf.first_line_indent = Pt(0)
    pf.left_indent = Pt(21)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_after = Pt(4)
    run = par.add_run(text)
    set_font(run, 9.5)

# ----------------------------------------------------------------------
# appendix: source code
# ----------------------------------------------------------------------
heading(doc, "Appendix A: Well-Documented Source Code", 1, page_break=True)
body(doc,
     "The appendix reproduces every Java source file of the implementation and the batch file "
     "that compiles and runs it. The files are grouped by layer in the order used in Section "
     "3: the domain classes first, then the memento types, the command layer, the factory "
     "layer, the presentation layer and the entry class. Each class carries a class comment "
     "that states its responsibility, and the operations that implement a design pattern say "
     "which pattern they serve.")

groups = [
    ("A.1 Domain Layer", ["VehicleFleet.java", "DeliveryVanFleet.java",
                          "RefridgeratedTruckFleet.java", "Driver.java",
                          "FleetRepository.java"]),
    ("A.2 Memento Types", ["Memento.java", "FleetNameMemento.java",
                           "DriverRoleMemento.java"]),
    ("A.3 Command Layer", ["Command.java", "AbstractCommand.java", "CommandContext.java",
                           "CommandManager.java", "CreateFleetCommand.java",
                           "SetCurrentFleetCommand.java", "AddDriverCommand.java",
                           "ModifyDriverRoleCommand.java", "DeleteDriverCommand.java",
                           "ChangeFleetNameCommand.java", "ShowFleetCommand.java",
                           "DisplayAllFleetsCommand.java", "UndoCommand.java",
                           "RedoCommand.java", "ShowUndoRedoListCommand.java",
                           "ExitCommand.java"]),
    ("A.4 Factory Layer", ["SDFMSAbstractFactory.java", "SDFMSFactory.java",
                           "FleetFactory.java", "DeliveryVanFleetFactory.java",
                           "RefridgeratedTruckFleetFactory.java",
                           "FleetFactoryRegistry.java", "DriverFactory.java",
                           "StandardDriverFactory.java", "CommandFactory.java",
                           "SDFMSCommandFactory.java"]),
    ("A.5 Presentation Layer", ["ConsoleInput.java", "SDFMSApplication.java"]),
    ("A.6 Entry Point and Batch File", ["Main.java"]),
]

for title, files in groups:
    heading(doc, title, 2)
    for name in files:
        code_file(doc, name)

body(doc, "run.bat")
code(doc,
     "@echo off\n"
     "javac *.java\n"
     "if errorlevel 1 goto end\n"
     "java Main\n"
     ":end\n", size=8.4)

doc.save(str(OUT))
print("saved", OUT)

