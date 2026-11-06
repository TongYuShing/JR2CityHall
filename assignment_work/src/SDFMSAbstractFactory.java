/**
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
