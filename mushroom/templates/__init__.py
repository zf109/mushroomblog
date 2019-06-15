import jinja2

templateEnv = jinja2.Environment(loader=jinja2.PackageLoader('mushroom', 'templates'))


def get_template(filename):
    return templateEnv.get_template(filename)


def render(filename, *args, **kwargs):
    return templateEnv.get_template(filename).render(*args, **kwargs)
