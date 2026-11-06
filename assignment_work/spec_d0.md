Hong Kong Institute of Information Technology

HIGHER DIPLOMA IN SOFTWARE ENGINEERING (IT114105)

Module Name: 	Contemporary Topics in Software Engineering

Module Code: 	ITP4507

Assignment Number: 	One

Hand-in: 	Friday 13 November, 2026 (On or before 4:30 PM to Moodle)

Weighting of This Assignment: 	66.67% of the End of Module Assessment

This assignment must be completed individually. Plagiarism will be treated seriously. Any assignment found to be wholly or partly involved in plagiarism, whether submitted by the original author or another student, will receive zero marks. Late submission will NOT be accepted.

Task Specification

The Smart Delivery Logistics Company provides delivery and fleet coordination services for commercial customers. It operates different types of delivery vehicles and maintains information about drivers assigned to vehicle fleets. The company plans to develop a Smart Delivery Fleet Management System (SDFMS) to maintain drivers in fleets for different kinds of delivery vehicles. At present, the system accommodates delivery van fleets and refrigerated truck fleets, with plans for expansion to include more fleet varieties in future. Below is the simplified class diagram representing the current data structure in SDFMS.

Note: VehicleFleet is an abstract class. updateDriverRole() and showFleet() are abstract operations. Vector or LinkedList may be used as the concrete implementation of AbstractList.

As a system analyst of the Company, you are required to design and develop SDFMS. You are reminded not to remove or modify the attributes and operations shown in the existing classes: VehicleFleet, DeliveryVanFleet, RefrigeratedTruckFleet, and Driver. You may introduce additional classes and interfaces where necessary.

SDFMS should provide the following functions:

Create a vehicle fleet record.

Set the current fleet by Fleet ID.

Add a driver to the current fleet.

Modify the role of a driver in the current fleet.

Delete a driver from the current fleet.

Show the current fleet.

Display all fleets.

Change the name of the current fleet.

Undo the last command.

Redo the last undone command.

Show the undo/redo lists.

Exit the system.

Your system design should conform to the Open-Closed Principle so that the system can be easily extended to support new fleet types, such as motorcycle-delivery fleets and electric-cargo-bike fleets.

You MUST apply the following design patterns for your new system

Command pattern to provide the “create fleet”, “set current fleet”, “add driver”, “modify driver role”, “delete driver”, “show current fleet”, “display all fleets”, “change fleet name”, “undo”, “redo” and “show undo/redo lists” functions.

Factory pattern or Abstract Factory pattern to create different kinds of Command objects, VehicleFleet objects and Driver objects, such as DeliveryVanFleet, RefrigeratedTruckFleet and Driver objects.

Memento pattern to provide “Undo” and “Redo” functions for the “modify driver role” and “change fleet name” functions.

The “create fleet”, “add driver”, “modify driver role”, “delete driver” and “change fleet name” functions must support undo and redo. The Memento pattern must be applied to the “modify driver role” and “change fleet name” functions.

Assignment Report

In addition to the system development, you are required to write a Short Report covering the following sections:

1. Assumptions regarding the problem context

2. Application design with class diagram

3. Discussion and explanation on each of the design patterns applied to the application

4. Test Plan and Test Cases

5. Well-documented source code

Mark Allocation

Your assignment work will be marked according to the following criteria.

| Work | Mark Allocated |
| --- | --- |
| System Coding and Implementation |  |
| Implementation of the system and coding style<br>(Hard-coded output will result in zero mark.) | 30% |
| Correctness of system functions *<br>(Hard-coded output will result in zero mark.) | 15% |
| Test Plan and Test Cases<br>(Will be used in testing your own application.) | 10% |
|  |  |
| System Analysis and Design, and Discussion |  |
| Design of your system and correct use of design patterns | 20% |
| Application design with class diagram | 10% |
| Discussion and explanation on each of the design patterns applied to the application | 15% |
|  |  |
| Total | 100% |

Note: * Please note that your source code will be recompiled and tested for the correctness of the system functions. You need to provide Windows batch file run.bat for compiling and running your system. For example, the run.bat file may contain the following commands for compiling Java source code and running your system:

javac *.java

java Main

Submission of Assignment Work

The front page of your submission should include the programme title(code), module title(code), and student number and student name.

Submit your Java source code and your report to https://moodle.vtc.edu.hk .

Well-documented source code of your program and a Windows batch file run.bat for compiling and running your system.

A report covering the analysis, design, discussion, user guide, test plan and test cases for your work.

The assumption made during analysis and design of the application

System design on your application with class diagram

Discussion of the design patterns applied in your program.

Test Plan with Test Cases (Design your own test plan and corresponding test cases for each function. For each test case, you should provide a SCREEN CAPTURE for test result).

Submit according to the guideline on the top part of cover page. Late submission will NOT be accepted.

Extra Reference: Sample Test

Testing Method

This sample run is served for reference only. You are free to design your own user interface. However, the input commands cannot be changed.

Sample Run of assignment

You may follow the design of user interface shown in this sample run in DOS command prompt.

In the following examples, characters shown in bold red text represent the user’s input.

1. Create a delivery van fleet

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- c<br>Enter fleet type (v = delivery van \| r = refrigerated truck) :- v<br>Fleet ID:- F001<br>Fleet Name:- CENTRAL EXPRESS<br>Delivery van fleet is created.<br>Current fleet is changed to F001. |
| --- |

2. Add drivers to the delivery van fleet

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- a<br>Please input driver information (id, name):- d001, Alex Chan<br>Role (1 = van driver \| 2 = courier driver) :- 1<br>Driver is added.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- a<br>Please input driver information (id, name):- d002, Jamie Lee<br>Role (1 = van driver \| 2 = courier driver) :- 2<br>Driver is added. |
| --- |

3. Show the current fleet

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sf<br>Delivery Van Fleet CENTRAL EXPRESS (F001)<br>Van Driver:<br>d001, Alex Chan<br>Courier Driver:<br>d002, Jamie Lee |
| --- |

4. Create a refrigerated truck fleet and display all fleets

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- c<br>Enter fleet type (v = delivery van \| r = refrigerated truck) :- r<br>Fleet ID:- F102<br>Fleet Name:- FROST LINE<br>Refrigerated truck fleet is created.<br>Current fleet is changed to F102.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F102 FROST LINE.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sa<br>Delivery Van Fleet CENTRAL EXPRESS (F001)<br>Refrigerated Truck Fleet FROST LINE (F102) |
| --- |

5. Add drivers to the refrigerated truck fleet

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F102 FROST LINE.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- a<br>Please input driver information (id, name):- d101, Morgan Wong<br>Role (1 = refrigerated-truck driver \| 2 = cold-chain delivery driver) :- 1<br>Driver is added.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F102 FROST LINE.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- a<br>Please input driver information (id, name):- d102, Taylor Lam<br>Role (1 = refrigerated-truck driver \| 2 = cold-chain delivery driver) :- 2<br>Driver is added. |
| --- |

6. Show the current fleet

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F102 FROST LINE.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sf<br>Refrigerated Truck Fleet FROST LINE (F102)<br>Refrigerated-Truck Driver:<br>d101, Morgan Wong<br>Cold-Chain Delivery Driver:<br>d102, Taylor Lam |
| --- |

7. Set the current fleet by Fleet ID

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F102 FROST LINE.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- s<br>Please input fleet ID:- F001<br>Changed current fleet to F001. |
| --- |

8. Display all fleets

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sa<br>Delivery Van Fleet CENTRAL EXPRESS (F001)<br>Refrigerated Truck Fleet FROST LINE (F102) |
| --- |

9. Modify a driver role

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- m<br>Please input driver ID:- d001<br>Role (1 = van driver \| 2 = courier driver) :- 2<br>Driver role is updated.<br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sf<br>Delivery Van Fleet CENTRAL EXPRESS (F001)<br>Van Driver: NIL<br>Courier Driver:<br>d001, Alex Chan<br>d002, Jamie Lee |
| --- |

10. Delete a driver

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- d<br>Please input driver ID:- d002<br>Driver is deleted.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sf<br>Delivery Van Fleet CENTRAL EXPRESS (F001)<br>Van Driver: NIL<br>Courier Driver:<br>d001, Alex Chan |
| --- |

11. Change the name of the current fleet

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- cn<br>Please input new name of the current fleet:- METRO EXPRESS<br>Fleet name is updated.<br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sf<br>Delivery Van Fleet METRO EXPRESS (F001)<br>Van Driver: NIL<br>Courier Driver:<br>d001, Alex Chan |
| --- |

12. Show undo/redo lists

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- l<br>Undo List<br>Create delivery van fleet, F001, CENTRAL EXPRESS<br>Add driver, d001, Alex Chan, van driver<br>Add driver, d002, Jamie Lee, courier driver<br>Create refrigerated truck fleet, F102, FROST LINE<br>Add driver, d101, Morgan Wong, refrigerated-truck driver<br>Add driver, d102, Taylor Lam, cold-chain delivery driver<br>Modify driver role, d001, courier driver<br>Delete driver, d002<br>Change fleet name, F001, METRO EXPRESS<br>-- End of undo list --<br>Redo List<br>-- End of redo list -- |
| --- |

13. UNDO actions in UNDO list

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- u<br>Command (Change fleet name, F001, METRO EXPRESS) is undone.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- u<br>Command (Delete driver, d002) is undone.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- u<br>Command (Modify driver role, d001, courier driver) is undone.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sf<br>Delivery Van Fleet CENTRAL EXPRESS (F001)<br>Van Driver:<br>d001, Alex Chan<br>Courier Driver:<br>d002, Jamie Lee |
| --- |

14. REDO actions in REDO list

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- r<br>Command (Modify driver role, d001, courier driver) is redone.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- r<br>Command (Delete driver, d002) is redone.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 CENTRAL EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- r<br>Command (Change fleet name, F001, METRO EXPRESS) is redone.<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- sf<br>Delivery Van Fleet METRO EXPRESS (F001)<br>Van Driver: NIL<br>Courier Driver:<br>d001, Alex Chan |
| --- |

15. Error handling and exit

| Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- s<br>Please input fleet ID:- F999<br>Fleet F999 is not found!<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- d<br>Please input driver ID:- d999<br>Driver d999 is not found in the current fleet!<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- q<br>Invalid command!<br><br>Smart Delivery Fleet Management System (SDFMS)<br>c = create fleet, s = set current fleet, a = add driver, m = modify driver role,<br>d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,<br>u = undo, r = redo, l = list undo/redo, x = exit system<br>The current fleet is F001 METRO EXPRESS.<br>Please enter command [ c \| s \| a \| m \| d \| sf \| sa \| cn \| u \| r \| l \| x ] :- x<br>Thank you for using SDFMS. System terminated.<br>- END OF SAMPLE TEST - |
| --- |
