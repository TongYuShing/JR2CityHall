import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Registry of the fleet factories that are currently supported. The console
 * never refers to a concrete fleet class, only to a factory found here.
 */
public class FleetFactoryRegistry {

    private final Map<String, FleetFactory> factories = new LinkedHashMap<String, FleetFactory>();

    /** Registers the fleet types that SDFMS supports out of the box. */
    public static FleetFactoryRegistry createDefault() {
        FleetFactoryRegistry registry = new FleetFactoryRegistry();
        registry.register(new DeliveryVanFleetFactory());
        registry.register(new RefridgeratedTruckFleetFactory());
        return registry;
    }

    public void register(FleetFactory factory) {
        factories.put(factory.getTypeCode(), factory);
    }

    public FleetFactory getFactory(String typeCode) {
        if (typeCode == null) {
            return null;
        }
        return factories.get(typeCode.trim().toLowerCase());
    }

    public boolean isSupported(String typeCode) {
        return getFactory(typeCode) != null;
    }
}
