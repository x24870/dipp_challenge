"""
System file to manage the utility commands
"""
from flask import current_app
from flask_script import Shell, Manager

from app.app import create_app
from urllib.parse import unquote


def _create_manager_obj(application):
    """
    Method to create one manager object
    """
    manager_obj = Manager(application, with_default_commands=False)
    manager_obj.add_command("shell", Shell)

    return manager_obj


flask_app = create_app()
manager = _create_manager_obj(flask_app)


@manager.command
def run():
    """
    Runs the api server
    """
    port = int(current_app.config["PORT"])
    host = current_app.config["HOST"]
    debug = current_app.config["DEBUG"]

    current_app.run(host=host, port=port, debug=debug)


@manager.command
def routes():
    """
    List all url routes
    """
    output = []
    print(unquote("{:40s} {:12s} {}".format("Name", "Method", "Path")))  # header

    for rule in flask_app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = f"[{arg}]"

        methods = ", ".join(
            [i for i in rule.methods if i not in ("HEAD", "OPTIONS")],  # filter out head and options
        )

        if rule.endpoint != "static":
            url = "%s" % rule
            output.append({"endpoint": rule.endpoint, "methods": methods, "url": url})

    for line in sorted(output, key=lambda l: l["url"]):
        line = unquote("{:40s} {:12s} {}".format(line["endpoint"], line["methods"], line["url"]))
        print(line)


if __name__ == "__main__":
    manager.run()
