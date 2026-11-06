/** "Display all fleets" command. */
public class DisplayAllFleetsCommand extends AbstractCommand {

    public DisplayAllFleetsCommand(CommandContext context) {
        super("sa", context);
    }

    @Override
    public void execute() {
        FleetRepository repository = getContext().getRepository();
        if (repository.isEmpty()) {
            System.out.println("No fleet record is found.");
            return;
        }
        for (VehicleFleet fleet : repository.getFleets()) {
            fleet.showFleetSummary();
        }
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Display all fleets";
    }
}
