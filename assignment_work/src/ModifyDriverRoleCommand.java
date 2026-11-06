/**
 * "Modify the role of a driver in the current fleet" command. The old role
 * is captured in a memento before the change and restored on undo.
 */
public class ModifyDriverRoleCommand extends AbstractCommand {

    private VehicleFleet fleet;
    private String driverID;
    private int newRole;
    private Memento memento;

    public ModifyDriverRoleCommand(CommandContext context) {
        super("m", context);
    }

    @Override
    public void execute() {
        fleet = getContext().getCurrentFleetOrReport();
        if (fleet == null) {
            return;
        }
        driverID = getContext().getInput().readLine("Please input driver ID:- ");
        if (!fleet.hasDriver(driverID)) {
            System.out.println("Driver " + driverID + " is not found in the current fleet!");
            return;
        }
        newRole = getContext().getInput().readRole(fleet.getRolePrompt());
        if (newRole != 1 && newRole != 2) {
            System.out.println("Invalid role!");
            return;
        }
        memento = fleet.createDriverRoleMemento(driverID);
        applyChange();
        System.out.println("Driver role is updated.");
    }

    private void applyChange() {
        Driver driver = fleet.findDriver(driverID);
        if (driver != null) {
            driver.setRole(newRole);
        }
    }

    @Override
    public void undo() {
        fleet.restoreDriverRole(memento);
    }

    @Override
    public void redo() {
        applyChange();
    }

    @Override
    public String getDescription() {
        return "Modify driver role, " + driverID + ", " + fleet.getRoleName(newRole);
    }
}
