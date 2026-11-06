/**
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
