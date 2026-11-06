/** "Show the current fleet" command. */
public class ShowFleetCommand extends AbstractCommand {

    public ShowFleetCommand(CommandContext context) {
        super("sf", context);
    }

    @Override
    public void execute() {
        VehicleFleet current = getContext().getCurrentFleetOrReport();
        if (current == null) {
            return;
        }
        current.showFleet();
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Show current fleet";
    }
}
