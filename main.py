from flask import Flask, redirect, url_for, render_template, request, flash
import os
### custom imports
import calendars
import helpers

app = Flask('__main__')
app.secret_key = os.urandom(16)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST' and 'cal_text' in request.form and 'year' in request.form:
        calendar = calendars.Calendar(request.form['cal_text'], request.form['year'])
        if calendar.flagged_lines:
            flash(f'Error processing line(s): {", ".join([str(x) for x in calendar.flagged_lines])}')
        
        year_tables = calendar.year_tables()
        month_names = ''
        month_tables = ''
        for month in range(1,13):
            month_names += f'<span name={month}>' + year_tables[month]['name'] + ' ' + str(calendar.year) + '</span>'
            month_tables += f'<div name={month}>' + year_tables[month]['caltable'] + '</div>'
        return render_template('home.html', processed_text = calendar.processed_text, year = calendar.year, month_names = month_names, month_tables = month_tables)
    return render_template('home.html')


@app.route('/convert/', methods=['GET', 'POST'])
def converter():
    to_display = ''
    if request.method == 'POST' and 'text' in request.form:
        to_display = helpers.remove_bracketed_words(request.form['text'])
    return render_template('converter.html', txt = to_display)


@app.errorhandler(404)
def error_not_found(e):
    flash('Error 404: Page not found. You have been redirected to the home page.')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(
        debug = True
    )