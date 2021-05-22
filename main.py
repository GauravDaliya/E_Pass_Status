from flask import Flask, render_template
from twilio.rest import Client
from flask import request
import requests

account_sid = 'ACc415b17e7e0f0ba40a197787b22fb45f'
auth_token = 'e540b0ebc7970bff46a063a79c8481e6'

client = Client(account_sid, auth_token)

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('registerPage.html')


@app.route('/loginPage', methods=["GET", "POST"])
def login_details():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email_id = request.form['mail_id']
        source_state = request.form['sourceState']
        source_city = request.form['sourceCity']
        destination_state = request.form['destinationState']
        destination_city = request.form['destinationCity']
        number = request.form['phoneNumber']
        id_proof = request.form['idProof']
        date = request.form['date']
        full_name = first_name + last_name
        r = requests.get('https://api.covid19india.org/v4/data.json')
        json_data = r.json()
        confirmed_cases = json_data[destination_state]['districts'][destination_city]['total']['confirmed']
        total_population = json_data[destination_state]['districts'][destination_city]['meta']['population']
        travel_pass_percentage = ((confirmed_cases / total_population) * 100)
        if travel_pass_percentage < 30 and request.method == 'POST':
            status = 'CONFIRMED'
            client.messages.create(to="whatsapp:+917995466001", from_="whatsapp:+14155238886", body=
            "Hello " + full_name + " Your Travel From " + source_city + " To " + destination_city + " has " + status + " on " + date)

            return render_template('user_details.html', name=full_name, mail=email_id, proof=id_proof,
                               SourceState=source_state, SourceCity=source_city, DestinationState=destination_state,
                               DestinationCity=destination_city, num=number, Date=date, Status=status)

        else:
            status = 'NOT CONFIRMED'
            client.messages.create(to="whatsapp:+917995466001", from_="whatsapp:+14155238886", body=
            "Hello " + full_name + " Your Travel From " + source_city + " To " + destination_city + " has " + status + " on " + date + " Apply Later")

            return render_template('user_details.html', name=full_name, mail=email_id, proof=id_proof,
                               SourceState=source_state, SourceCity=source_city, DestinationState=destination_state,
                               DestinationCity=destination_city, num=number, Date=date, Status=status)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
