/** "Exit the system" command. */
public class ExitCommand extends AbstractCommand {

    public ExitCommand(CommandContext context) {
        super("x", context);
    }

    @Override
    public void execute() {
        System.out.println("Thank you for using SDFMS. System terminated.");
        getContext().setRunning(false);
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Exit system";
    }
}
