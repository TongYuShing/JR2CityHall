/**
 * Creates every command object of SDFMS. Adding a new user function means
 * adding one command class and one line here.
 */
public class SDFMSCommandFactory implements CommandFactory {

    private final CommandContext context;

    public SDFMSCommandFactory(CommandContext context) {
        this.context = context;
    }

    @Override
    public Command createCommand(String commandCode) {
        if (commandCode == null) {
            return null;
        }
        String code = commandCode.trim().toLowerCase();
        switch (code) {
            case "c":
                return new CreateFleetCommand(context);
            case "s":
                return new SetCurrentFleetCommand(context);
            case "a":
                return new AddDriverCommand(context);
            case "m":
                return new ModifyDriverRoleCommand(context);
            case "d":
                return new DeleteDriverCommand(context);
            case "sf":
                return new ShowFleetCommand(context);
            case "sa":
                return new DisplayAllFleetsCommand(context);
            case "cn":
                return new ChangeFleetNameCommand(context);
            case "u":
                return new UndoCommand(context);
            case "r":
                return new RedoCommand(context);
            case "l":
                return new ShowUndoRedoListCommand(context);
            case "x":
                return new ExitCommand(context);
            default:
                return null;
        }
    }
}
