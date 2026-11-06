/**
 * "Create a vehicle fleet record" command. The fleet object itself is
 * created by the abstract factory from the type code typed by the user.
 */
public class CreateFleetCommand extends AbstractCommand {

    private String fleetTypeCode;
    private String fleetID;
    private String fleetName;
    private VehicleFleet createdFleet;

    public CreateFleetCommand(CommandContext context) {
        super("c", context);
    }

    @Override
    public void execute() {
        ConsoleInput input = getContext().getInput();
        FleetRepository repository = getContext().getRepository();
        SDFMSAbstractFactory factory = getContext().getFactory();

        fleetTypeCode = input.readLine(
                "Enter fleet type (v = delivery van | r = refrigerated truck) :- ");
        if (!factory.isValidFleetType(fleetTypeCode)) {
            System.out.println("Invalid fleet type!");
            return;
        }
        fleetID = input.readLine("Fleet ID:- ");
        fleetName = input.readLine("Fleet Name:- ");
        if (fleetID == null || fleetID.isEmpty() || fleetName == null || fleetName.isEmpty()) {
            System.out.println("Fleet ID and fleet name must not be empty!");
            return;
        }
        if (repository.containsFleet(fleetID)) {
            System.out.println("Fleet " + fleetID + " already exists!");
            return;
        }

        createdFleet = factory.createFleet(fleetTypeCode, fleetID);
        createdFleet.setName(fleetName);
        applyChange();
        System.out.println(capitalize(factory.getFleetTypeLabel(fleetTypeCode))
                + " is created.");
        System.out.println("Current fleet is changed to " + fleetID + ".");
    }

    private void applyChange() {
        getContext().getRepository().addFleet(createdFleet);
        getContext().getRepository().setCurrentFleet(createdFleet);
    }

    @Override
    public void undo() {
        getContext().getRepository().removeFleet(createdFleet);
    }

    @Override
    public void redo() {
        applyChange();
    }

    @Override
    public String getDescription() {
        return "Create " + getContext().getFactory().getFleetTypeLabel(fleetTypeCode)
                + ", " + fleetID + ", " + fleetName;
    }

    private static String capitalize(String text) {
        if (text == null || text.isEmpty()) {
            return text;
        }
        return Character.toUpperCase(text.charAt(0)) + text.substring(1);
    }
}
