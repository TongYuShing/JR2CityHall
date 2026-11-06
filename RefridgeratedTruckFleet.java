import java.util.Iterator;

public class RefridgeratedTruckFleet extends VehicleFleet {
    private final int REFRIDGERATED_TRUCK_DRIVER_ROLE = 1;
    private final int COLD_CHAIN_DELIVERY_DRIVER_ROLE = 2;
    
    public RefridgeratedTruckFleet(String fleetID) {
        super(fleetID);
    }
    
    @Override
    public void updateDriverRole() {
        Iterator<Driver> iterator = getDrivers().iterator();
        while (iterator.hasNext()) {
            Driver driver = iterator.next();
            driver.setRole(REFRIDGERATED_TRUCK_DRIVER_ROLE);
        }
    }
    
    @Override
    public void showFleet() {
        System.out.println("Refrigerated Truck Fleet " + getName() + " (" + getFleetID() + ")");
        printRole(1, "Refrigerated-truck Driver:");
        printRole(2, "Cold-chain Delivery Driver:");
    }

    private void printRole(int role, String heading) {
        boolean found = false;
        Iterator<Driver> iterator = getDrivers().iterator();
        while (iterator.hasNext()) {
            if (iterator.next().getRole() == role) {
                found = true;
                break;
            }
        }
        if (!found) {
            System.out.println(heading + " NIL");
            return;
        }
        System.out.println(heading);
        iterator = getDrivers().iterator();
        while (iterator.hasNext()) {
            Driver driver = iterator.next();
            if (driver.getRole() == role) {
                System.out.println(driver.getDriverID() + ", " + driver.getName());
            }
        }
    }
}
