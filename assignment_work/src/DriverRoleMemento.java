/**
 * Memento that stores the role of a driver before it is modified.
 */
public class DriverRoleMemento implements Memento {

    private final String driverID;
    private final int role;

    public DriverRoleMemento(String driverID, int role) {
        this.driverID = driverID;
        this.role = role;
    }

    public String getDriverID() {
        return driverID;
    }

    public int getRole() {
        return role;
    }
}
