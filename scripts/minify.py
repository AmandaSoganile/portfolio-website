import rcssmin, rjsmin, pathlib

css = pathlib.Path('static/css/style.css')
css.write_text(rcssmin.cssmin(css.read_text()))
print('Minified CSS:', css.stat().st_size, 'bytes')

js = pathlib.Path('static/js/app.js')
js.write_text(rjsmin.jsmin(js.read_text()))
print('Minified JS:', js.stat().st_size, 'bytes')
