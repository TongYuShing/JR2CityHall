/**
 * Factory that creates driver objects. Keeping driver creation behind a
 * factory allows the representation of a driver to change without touching
 * the commands.
 */
public interface DriverFactory {

    Driver createDriver(String driverID, String driverName, int role);
}
