/**
 * Console front end of SDFMS. It prints the menu, reads a command code, asks
 * the abstract factory for the matching Command object and lets the command
 * manager execute it.
 */
public class SDFMSApplication {

    private static final String SYSTEM_TITLE =
            "Smart Delivery Fleet Management System (SDFMS)";
    private static final String MENU_LINE_1 =
            "c = create fleet, s = set current fleet, a = add driver, m = modify driver role,";
    private static final String MENU_LINE_2 =
            "d = delete driver, sf = show fleet, sa = display all fleets, cn = change fleet name,";
    private static final String MENU_LINE_3 =
            "u = undo, r = redo, l = list undo/redo, x = exit system";
    private static final String COMMAND_PROMPT =
            "Please enter command [ c | s | a | m | d | sf | sa | cn | u | r | l | x ] :- ";

    private final CommandContext context;

    public SDFMSApplication(CommandContext context) {
        this.context = context;
    }

    /** Runs the read-execute loop until the exit command or end of input. */
    public void run() {
        printMenu();
        while (context.isRunning()) {
            String commandCode = context.getInput().readLine(COMMAND_PROMPT);
            while (commandCode != null && commandCode.isEmpty()) {
                commandCode = context.getInput().readLine(COMMAND_PROMPT);
            }
            if (commandCode == null) {
                break;
            }
            Command command = context.getFactory().createCommand(commandCode);
            if (command == null) {
                System.out.println("Invalid command!");
            } else {
                context.getCommandManager().execute(command);
            }
            if (context.isRunning()) {
                printMenu();
            }
        }
    }

    private void printMenu() {
        System.out.println(SYSTEM_TITLE);
        System.out.println(MENU_LINE_1);
        System.out.println(MENU_LINE_2);
        System.out.println(MENU_LINE_3);
        VehicleFleet current = context.getRepository().getCurrentFleet();
        if (current != null) {
            System.out.println("The current fleet is " + current.getFleetID() + " "
                    + current.getName() + ".");
        }
    }
}
