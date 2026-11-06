/**
 * Memento that stores the name of a fleet before it is changed.
 */
public class FleetNameMemento implements Memento {

    private final String fleetID;
    private final String fleetName;

    public FleetNameMemento(String fleetID, String fleetName) {
        this.fleetID = fleetID;
        this.fleetName = fleetName;
    }

    public String getFleetID() {
        return fleetID;
    }

    public String getFleetName() {
        return fleetName;
    }
}
