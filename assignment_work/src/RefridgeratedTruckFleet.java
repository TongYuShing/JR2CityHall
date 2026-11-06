import java.util.ArrayList;
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
