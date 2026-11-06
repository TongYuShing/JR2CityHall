import java.util.AbstractList;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

/**
 * Abstract base class of every kind of vehicle fleet.
 *
 * <p>The attributes and operations supplied in the assignment skeleton are
 * kept unchanged. Operations that differ from one fleet type to another
 * (role names, role prompt, display name, the two abstract operations) are
 * declared abstract so that new fleet types can be added without touching
 * this class or any command class.</p>
 */
public abstract class VehicleFleet {

    private String fleetID;
    private String fleetName;
    private AbstractList drivers;

    public VehicleFleet(String fleetID) {
        this.fleetID = fleetID;
        this.drivers = new Vector();
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

    /** Re-assigns every driver of this fleet to the first role of the fleet. */
    public abstract void updateDriverRole();

    /** Prints the fleet header followed by the drivers of every role. */
    public abstract void showFleet();

    /**
     * Returns the drivers of the fleet as a typed list so that the rest of
     * the application does not have to work with the raw AbstractList.
     */
    @SuppressWarnings("unchecked")
    public List<Driver> getDriverList() {
        return (List<Driver>) drivers;
    }

    /** Returns the driver with the given id, or null when it is not in this fleet. */
    public Driver findDriver(String driverID) {
        for (Driver driver : getDriverList()) {
            if (driver.getDriverID().equals(driverID)) {
                return driver;
            }
        }
        return null;
    }

    /** Returns true when a driver with the given id belongs to this fleet. */
    public boolean hasDriver(String driverID) {
        return findDriver(driverID) != null;
    }

    /** Text used in front of a fleet line, e.g. "Delivery Van Fleet". */
    public abstract String getFleetTypeDisplayName();

    /** Human readable name of a role code, e.g. "van driver". */
    public abstract String getRoleName(int role);

    /** Prompt shown when the user has to choose a role for this fleet type. */
    public abstract String getRolePrompt();

    /** Prints the one-line form used by "display all fleets". */
    public abstract void showFleetSummary();

    /** One-line header shared by showFleet() and showFleetSummary(). */
    protected String describeHeader() {
        return getFleetTypeDisplayName() + " " + fleetName + " (" + fleetID + ")";
    }

    // ------------------------------------------------------------------
    // Originator operations of the Memento pattern
    // ------------------------------------------------------------------

    /** Captures the current name of this fleet. */
    public Memento createFleetNameMemento() {
        return new FleetNameMemento(fleetID, fleetName);
    }

    /** Restores the fleet name stored in the given memento. */
    public void restoreFleetName(Memento memento) {
        if (memento instanceof FleetNameMemento) {
            FleetNameMemento saved = (FleetNameMemento) memento;
            if (fleetID.equals(saved.getFleetID())) {
                fleetName = saved.getFleetName();
            }
        }
    }

    /** Captures the current role of the given driver. */
    public Memento createDriverRoleMemento(String driverID) {
        Driver driver = findDriver(driverID);
        int role = (driver == null) ? -1 : driver.getRole();
        return new DriverRoleMemento(driverID, role);
    }

    /** Restores the driver role stored in the given memento. */
    public void restoreDriverRole(Memento memento) {
        if (memento instanceof DriverRoleMemento) {
            DriverRoleMemento saved = (DriverRoleMemento) memento;
            Driver driver = findDriver(saved.getDriverID());
            if (driver != null && saved.getRole() >= 0) {
                driver.setRole(saved.getRole());
            }
        }
    }
}
