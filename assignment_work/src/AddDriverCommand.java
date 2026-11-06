/**
 * "Add a driver to the current fleet" command. The driver object is created
 * by the abstract factory and kept in the command so that undo can remove it
 * and redo can add the same driver back.
 */
public class AddDriverCommand extends AbstractCommand {

    private String driverID;
    private String driverName;
    private int role;
    private VehicleFleet targetFleet;
    private Driver driver;

    public AddDriverCommand(CommandContext context) {
        super("a", context);
    }

    @Override
    public void execute() {
        targetFleet = getContext().getCurrentFleetOrReport();
        if (targetFleet == null) {
            return;
        }
        String[] information = getContext().getInput().readDriverInformation();
        if (information == null) {
            System.out.println("Invalid driver information!");
            return;
        }
        driverID = information[0];
        driverName = information[1];
        if (targetFleet.hasDriver(driverID)) {
            System.out.println("Driver " + driverID + " already exists in the current fleet!");
            return;
        }
        role = getContext().getInput().readRole(targetFleet.getRolePrompt());
        if (!isValidRole()) {
            System.out.println("Invalid role!");
            return;
        }
        driver = getContext().getFactory().createDriver(driverID, driverName, role);
        applyChange();
        System.out.println("Driver is added.");
    }

    private boolean isValidRole() {
        return role == 1 || role == 2;
    }

    private void applyChange() {
        targetFleet.addDriver(driver);
    }

    @Override
    public void undo() {
        targetFleet.dropDriver(driver);
    }

    @Override
    public void redo() {
        applyChange();
    }

    @Override
    public String getDescription() {
        return "Add driver, " + driverID + ", " + driverName + ", "
                + targetFleet.getRoleName(role);
    }
}
