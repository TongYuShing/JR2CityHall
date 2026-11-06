/**
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
