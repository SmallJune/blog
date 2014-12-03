from django.shortcuts import render_to_response
from django.utils.timezone import now

__author__ = 'garfield'


def json_performance(f):
    def wrapped_f(request, *args, **kwargs):
        in_time = now()
        f(request, *args, **kwargs)
        out_time = now()
        time = (out_time - in_time).microseconds / 1000.0
        return render_to_response('json.jinja', {
            'time_data': time,
        })

    return wrapped_f