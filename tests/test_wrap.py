from pyqgraf.wrap import dewrap_all, dewrap_model, wrap_model


def test_wrap():
    test = " [ e_plus, e_minus, + ] "
    print(wrap_model(test))
    print(dewrap_model(wrap_model(test)[0]))


def test_dewrap_all():
    test = " [ e_plus, e_minus, + ] "
    print(wrap_model(test))
    print(dewrap_all(wrap_model(test)[0]))
