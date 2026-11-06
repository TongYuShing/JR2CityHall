/**
 * Factory that creates one kind of vehicle fleet.
 *
 * <p>A new fleet type is supported by adding one implementation of this
 * interface and registering it in the registry; no existing class has to be
 * changed, which is the Open-Closed Principle in practice.</p>
 */
public interface FleetFactory {

    /** Single character code typed by the user, e.g. "v". */
    String getTypeCode();

    /** Lower case description used in messages and undo entries. */
    String getTypeLabel();

    /** Creates an empty fleet with the given fleet id. */
    VehicleFleet createFleet(String fleetID);
}
