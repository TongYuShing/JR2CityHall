/** Creates delivery van fleets. */
public class DeliveryVanFleetFactory implements FleetFactory {

    @Override
    public String getTypeCode() {
        return "v";
    }

    @Override
    public String getTypeLabel() {
        return "delivery van fleet";
    }

    @Override
    public VehicleFleet createFleet(String fleetID) {
        return new DeliveryVanFleet(fleetID);
    }
}
