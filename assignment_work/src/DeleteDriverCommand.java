/**
 * "Delete a driver from the current fleet" command. The removed driver object
 * is kept so that undo can put it back in the same position of the fleet.
 */
public class DeleteDriverCommand extends AbstractCommand {

    private VehicleFleet targetFleet;
    private String driverID;
    private Driver deletedDriver;

    public DeleteDriverCommand(CommandContext context) {
        super("d", context);
    }

    @Override
    public void execute() {
        targetFleet = getContext().getCurrentFleetOrReport();
        if (targetFleet == null) {
            return;
        }
        driverID = getContext().getInput().readLine("Please input driver ID:- ");
        deletedDriver = targetFleet.findDriver(driverID);
        if (deletedDriver == null) {
            System.out.println("Driver " + driverID + " is not found in the current fleet!");
            return;
        }
        applyChange();
        System.out.println("Driver is deleted.");
    }

    private void applyChange() {
        targetFleet.dropDriver(deletedDriver);
    }

    @Override
    public void undo() {
        targetFleet.addDriver(deletedDriver);
    }

    @Override
    public void redo() {
        applyChange();
    }

    @Override
    public String getDescription() {
        return "Delete driver, " + driverID;
    }
}
