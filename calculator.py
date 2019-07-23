"""
Neima Schafi - Lesson04 Assignment
"""
from functools import reduce
import operator

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum_all = "0"

    try:
        total = sum(map(int, args))
        sum_all = str(total)
    except (ValueError, TypeError , IndexError):
        print("Unable to calculate sum due to possible non-integer or no integers provided")
    return sum_all

def subtract(*args):
    """ Returns a STRING with the results of subtracting the arguments """
    results = "0"
    try:
        args = list(map(int, args))
        total = args[0] - sum(args[1:])
        results = str(total)
    except (ValueError, TypeError):
        print("Unable to calculate sum due to possible non-integer")
    return results

def multiply(*args):
    """ Returns a STRING with the result of multiplying the arguments """
    results = "0"
    try:
        args = list(map(int, args))
        total = reduce(operator.mul, args, 1)
        results = str(total)
    except (ValueError, TypeError , IndexError):
        print("Unable to calculate sum due to possible non-integer or no integers provided")
    return results

def divide(*args):
    """ Returns a STRING with the result of dividing the arguments """
    results = "0"

    try:
        args = list(map(int, args))
        total = reduce(operator.truediv, args)
        results = str(total)
    except (ValueError, TypeError, IndexError):
        print("Unable to calculate sum due to possible non-integer or no integers provided")
    except ZeroDivisionError as e:
        return "Error - You divided by 0, try again."
    return results

def homepage():
    """ Home page for calculations. Home page explains how to perfrom calculations """
    # I should also be able to see a home page (http://localhost:8080/)
    # that explains how to perform calculations.
    body = """<html>
            <head>
            <title>WSGI calculator</title>
            </head>
            <body>
            <p> Welcome to the WSGI calculator page!!</p>
            <p> Using the WSGI calculator you can add, subtract, multiply, or divide two (or more) numbers.</p>
            <p>
            You can use the calculator by appending any of the mentioned actions (add, subtract, multiply, or divide two numbers)
            to http://localhost:8080/ as such: http://localhost:8080/multiply/3/5 => 15
            </p>
            </html>"""
    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {'': homepage, 'add': add, 'subtract': subtract,
            'multiply': multiply, 'divide': divide,}
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

    start_response(status, headers)
    return ["<h1>No Progress Yet</h1>".encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
