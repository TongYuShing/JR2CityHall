import java.util.AbstractList;
import java.util.ArrayList;

public abstract class VehicleFleet {
    private String fleetID;
    private String fleetName;
    private AbstractList drivers;

    public VehicleFleet(String fleetID) {
        this.fleetID = fleetID;
        this.drivers = new ArrayList();
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

    public abstract void updateDriverRole();
    public abstract void showFleet();
}
