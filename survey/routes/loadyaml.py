# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request

def loadyaml():
    # DO NOT COMMIT!
    import pdb; pdb.set_trace();
    # DO NOT COMMIT!

    if request.method == 'POST':

        yaml = request.files['file']
        if yaml and yaml.endswith('yml'):
            pass

    return render_template('loadyaml.html')
