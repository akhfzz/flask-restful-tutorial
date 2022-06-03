from flask_restful import abort

def abort_no_data(id, data):
    if not data:
        abort(404, f"Data with id {id} doesn't exist")

def abort_no_arg(arg, args):
    if not args[arg]:
        abort(400, message=f"Data '{arg}' isn't supplied")