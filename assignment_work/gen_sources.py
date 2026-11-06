import pathlib

SRC = pathlib.Path(__file__).resolve().parent / "src"
SRC.mkdir(parents=True, exist_ok=True)

FILES = {}

FILES["Driver.java"] = r'''/**
 * A driver that can be assigned to a vehicle fleet.
 *
 * <p>The attributes and operations of this class are those supplied in the
 * assignment skeleton; only documentation has been added.</p>
 */
public class Driver {

    private String driverID;
    private String driverName;
    private int role;

    /**
     * Creates a driver.
     *
     * @param driverID   unique driver identifier, e.g. "d001"
     * @param driverName driver name, e.g. "Alex Chan"
     * @param role       role code inside the fleet (1 or 2, meaning depends on
     *                   the type of fleet the driver belongs to)
     */
    public Driver(String driverID, String driverName, int role) {
        this.driverID = driverID;
        this.driverName = driverName;
        this.role = role;
    }

    public String getDriverID() {
        return driverID;
    }

    public String getName() {
        return driverName;
    }

    public int getRole() {
        return role;
    }

    public void setName(String driverName) {
        this.driverName = driverName;
    }

    public void setRole(int role) {
        this.role = role;
    }
}
'''

FILES["Memento.java"] = r'''/**
 * Marker interface for all memento objects used by the undo mechanism.
 *
 * <p>A memento is an opaque snapshot of the state of an originator. Only the
 * originator that created it knows how to interpret it, which keeps the
 * command objects independent of the internal structure of the fleet.</p>
 */
public interface Memento {
}
'''

FILES["FleetNameMemento.java"] = r'''/**
 * Memento that stores the name of a fleet before it is changed.
 */
public class FleetNameMemento implements Memento {

    private final String fleetID;
    private final String fleetName;

    public FleetNameMemento(String fleetID, String fleetName) {
        this.fleetID = fleetID;
        this.fleetName = fleetName;
    }

    public String getFleetID() {
        return fleetID;
    }

    public String getFleetName() {
        return fleetName;
    }
}
'''

FILES["DriverRoleMemento.java"] = r'''/**
 * Memento that stores the role of a driver before it is modified.
 */
public class DriverRoleMemento implements Memento {

    private final String driverID;
    private final int role;

    public DriverRoleMemento(String driverID, int role) {
        this.driverID = driverID;
        this.role = role;
    }

    public String getDriverID() {
        return driverID;
    }

    public int getRole() {
        return role;
    }
}
'''

FILES["VehicleFleet.java"] = r'''import java.util.AbstractList;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

/**
 * Abstract base class of every kind of vehicle fleet.
 *
 * <p>The attributes and operations supplied in the assignment skeleton are
 * kept unchanged. Operations that differ from one fleet type to another
 * (role names, role prompt, display name, the two abstract operations) are
 * declared abstract so that new fleet types can be added without touching
 * this class or any command class.</p>
 */
public abstract class VehicleFleet {

    private String fleetID;
    private String fleetName;
    private AbstractList drivers;

    public VehicleFleet(String fleetID) {
        this.fleetID = fleetID;
        this.drivers = new Vector();
    }

    public String getFleetID() {
        return fleetID;
    }

    public String getName() {
        return fleetName;
    }

    public void setName(String fleetName) {
        this.fleetName = fleetName;
    }

    public void addDriver(Driver driver) {
        drivers.add(driver);
    }

    public void dropDriver(Driver driver) {
        drivers.remove(driver);
    }

    public AbstractList getDrivers() {
        return drivers;
    }

    /** Re-assigns every driver of this fleet to the first role of the fleet. */
    public abstract void updateDriverRole();

    /** Prints the fleet header followed by the drivers of every role. */
    public abstract void showFleet();

    /**
     * Returns the drivers of the fleet as a typed list so that the rest of
     * the application does not have to work with the raw AbstractList.
     */
    @SuppressWarnings("unchecked")
    public List<Driver> getDriverList() {
        return (List<Driver>) drivers;
    }

    /** Returns the driver with the given id, or null when it is not in this fleet. */
    public Driver findDriver(String driverID) {
        for (Driver driver : getDriverList()) {
            if (driver.getDriverID().equals(driverID)) {
                return driver;
            }
        }
        return null;
    }

    /** Returns true when a driver with the given id belongs to this fleet. */
    public boolean hasDriver(String driverID) {
        return findDriver(driverID) != null;
    }

    /** Text used in front of a fleet line, e.g. "Delivery Van Fleet". */
    public abstract String getFleetTypeDisplayName();

    /** Human readable name of a role code, e.g. "van driver". */
    public abstract String getRoleName(int role);

    /** Prompt shown when the user has to choose a role for this fleet type. */
    public abstract String getRolePrompt();

    /** Prints the one-line form used by "display all fleets". */
    public abstract void showFleetSummary();

    /** One-line header shared by showFleet() and showFleetSummary(). */
    protected String describeHeader() {
        return getFleetTypeDisplayName() + " " + fleetName + " (" + fleetID + ")";
    }

    // ------------------------------------------------------------------
    // Originator operations of the Memento pattern
    // ------------------------------------------------------------------

    /** Captures the current name of this fleet. */
    public Memento createFleetNameMemento() {
        return new FleetNameMemento(fleetID, fleetName);
    }

    /** Restores the fleet name stored in the given memento. */
    public void restoreFleetName(Memento memento) {
        if (memento instanceof FleetNameMemento) {
            FleetNameMemento saved = (FleetNameMemento) memento;
            if (fleetID.equals(saved.getFleetID())) {
                fleetName = saved.getFleetName();
            }
        }
    }

    /** Captures the current role of the given driver. */
    public Memento createDriverRoleMemento(String driverID) {
        Driver driver = findDriver(driverID);
        int role = (driver == null) ? -1 : driver.getRole();
        return new DriverRoleMemento(driverID, role);
    }

    /** Restores the driver role stored in the given memento. */
    public void restoreDriverRole(Memento memento) {
        if (memento instanceof DriverRoleMemento) {
            DriverRoleMemento saved = (DriverRoleMemento) memento;
            Driver driver = findDriver(saved.getDriverID());
            if (driver != null && saved.getRole() >= 0) {
                driver.setRole(saved.getRole());
            }
        }
    }
}
'''

FILES["DeliveryVanFleet.java"] = r'''import java.util.ArrayList;
import java.util.List;

/**
 * Fleet of delivery vans. Roles: 1 = van driver, 2 = courier driver.
 */
public class DeliveryVanFleet extends VehicleFleet {

    private static final int VAN_DRIVER_ROLE = 1;
    private static final int COURIER_DRIVER_ROLE = 2;

    public DeliveryVanFleet(String fleetID) {
        super(fleetID);
    }

    @Override
    public void updateDriverRole() {
        for (Driver driver : getDriverList()) {
            driver.setRole(VAN_DRIVER_ROLE);
        }
    }

    @Override
    public void showFleet() {
        System.out.println(describeHeader());
        printDriversOfRole(VAN_DRIVER_ROLE, "Van Driver:");
        printDriversOfRole(COURIER_DRIVER_ROLE, "Courier Driver:");
    }

    @Override
    public void showFleetSummary() {
        System.out.println(describeHeader());
    }

    @Override
    public String getFleetTypeDisplayName() {
        return "Delivery Van Fleet";
    }

    @Override
    public String getRoleName(int role) {
        switch (role) {
            case VAN_DRIVER_ROLE:
                return "van driver";
            case COURIER_DRIVER_ROLE:
                return "courier driver";
            default:
                return "unknown role";
        }
    }

    @Override
    public String getRolePrompt() {
        return "Role (1 = van driver | 2 = courier driver) :- ";
    }

    /**
     * Prints the drivers that hold the given role. When nobody holds it, the
     * heading is printed together with "NIL".
     */
    private void printDriversOfRole(int role, String heading) {
        List<Driver> matches = new ArrayList<Driver>();
        for (Driver driver : getDriverList()) {
            if (driver.getRole() == role) {
                matches.add(driver);
            }
        }
        if (matches.isEmpty()) {
            System.out.println(heading + " NIL");
            return;
        }
        System.out.println(heading);
        for (Driver driver : matches) {
            System.out.println(driver.getDriverID() + ", " + driver.getName());
        }
    }
}
'''

FILES["RefridgeratedTruckFleet.java"] = r'''import java.util.ArrayList;
import java.util.List;

/**
 * Fleet of refrigerated trucks. Roles: 1 = refrigerated-truck driver,
 * 2 = cold-chain delivery driver.
 *
 * <p>The class name is kept exactly as supplied in the skeleton.</p>
 */
public class RefridgeratedTruckFleet extends VehicleFleet {

    private static final int REFRIDGERATED_TRUCK_DRIVER_ROLE = 1;
    private static final int COLD_CHAIN_DELIVERY_DRIVER_ROLE = 2;

    public RefridgeratedTruckFleet(String fleetID) {
        super(fleetID);
    }

    @Override
    public void updateDriverRole() {
        for (Driver driver : getDriverList()) {
            driver.setRole(REFRIDGERATED_TRUCK_DRIVER_ROLE);
        }
    }

    @Override
    public void showFleet() {
        System.out.println(describeHeader());
        printDriversOfRole(REFRIDGERATED_TRUCK_DRIVER_ROLE, "Refrigerated-truck Driver:");
        printDriversOfRole(COLD_CHAIN_DELIVERY_DRIVER_ROLE, "Cold-chain Delivery Driver:");
    }

    @Override
    public void showFleetSummary() {
        System.out.println(describeHeader());
    }

    @Override
    public String getFleetTypeDisplayName() {
        return "Refrigerated Truck Fleet";
    }

    @Override
    public String getRoleName(int role) {
        switch (role) {
            case REFRIDGERATED_TRUCK_DRIVER_ROLE:
                return "refrigerated-truck driver";
            case COLD_CHAIN_DELIVERY_DRIVER_ROLE:
                return "cold-chain delivery driver";
            default:
                return "unknown role";
        }
    }

    @Override
    public String getRolePrompt() {
        return "Role (1 = refrigerated-truck driver | 2 = cold-chain delivery driver) :- ";
    }

    private void printDriversOfRole(int role, String heading) {
        List<Driver> matches = new ArrayList<Driver>();
        for (Driver driver : getDriverList()) {
            if (driver.getRole() == role) {
                matches.add(driver);
            }
        }
        if (matches.isEmpty()) {
            System.out.println(heading + " NIL");
            return;
        }
        System.out.println(heading);
        for (Driver driver : matches) {
            System.out.println(driver.getDriverID() + ", " + driver.getName());
        }
    }
}
'''

FILES["Command.java"] = r'''/**
 * A command in the sense of the Command pattern.
 *
 * <p>Every user function of SDFMS is represented by one command object,
 * including "undo", "redo" and "show undo/redo lists". Command objects
 * encapsulate the request together with everything needed to carry it out,
 * so the console only has to create the object and execute it.</p>
 */
public interface Command {

    /** Carries out the request, including any interaction with the user. */
    void execute();

    /** Reverses the effect of a previous execution. */
    void undo();

    /** Re-applies the effect after it has been undone. */
    void redo();

    /** Text used in the undo/redo lists and in the undo/redo messages. */
    String getDescription();

    /** Tells the command manager whether this command belongs to the history. */
    boolean isUndoable();
}
'''

FILES["AbstractCommand.java"] = r'''/**
 * Common behaviour shared by all SDFMS commands.
 */
public abstract class AbstractCommand implements Command {

    private final String commandCode;
    private final CommandContext context;

    protected AbstractCommand(String commandCode, CommandContext context) {
        this.commandCode = commandCode;
        this.context = context;
    }

    public String getCommandCode() {
        return commandCode;
    }

    protected CommandContext getContext() {
        return context;
    }

    @Override
    public boolean isUndoable() {
        return true;
    }

    @Override
    public void undo() {
        // Commands that do not change persistent data override nothing.
    }

    @Override
    public void redo() {
        execute();
    }

    @Override
    public String getDescription() {
        return commandCode;
    }
}
'''

FILES["CommandContext.java"] = r'''/**
 * Holds the collaborators that every command needs: the fleet repository,
 * the console input, the command manager (undo/redo history) and the abstract
 * factory used to create fleets and drivers.
 */
public class CommandContext {

    private final FleetRepository repository;
    private final ConsoleInput input;
    private CommandManager commandManager;
    private SDFMSAbstractFactory factory;
    private boolean running = true;

    public CommandContext(FleetRepository repository, ConsoleInput input) {
        this.repository = repository;
        this.input = input;
    }

    public FleetRepository getRepository() {
        return repository;
    }

    public ConsoleInput getInput() {
        return input;
    }

    public CommandManager getCommandManager() {
        return commandManager;
    }

    public void setCommandManager(CommandManager commandManager) {
        this.commandManager = commandManager;
    }

    public SDFMSAbstractFactory getFactory() {
        return factory;
    }

    public void setFactory(SDFMSAbstractFactory factory) {
        this.factory = factory;
    }

    public boolean isRunning() {
        return running;
    }

    public void setRunning(boolean running) {
        this.running = running;
    }

    /**
     * Returns the current fleet or prints an error and returns null when no
     * fleet has been set yet.
     */
    public VehicleFleet getCurrentFleetOrReport() {
        VehicleFleet current = repository.getCurrentFleet();
        if (current == null) {
            System.out.println("No current fleet is set!");
        }
        return current;
    }
}
'''

FILES["CommandManager.java"] = r'''import java.util.List;
import java.util.Vector;

/**
 * Invoker of the Command pattern. It executes commands and keeps the two
 * history lists used by Undo and Redo.
 */
public class CommandManager {

    private final Vector<Command> undoList = new Vector<Command>();
    private final Vector<Command> redoList = new Vector<Command>();

    /** Executes a command and records it when it is an undoable command. */
    public void execute(Command command) {
        command.execute();
        if (command.isUndoable()) {
            undoList.add(command);
            redoList.clear();
        }
    }

    /** Undoes the most recent undoable command. */
    public void undo() {
        if (undoList.isEmpty()) {
            System.out.println("No command can be undone.");
            return;
        }
        Command command = undoList.remove(undoList.size() - 1);
        command.undo();
        redoList.add(command);
        System.out.println("Command (" + command.getDescription() + ") is undone.");
    }

    /** Redoes the most recently undone command. */
    public void redo() {
        if (redoList.isEmpty()) {
            System.out.println("No command can be redone.");
            return;
        }
        Command command = redoList.remove(redoList.size() - 1);
        command.redo();
        undoList.add(command);
        System.out.println("Command (" + command.getDescription() + ") is redone.");
    }

    /** Prints both history lists, oldest entry first. */
    public void showLists() {
        System.out.println("Undo List");
        for (Command command : undoList) {
            System.out.println(command.getDescription());
        }
        System.out.println("-- End of undo list --");
        System.out.println("Redo List");
        for (Command command : redoList) {
            System.out.println(command.getDescription());
        }
        System.out.println("-- End of redo list --");
    }

    public List<Command> getUndoList() {
        return undoList;
    }

    public List<Command> getRedoList() {
        return redoList;
    }
}
'''

FILES["FleetRepository.java"] = r'''import java.util.List;
import java.util.Vector;

/**
 * In-memory store of all fleet records together with the current fleet.
 */
public class FleetRepository {

    private final Vector<VehicleFleet> fleets = new Vector<VehicleFleet>();
    private VehicleFleet currentFleet;

    public List<VehicleFleet> getFleets() {
        return fleets;
    }

    public VehicleFleet findFleet(String fleetID) {
        for (VehicleFleet fleet : fleets) {
            if (fleet.getFleetID().equals(fleetID)) {
                return fleet;
            }
        }
        return null;
    }

    public boolean containsFleet(String fleetID) {
        return findFleet(fleetID) != null;
    }

    public void addFleet(VehicleFleet fleet) {
        fleets.add(fleet);
    }

    /** Removes a fleet; the current fleet is cleared when it was that fleet. */
    public void removeFleet(VehicleFleet fleet) {
        fleets.remove(fleet);
        if (currentFleet == fleet) {
            currentFleet = null;
        }
    }

    public VehicleFleet getCurrentFleet() {
        return currentFleet;
    }

    public void setCurrentFleet(VehicleFleet currentFleet) {
        this.currentFleet = currentFleet;
    }

    public boolean isEmpty() {
        return fleets.isEmpty();
    }
}
'''

FILES["ConsoleInput.java"] = r'''import java.util.Scanner;

/**
 * Thin wrapper around Scanner that prints the prompt before reading a line.
 * A null is returned when the input stream has no more lines.
 */
public class ConsoleInput {

    private final Scanner scanner;

    public ConsoleInput(Scanner scanner) {
        this.scanner = scanner;
    }

    /** Prints a prompt and returns the next input line, or null at end of input. */
    public String readLine(String prompt) {
        System.out.print(prompt);
        if (!scanner.hasNextLine()) {
            return null;
        }
        return scanner.nextLine().trim();
    }

    /** Prints a prompt and returns the next input line as a role code, or -1. */
    public int readRole(String prompt) {
        String line = readLine(prompt);
        if (line == null) {
            return -1;
        }
        try {
            return Integer.parseInt(line.trim());
        } catch (NumberFormatException ex) {
            return -1;
        }
    }

    /**
     * Reads a line of the form "id, name" and returns a two element array,
     * or null when the line cannot be split into exactly two parts.
     */
    public String[] readDriverInformation() {
        String line = readLine("Please input driver information (id, name):- ");
        if (line == null) {
            return null;
        }
        String[] parts = line.split(",", 2);
        if (parts.length < 2) {
            return null;
        }
        String id = parts[0].trim();
        String name = parts[1].trim();
        if (id.isEmpty() || name.isEmpty()) {
            return null;
        }
        return new String[] {id, name};
    }
}
'''

FILES["FleetFactory.java"] = r'''/**
 * Factory that creates one kind of vehicle fleet.
 *
 * <p>A new fleet type is supported by adding one implementation of this
 * interface and registering it in the registry; no existing class has to be
 * changed, which is the Open-Closed Principle in practice.</p>
 */
public interface FleetFactory {

    /** Single character code typed by the user, e.g. "v". */
    String getTypeCode();

    /** Lower case description used in messages and undo entries. */
    String getTypeLabel();

    /** Creates an empty fleet with the given fleet id. */
    VehicleFleet createFleet(String fleetID);
}
'''

FILES["DeliveryVanFleetFactory.java"] = r'''/** Creates delivery van fleets. */
public class DeliveryVanFleetFactory implements FleetFactory {

    @Override
    public String getTypeCode() {
        return "v";
    }

    @Override
    public String getTypeLabel() {
        return "delivery van fleet";
    }

    @Override
    public VehicleFleet createFleet(String fleetID) {
        return new DeliveryVanFleet(fleetID);
    }
}
'''

FILES["RefridgeratedTruckFleetFactory.java"] = r'''/** Creates refrigerated truck fleets. */
public class RefridgeratedTruckFleetFactory implements FleetFactory {

    @Override
    public String getTypeCode() {
        return "r";
    }

    @Override
    public String getTypeLabel() {
        return "refrigerated truck fleet";
    }

    @Override
    public VehicleFleet createFleet(String fleetID) {
        return new RefridgeratedTruckFleet(fleetID);
    }
}
'''

FILES["FleetFactoryRegistry.java"] = r'''import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Registry of the fleet factories that are currently supported. The console
 * never refers to a concrete fleet class, only to a factory found here.
 */
public class FleetFactoryRegistry {

    private final Map<String, FleetFactory> factories = new LinkedHashMap<String, FleetFactory>();

    /** Registers the fleet types that SDFMS supports out of the box. */
    public static FleetFactoryRegistry createDefault() {
        FleetFactoryRegistry registry = new FleetFactoryRegistry();
        registry.register(new DeliveryVanFleetFactory());
        registry.register(new RefridgeratedTruckFleetFactory());
        return registry;
    }

    public void register(FleetFactory factory) {
        factories.put(factory.getTypeCode(), factory);
    }

    public FleetFactory getFactory(String typeCode) {
        if (typeCode == null) {
            return null;
        }
        return factories.get(typeCode.trim().toLowerCase());
    }

    public boolean isSupported(String typeCode) {
        return getFactory(typeCode) != null;
    }
}
'''

FILES["DriverFactory.java"] = r'''/**
 * Factory that creates driver objects. Keeping driver creation behind a
 * factory allows the representation of a driver to change without touching
 * the commands.
 */
public interface DriverFactory {

    Driver createDriver(String driverID, String driverName, int role);
}
'''

FILES["StandardDriverFactory.java"] = r'''/** Creates the standard Driver objects used by SDFMS. */
public class StandardDriverFactory implements DriverFactory {

    @Override
    public Driver createDriver(String driverID, String driverName, int role) {
        return new Driver(driverID, driverName, role);
    }
}
'''

FILES["CommandFactory.java"] = r'''/**
 * Factory that turns a command code typed by the user into a Command object.
 */
public interface CommandFactory {

    /** Returns the command for the code, or null when the code is unknown. */
    Command createCommand(String commandCode);
}
'''

FILES["SDFMSCommandFactory.java"] = r'''/**
 * Creates every command object of SDFMS. Adding a new user function means
 * adding one command class and one line here.
 */
public class SDFMSCommandFactory implements CommandFactory {

    private final CommandContext context;

    public SDFMSCommandFactory(CommandContext context) {
        this.context = context;
    }

    @Override
    public Command createCommand(String commandCode) {
        if (commandCode == null) {
            return null;
        }
        String code = commandCode.trim().toLowerCase();
        switch (code) {
            case "c":
                return new CreateFleetCommand(context);
            case "s":
                return new SetCurrentFleetCommand(context);
            case "a":
                return new AddDriverCommand(context);
            case "m":
                return new ModifyDriverRoleCommand(context);
            case "d":
                return new DeleteDriverCommand(context);
            case "sf":
                return new ShowFleetCommand(context);
            case "sa":
                return new DisplayAllFleetsCommand(context);
            case "cn":
                return new ChangeFleetNameCommand(context);
            case "u":
                return new UndoCommand(context);
            case "r":
                return new RedoCommand(context);
            case "l":
                return new ShowUndoRedoListCommand(context);
            case "x":
                return new ExitCommand(context);
            default:
                return null;
        }
    }
}
'''

FILES["SDFMSAbstractFactory.java"] = r'''/**
 * Abstract factory of the application. It gives access to the three families
 * of objects SDFMS needs: fleet objects, driver objects and command objects.
 */
public interface SDFMSAbstractFactory {

    VehicleFleet createFleet(String fleetTypeCode, String fleetID);

    Driver createDriver(String driverID, String driverName, int role);

    Command createCommand(String commandCode);

    boolean isValidFleetType(String fleetTypeCode);

    String getFleetTypeLabel(String fleetTypeCode);
}
'''

FILES["SDFMSFactory.java"] = r'''/**
 * Concrete abstract factory. Fleet creation is delegated to the registered
 * FleetFactory of the requested type, driver creation to a DriverFactory and
 * command creation to a CommandFactory.
 */
public class SDFMSFactory implements SDFMSAbstractFactory {

    private final FleetFactoryRegistry fleetFactories;
    private final DriverFactory driverFactory;
    private final CommandFactory commandFactory;

    public SDFMSFactory(CommandContext context) {
        this(context, FleetFactoryRegistry.createDefault(), new StandardDriverFactory());
    }

    public SDFMSFactory(CommandContext context, FleetFactoryRegistry fleetFactories,
            DriverFactory driverFactory) {
        this.fleetFactories = fleetFactories;
        this.driverFactory = driverFactory;
        this.commandFactory = new SDFMSCommandFactory(context);
    }

    @Override
    public VehicleFleet createFleet(String fleetTypeCode, String fleetID) {
        FleetFactory factory = fleetFactories.getFactory(fleetTypeCode);
        if (factory == null) {
            throw new IllegalArgumentException("Unsupported fleet type: " + fleetTypeCode);
        }
        return factory.createFleet(fleetID);
    }

    @Override
    public Driver createDriver(String driverID, String driverName, int role) {
        return driverFactory.createDriver(driverID, driverName, role);
    }

    @Override
    public Command createCommand(String commandCode) {
        return commandFactory.createCommand(commandCode);
    }

    @Override
    public boolean isValidFleetType(String fleetTypeCode) {
        return fleetFactories.isSupported(fleetTypeCode);
    }

    @Override
    public String getFleetTypeLabel(String fleetTypeCode) {
        FleetFactory factory = fleetFactories.getFactory(fleetTypeCode);
        return (factory == null) ? "unknown fleet" : factory.getTypeLabel();
    }
}
'''

FILES["CreateFleetCommand.java"] = r'''/**
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
'''

FILES["SetCurrentFleetCommand.java"] = r'''/**
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
'''

FILES["AddDriverCommand.java"] = r'''/**
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
'''

FILES["ModifyDriverRoleCommand.java"] = r'''/**
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
'''

FILES["DeleteDriverCommand.java"] = r'''/**
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
'''

FILES["ChangeFleetNameCommand.java"] = r'''/**
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
'''

FILES["ShowFleetCommand.java"] = r'''/** "Show the current fleet" command. */
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
'''

FILES["DisplayAllFleetsCommand.java"] = r'''/** "Display all fleets" command. */
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
'''

FILES["UndoCommand.java"] = r'''/**
 * "Undo the last command" command. Undo is itself a command object, so the
 * console treats it exactly like every other function.
 */
public class UndoCommand extends AbstractCommand {

    public UndoCommand(CommandContext context) {
        super("u", context);
    }

    @Override
    public void execute() {
        getContext().getCommandManager().undo();
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Undo";
    }
}
'''

FILES["RedoCommand.java"] = r'''/** "Redo the last undone command" command. */
public class RedoCommand extends AbstractCommand {

    public RedoCommand(CommandContext context) {
        super("r", context);
    }

    @Override
    public void execute() {
        getContext().getCommandManager().redo();
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Redo";
    }
}
'''

FILES["ShowUndoRedoListCommand.java"] = r'''/** "Show the undo/redo lists" command. */
public class ShowUndoRedoListCommand extends AbstractCommand {

    public ShowUndoRedoListCommand(CommandContext context) {
        super("l", context);
    }

    @Override
    public void execute() {
        getContext().getCommandManager().showLists();
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Show undo/redo lists";
    }
}
'''

FILES["ExitCommand.java"] = r'''/** "Exit the system" command. */
public class ExitCommand extends AbstractCommand {

    public ExitCommand(CommandContext context) {
        super("x", context);
    }

    @Override
    public void execute() {
        System.out.println("Thank you for using SDFMS. System terminated.");
        getContext().setRunning(false);
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Exit system";
    }
}
'''

FILES["SDFMSApplication.java"] = r'''/**
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
'''

FILES["Main.java"] = r'''import java.util.Scanner;

/**
 * Entry point of SDFMS. It wires the console, the repository, the command
 * manager and the abstract factory together and starts the application.
 */
public class Main {

    public static void main(String[] args) {
        FleetRepository repository = new FleetRepository();
        ConsoleInput input = new ConsoleInput(new Scanner(System.in));
        CommandContext context = new CommandContext(repository, input);
        context.setCommandManager(new CommandManager());
        context.setFactory(new SDFMSFactory(context));
        new SDFMSApplication(context).run();
    }
}
'''

for name, content in FILES.items():
    (SRC / name).write_text(content, encoding="utf-8", newline="\n")

(SRC / "run.bat").write_text(
    "@echo off\r\n"
    "javac *.java\r\n"
    "if errorlevel 1 goto end\r\n"
    "java Main\r\n"
    ":end\r\n",
    encoding="utf-8", newline="")

print("written", len(FILES), "java files")
