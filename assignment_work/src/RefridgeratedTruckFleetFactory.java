/** Creates refrigerated truck fleets. */
public class RefridgeratedTruckFleetFactory implements FleetFactory {

    @Override
    public String getTypeCode() {
        return "r";
    }

    @Override
    public String getTypeLabel() {
        return "refrigerated truck fleet";
    }

    @Override
    public VehicleFleet createFleet(String fleetID) {
        return new RefridgeratedTruckFleet(fleetID);
    }
}
