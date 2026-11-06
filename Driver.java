public class Driver {
    private String driverID;
    private String driverName;
    private int role;
    
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
