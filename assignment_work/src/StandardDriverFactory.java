/** Creates the standard Driver objects used by SDFMS. */
public class StandardDriverFactory implements DriverFactory {

    @Override
    public Driver createDriver(String driverID, String driverName, int role) {
        return new Driver(driverID, driverName, role);
    }
}
