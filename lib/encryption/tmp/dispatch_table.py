def _m_handler(a, b):
    print(a + b)


def _c_handler(a, b):
    print(a + b)


def _s_handler(a, b):
    print(a + b)


def _u_handler(a, b):
    print(a + b)


def _f_handler(a, b, c=None):
    print(a + b)


def _x_handler(a, b):
    print(a + b)


def _w_handler(a, b):
    print(a + b)


def _c_handler(a, b):
    print(a + b)


def _t_handler(a, b):
    print(a + b)


def _k_handler(a, b):
    print(a + b)


def _error_handler(*args):
    raise RuntimeError('unknown message type.')


dispatch_router = {
    'M': _m_handler,
    'C': _c_handler,
    'S': _s_handler,
    'U': _u_handler,
    'F': _f_handler,
    'X': _x_handler,
    'W': _w_handler,
    'T': _t_handler,
    'K': _k_handler
}

type = 'J'

dispatch_router.get(type, _error_handler)(1, 2)
