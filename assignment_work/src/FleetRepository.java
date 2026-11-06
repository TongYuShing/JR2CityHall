import java.util.List;
import java.util.Vector;

/**
 * In-memory store of all fleet records together with the current fleet.
 */
public class FleetRepository {

    private final Vector<VehicleFleet> fleets = new Vector<VehicleFleet>();
    private VehicleFleet currentFleet;

    public List<VehicleFleet> getFleets() {
        return fleets;
    }

    public VehicleFleet findFleet(String fleetID) {
        for (VehicleFleet fleet : fleets) {
            if (fleet.getFleetID().equals(fleetID)) {
                return fleet;
            }
        }
        return null;
    }

    public boolean containsFleet(String fleetID) {
        return findFleet(fleetID) != null;
    }

    public void addFleet(VehicleFleet fleet) {
        fleets.add(fleet);
    }

    /** Removes a fleet; the current fleet is cleared when it was that fleet. */
    public void removeFleet(VehicleFleet fleet) {
        fleets.remove(fleet);
        if (currentFleet == fleet) {
            currentFleet = null;
        }
    }

    public VehicleFleet getCurrentFleet() {
        return currentFleet;
    }

    public void setCurrentFleet(VehicleFleet currentFleet) {
        this.currentFleet = currentFleet;
    }

    public boolean isEmpty() {
        return fleets.isEmpty();
    }
}
