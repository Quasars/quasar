import sys
import argparse

try:
    import win32com.client
except ImportError:
    pass


def create_shortcut(
        path: str, target: str, arguments="", icon="", window_style=None,
        working_directory=None,
):
    shell = win32com.client.Dispatch("WScript.Shell")
    sh = shell.CreateShortcut(path)
    sh.TargetPath = target
    if arguments:
        sh.Arguments = arguments
    if icon:
        sh.IconLocation = icon
    if window_style is not None:
        sh.WindowStyle = window_style
    if working_directory is not None:
        sh.WorkingDirectory = working_directory
    sh.save()


def main(argv):
    WindowStyles = {"normal": 1, "maximized": 3, "minimized": 7}
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shortcut", help="Shortcut location/path")
    parser.add_argument("-t", "--target", help="Shortcut target")
    parser.add_argument("-a", "--arguments", help="Shortcut arguments", default="")
    parser.add_argument("-i", "--icon", help="Shortcut icon", default="")
    parser.add_argument("-n", "--window-style", help="Window style (Normal, Minimized, Maximized)",
                        default="Normal", type=lambda v:  WindowStyles[v.lower()])
    parser.add_argument("-w", "--working-directory", help="Working directory", default=None)

    opts = parser.parse_args(argv[1:])
    create_shortcut(
        opts.shortcut,
        opts.target,
        opts.arguments,
        opts.icon,
        opts.window_style,
        opts.working_directory,
    )
    return 0


if __name__ == "__main__":
    main(sys.argv)
