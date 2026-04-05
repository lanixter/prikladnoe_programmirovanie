from flask import Flask, request, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange
import subprocess
import signal
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-for-csrf'


class CodeForm(FlaskForm):

    code = StringField('Python Code', validators=[
        InputRequired(message='Code is required')
    ])
    timeout = IntegerField('Timeout (seconds)', validators=[
        InputRequired(message='Timeout is required'),
        NumberRange(min=1, max=30, message='Timeout must be between 1 and 30 seconds')
    ])


HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Remote Code Execution</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .error { color: red; }
        textarea, input { width: 100%; padding: 10px; margin: 5px 0; }
        button { padding: 10px 20px; background: blue; color: white; border: none; cursor: pointer; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Remote Code Execution</h1>
    <form method="POST">
        {{ form.csrf_token }}
        <div>
            {{ form.code.label }}<br>
            {{ form.code(rows=10, cols=50) }}<br>
            {% for error in form.code.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>
        <div>
            {{ form.timeout.label }}<br>
            {{ form.timeout() }}<br>
            {% for error in form.timeout.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>
        <button type="submit">Execute</button>
    </form>
</body>
</html>
'''


def execute_code_safely(code, timeout):

    safe_code = code.replace('"', '\\"').replace('`', '').replace('$', '')

    cmd = f'prlimit --nproc=1:1 --nofile=10:10 python3 -c "{safe_code}"'

    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None
        )

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return {
                'success': True,
                'stdout': stdout,
                'stderr': stderr,
                'returncode': process.returncode
            }
        except subprocess.TimeoutExpired:
            #
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.kill()
            return {
                'success': False,
                'error': f'Execution timed out after {timeout} seconds'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route('/execute', methods=['GET', 'POST'])
def execute():

    form = CodeForm()

    if form.validate_on_submit():
        result = execute_code_safely(form.code.data, form.timeout.data)

        if result['success']:
            return f'''
            <h1>Execution Result</h1>
            <h2>STDOUT:</h2>
            <pre>{result['stdout']}</pre>
            <h2>STDERR:</h2>
            <pre>{result['stderr']}</pre>
            <h2>Return Code:</h2>
            <pre>{result['returncode']}</pre>
            <a href="/execute">← Back</a>
            '''
        else:
            return f'''
            <h1>Execution Failed</h1>
            <pre style="color: red;">{result['error']}</pre>
            <a href="/execute">← Back</a>
            '''

    return render_template_string(HTML_FORM, form=form)


if __name__ == '__main__':
    app.run(debug=True)