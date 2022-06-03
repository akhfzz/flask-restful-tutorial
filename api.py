from pkgutil import iter_modules
import system
import config
import models

root = config.app.root
res = config.app.resources

print(f'Loading list of modules...')
modules = [name for _, name, _ in iter_modules([res])]
print('done.\n')

for module in modules:
    print(f'Loading module {module}...')
    exec(f'from {res} import {module}')
    cfg = eval(f'{module}.config')
    
    print(f'  Loading routes of module {module}...')
    routes = cfg['routes']
    for route in routes:
        urls = ['/' + module + route]
        if root == module and not route:
            urls.append('/')
        system.api.add_resource(routes[route], *urls)
    print(f'  {len(routes)} route(s) loaded.')

    print('done.\n')

if __name__ == '__main__':
    system.app.run(debug=True)
    # models.db.create_all()