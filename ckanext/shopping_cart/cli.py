import click


@click.group(short_help="shopping_cart CLI.")
def shopping_cart():
    """shopping_cart CLI."""
    pass


@shopping_cart.command()
@click.argument("name", default="shopping_cart")
def command(name):
    """Docs."""
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [shopping_cart]
