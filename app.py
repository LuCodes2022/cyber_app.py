from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages

# List of countries for the dropdown
countries = ['USA', 'Canada', 'UK', 'France', 'Germany', 'Australia']

# Honeypot field name (hidden from users)
honeypot_field = 'phone'

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        country = request.form['country']
        message = request.form['message']
        gender = request.form['gender']
        subjects = request.form.getlist('subjects')
        honeypot = request.form[honeypot_field]

        # Sanitization (escaping special characters)
        first_name = sanitize(first_name)
        last_name = sanitize(last_name)
        email = sanitize(email)
        country = sanitize(country)
        message = sanitize(message)
        gender = sanitize(gender)

        # Default subjects to "Others" if none selected
        if not subjects:
            subjects = ['Others']

        # Validation
        errors = []
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not email or not is_valid_email(email):
            errors.append('A valid email is required.')
        if not country or country not in countries:
            errors.append('A valid country is required.')
        if not message:
            errors.append('Message is required.')
        if gender not in ['M', 'F']:
            errors.append('Gender selection is required.')
        if honeypot:
            errors.append('Bot detected.')

        if errors:
            # If there are errors, flash them and render the form again with existing data
            for error in errors:
                flash(error)
            return render_template('contact.html', first_name=first_name, last_name=last_name, email=email,
                                   country=country, message=message, gender=gender, subjects=subjects, countries=countries)
        else:
            # If no errors, display the thank you page with encoded information
            return render_template('thank_you.html', first_name=first_name, last_name=last_name, email=email,
                                   country=country, message=message, gender=gender, subjects=subjects)

    return render_template('contact.html', countries=countries)

def sanitize(input_string):
    return re.sub(r'[<>]', '', input_string)

def is_valid_email(email):
    # Simple email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

if __name__ == '__main__':
    app.run(debug=True)
