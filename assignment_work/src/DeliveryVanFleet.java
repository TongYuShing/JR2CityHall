import java.util.ArrayList;
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
