import java.util.Iterator;

public class DeliveryVanFleet extends VehicleFleet {
    private final int VAN_DRIVER_ROLE = 1;
    private final int COURIER_DRIVER_ROLE = 2;
    
    public DeliveryVanFleet(String fleetID) {
        super(fleetID);
    }
    
    @Override
    public void updateDriverRole() {
        Iterator<Driver> iterator = getDrivers().iterator();
        while (iterator.hasNext()) {
            Driver driver = iterator.next();
            driver.setRole(VAN_DRIVER_ROLE);
        }
    }
    
    @Override
    public void showFleet() {
        System.out.println("Delivery Van Fleet " + getName() + " (" + getFleetID() + ")");
        printRole(1, "Van Driver:");
        printRole(2, "Courier Driver:");
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
