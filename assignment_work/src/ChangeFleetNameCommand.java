/**
 * "Change the name of the current fleet" command. The previous name is
 * captured in a memento before the change and restored on undo.
 */
public class ChangeFleetNameCommand extends AbstractCommand {

    private VehicleFleet fleet;
    private String newName;
    private Memento memento;

    public ChangeFleetNameCommand(CommandContext context) {
        super("cn", context);
    }

    @Override
    public void execute() {
        fleet = getContext().getCurrentFleetOrReport();
        if (fleet == null) {
            return;
        }
        newName = getContext().getInput().readLine(
                "Please input new name of the current fleet:- ");
        if (newName == null || newName.isEmpty()) {
            System.out.println("Fleet name must not be empty!");
            return;
        }
        memento = fleet.createFleetNameMemento();
        applyChange();
        System.out.println("Fleet name is updated.");
    }

    private void applyChange() {
        fleet.setName(newName);
    }

    @Override
    public void undo() {
        fleet.restoreFleetName(memento);
    }

    @Override
    public void redo() {
        applyChange();
    }

    @Override
    public String getDescription() {
        return "Change fleet name, " + fleet.getFleetID() + ", " + newName;
    }
}
