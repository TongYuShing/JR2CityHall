# Assignment — Smart Delivery Fleet Management System (SDFMS)

# ITP4507 Assignment — Smart Delivery Fleet Management System (SDFMS)

**Module:** ITP4507 Contemporary Topics in Software Engineering

**Programme:** Higher Diploma in Software Engineering (IT114105)

**Assignment Number:** One

**Hand-in:** Friday 13 November 2026 (on or before 4:30 PM)

**Weighting:** 66.67% of the End of Module Assessment

This assignment must be completed individually. Plagiarism will be treated seriously. Any assignment found to be wholly or partly involved in plagiarism, whether submitted by the original author or another student, will receive zero marks. Late submission will NOT be accepted.

## Task Specification

The Smart Delivery Logistics Company provides delivery and fleet coordination services for commercial customers. It operates different types of delivery vehicles and maintains information about drivers assigned to vehicle fleets. The company plans to develop a Smart Delivery Fleet Management System (SDFMS) to maintain drivers in fleets for different kinds of delivery vehicles. At present, the system accommodates delivery van fleets and refrigerated truck fleets, with plans for expansion to include more fleet varieties in future.

Note: `VehicleFleet` is an abstract class. `updateDriverRole()` and `showFleet()` are abstract operations. `Vector` or `LinkedList` may be used as the concrete implementation of `AbstractList`.

As a system analyst of the Company, you are required to design and develop SDFMS. You are reminded **not to remove or modify the attributes and operations** shown in the existing classes: `VehicleFleet`, `DeliveryVanFleet`, `RefrigeratedTruckFleet`, and `Driver`. You may introduce additional classes and interfaces where necessary.

SDFMS should provide the following functions:

1. Create a vehicle fleet record.
2. Set the current fleet by Fleet ID.
3. Add a driver to the current fleet.
4. Modify the role of a driver in the current fleet.
5. Delete a driver from the current fleet.
6. Show the current fleet.
7. Display all fleets.
8. Change the name of the current fleet.
9. Undo the last command.
10. Redo the last undone command.
11. Show the undo/redo lists.
12. Exit the system.

Your system design should conform to the **Open-Closed Principle** so that the system can be easily extended to support new fleet types, such as motorcycle-delivery fleets and electric-cargo-bike fleets.

### Required design patterns

- **Command pattern** — for the "create fleet", "set current fleet", "add driver", "modify driver role", "delete driver", "show current fleet", "display all fleets", "change fleet name", "undo", "redo" and "show undo/redo lists" functions.
- **Factory pattern** or **Abstract Factory pattern** — to create different kinds of Command objects, VehicleFleet objects and Driver objects, such as `DeliveryVanFleet`, `RefrigeratedTruckFleet` and `Driver` objects.
- **Memento pattern** — to provide "Undo" and "Redo" functions for the "modify driver role" and "change fleet name" functions.

The "create fleet", "add driver", "modify driver role", "delete driver" and "change fleet name" functions must support undo and redo. The Memento pattern must be applied to the "modify driver role" and "change fleet name" functions.

## Assignment Report

In addition to the system development, you are required to write a Short Report covering the following sections:

1. Assumptions regarding the problem context
2. Application design with class diagram
3. Discussion and explanation on each of the design patterns applied to the application
4. Test Plan and Test Cases
5. Well-documented source code

## Mark Allocation

| Work | Mark Allocated |
| --- | --- |
| System Coding and Implementation | |
| Implementation of the system and coding style (Hard-coded output will result in zero mark.) | 30% |
| Correctness of system functions * (Hard-coded output will result in zero mark.) | 15% |
| Test Plan and Test Cases | 10% |
| System Analysis and Design, and Discussion | |
| Design of your system and correct use of design patterns | 20% |
| Application design with class diagram | 10% |
| Discussion and explanation on each of the design patterns applied to the application | 15% |
| Total | 100% |

\* Please note that your source code will be recompiled and tested for the correctness of the system functions.

## Testing method

You can ease testing by using copy and paste rather than inputting data manually. Prepare a text file which includes all the user inputs for a run, then paste it into the console. This automatically feeds the input and you get the result automatically. The input commands cannot be changed. You are free to design your own user interface.

### Sample run — input sequence

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
d
d002
sf
cn
METRO EXPRESS
sf
l
u
u
u
sf
r
r
r
sf
s
F999
d
d999
q
x
```

The visible test cases on this lab page demonstrate the expected console output for each step of this sample run.

## Submitting

The autograder recompiles your submitted `.java` source and runs the class **`Main`**, feeding the test inputs on standard input. Compile and run your system as:

```
javac *.java
java Main
```

Submit your Java source code and your report to https://moodle.vtc.edu.hk. You need to provide a Windows batch file `run.bat` for compiling and running your system.

Submit according to the guideline on the top part of the cover page. Late submission will NOT be accepted.


## Entry point

Implement `Main` (class `Main` with a `main` method).

## How grading works

Push your `.java` sources to the default branch (`main`). The platform clones
your repository at the pushed commit, compiles every `.java` file with
`javac --release 21`, runs the entry class against all test cases, and posts the result as a commit status on
this repository. You can also grade your latest commit manually from the lab
page.

Keep solutions in this repository — your commits are part of your submission
history.

## Sample test cases

### Sample case 1

**Input**

```
c
v
F001
CENTRAL EXPRESS
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Thank you for using SDFMS. System terminated.
```

### Sample case 2

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Thank you for using SDFMS. System terminated.
```

### Sample case 3

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Thank you for using SDFMS. System terminated.
```

### Sample case 4

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Thank you for using SDFMS. System terminated.
```

### Sample case 5

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Thank you for using SDFMS. System terminated.
```

### Sample case 6

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Thank you for using SDFMS. System terminated.
```

### Sample case 7

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Thank you for using SDFMS. System terminated.
```

### Sample case 8

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Thank you for using SDFMS. System terminated.
```

### Sample case 9

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver role is updated.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
d002, Jamie Lee
Thank you for using SDFMS. System terminated.
```

### Sample case 10

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
d
d002
sf
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver role is updated.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
d002, Jamie Lee
Driver is deleted.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Thank you for using SDFMS. System terminated.
```

### Sample case 11

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
d
d002
sf
cn
METRO EXPRESS
sf
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver role is updated.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
d002, Jamie Lee
Driver is deleted.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Fleet name is updated.
Delivery Van Fleet METRO EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Thank you for using SDFMS. System terminated.
```

### Sample case 12

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
d
d002
sf
cn
METRO EXPRESS
sf
l
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver role is updated.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
d002, Jamie Lee
Driver is deleted.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Fleet name is updated.
Delivery Van Fleet METRO EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Undo List
Create delivery van fleet, F001, CENTRAL EXPRESS
Add driver, d001, Alex Chan, van driver
Add driver, d002, Jamie Lee, courier driver
Create refrigerated truck fleet, F102, FROST LINE
Add driver, d101, Morgan Wong, refrigerated-truck driver
Add driver, d102, Taylor Lam, cold-chain delivery driver
Modify driver role, d001, courier driver
Delete driver, d002
Change fleet name, F001, METRO EXPRESS
-- End of undo list --
Redo List
-- End of redo list --
Thank you for using SDFMS. System terminated.
```

### Sample case 13

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
d
d002
sf
cn
METRO EXPRESS
sf
l
u
u
u
sf
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver role is updated.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
d002, Jamie Lee
Driver is deleted.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Fleet name is updated.
Delivery Van Fleet METRO EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Undo List
Create delivery van fleet, F001, CENTRAL EXPRESS
Add driver, d001, Alex Chan, van driver
Add driver, d002, Jamie Lee, courier driver
Create refrigerated truck fleet, F102, FROST LINE
Add driver, d101, Morgan Wong, refrigerated-truck driver
Add driver, d102, Taylor Lam, cold-chain delivery driver
Modify driver role, d001, courier driver
Delete driver, d002
Change fleet name, F001, METRO EXPRESS
-- End of undo list --
Redo List
-- End of redo list --
Command (Change fleet name, F001, METRO EXPRESS) is undone.
Command (Delete driver, d002) is undone.
Command (Modify driver role, d001, courier driver) is undone.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Thank you for using SDFMS. System terminated.
```

### Sample case 14

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
d
d002
sf
cn
METRO EXPRESS
sf
l
u
u
u
sf
r
r
r
sf
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver role is updated.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
d002, Jamie Lee
Driver is deleted.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Fleet name is updated.
Delivery Van Fleet METRO EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Undo List
Create delivery van fleet, F001, CENTRAL EXPRESS
Add driver, d001, Alex Chan, van driver
Add driver, d002, Jamie Lee, courier driver
Create refrigerated truck fleet, F102, FROST LINE
Add driver, d101, Morgan Wong, refrigerated-truck driver
Add driver, d102, Taylor Lam, cold-chain delivery driver
Modify driver role, d001, courier driver
Delete driver, d002
Change fleet name, F001, METRO EXPRESS
-- End of undo list --
Redo List
-- End of redo list --
Command (Change fleet name, F001, METRO EXPRESS) is undone.
Command (Delete driver, d002) is undone.
Command (Modify driver role, d001, courier driver) is undone.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Command (Modify driver role, d001, courier driver) is redone.
Command (Delete driver, d002) is redone.
Command (Change fleet name, F001, METRO EXPRESS) is redone.
Delivery Van Fleet METRO EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Thank you for using SDFMS. System terminated.
```

### Sample case 15

**Input**

```
c
v
F001
CENTRAL EXPRESS
a
d001, Alex Chan
1
a
d002, Jamie Lee
2
sf
c
r
F102
FROST LINE
sa
a
d101, Morgan Wong
1
a
d102, Taylor Lam
2
sf
s
F001
sa
m
d001
2
sf
d
d002
sf
cn
METRO EXPRESS
sf
l
u
u
u
sf
r
r
r
sf
s
F999
d
d999
q
x
x

```

**Expected output**

```
Delivery van fleet is created.
Current fleet is changed to F001.
Driver is added.
Driver is added.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Refrigerated truck fleet is created.
Current fleet is changed to F102.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver is added.
Driver is added.
Refrigerated Truck Fleet FROST LINE (F102)
Refrigerated-truck Driver:
d101, Morgan Wong
Cold-chain Delivery Driver:
d102, Taylor Lam
Changed current fleet to F001.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Refrigerated Truck Fleet FROST LINE (F102)
Driver role is updated.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
d002, Jamie Lee
Driver is deleted.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Fleet name is updated.
Delivery Van Fleet METRO EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Undo List
Create delivery van fleet, F001, CENTRAL EXPRESS
Add driver, d001, Alex Chan, van driver
Add driver, d002, Jamie Lee, courier driver
Create refrigerated truck fleet, F102, FROST LINE
Add driver, d101, Morgan Wong, refrigerated-truck driver
Add driver, d102, Taylor Lam, cold-chain delivery driver
Modify driver role, d001, courier driver
Delete driver, d002
Change fleet name, F001, METRO EXPRESS
-- End of undo list --
Redo List
-- End of redo list --
Command (Change fleet name, F001, METRO EXPRESS) is undone.
Command (Delete driver, d002) is undone.
Command (Modify driver role, d001, courier driver) is undone.
Delivery Van Fleet CENTRAL EXPRESS (F001)
Van Driver:
d001, Alex Chan
Courier Driver:
d002, Jamie Lee
Command (Modify driver role, d001, courier driver) is redone.
Command (Delete driver, d002) is redone.
Command (Change fleet name, F001, METRO EXPRESS) is redone.
Delivery Van Fleet METRO EXPRESS (F001)
Van Driver: NIL
Courier Driver:
d001, Alex Chan
Fleet F999 is not found!
Driver d999 is not found in the current fleet!
Invalid command!
Thank you for using SDFMS. System terminated.
```

