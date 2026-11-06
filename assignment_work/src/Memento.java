/**
 * Marker interface for all memento objects used by the undo mechanism.
 *
 * <p>A memento is an opaque snapshot of the state of an originator. Only the
 * originator that created it knows how to interpret it, which keeps the
 * command objects independent of the internal structure of the fleet.</p>
 */
public interface Memento {
}
