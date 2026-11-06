/**
 * "Set the current fleet by Fleet ID" command. Setting the current fleet
 * changes the working context only, so it is not part of the undo history.
 */
public class SetCurrentFleetCommand extends AbstractCommand {

    public SetCurrentFleetCommand(CommandContext context) {
        super("s", context);
    }

    @Override
    public void execute() {
        String fleetID = getContext().getInput().readLine("Please input fleet ID:- ");
        FleetRepository repository = getContext().getRepository();
        VehicleFleet fleet = repository.findFleet(fleetID);
        if (fleet == null) {
            System.out.println("Fleet " + fleetID + " is not found!");
            return;
        }
        repository.setCurrentFleet(fleet);
        System.out.println("Changed current fleet to " + fleet.getFleetID() + ".");
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Set current fleet";
    }
}
