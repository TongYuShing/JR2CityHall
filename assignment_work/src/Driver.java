/**
 * A driver that can be assigned to a vehicle fleet.
 *
 * <p>The attributes and operations of this class are those supplied in the
 * assignment skeleton; only documentation has been added.</p>
 */
public class Driver {

    private String driverID;
    private String driverName;
    private int role;

    /**
     * Creates a driver.
     *
     * @param driverID   unique driver identifier, e.g. "d001"
     * @param driverName driver name, e.g. "Alex Chan"
     * @param role       role code inside the fleet (1 or 2, meaning depends on
     *                   the type of fleet the driver belongs to)
     */
    public Driver(String driverID, String driverName, int role) {
        this.driverID = driverID;
        this.driverName = driverName;
        this.role = role;
    }

    public String getDriverID() {
        return driverID;
    }

    public String getName() {
        return driverName;
    }

    public int getRole() {
        return role;
    }

    public void setName(String driverName) {
        this.driverName = driverName;
    }

    public void setRole(int role) {
        this.role = role;
    }
}
