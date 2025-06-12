from flask import Flask, flash
from flask_login import LoginManager, login_manager
from Models.base_model import db
from Models.users import Staff
from flask_migrate import Migrate
from config import Config
from flask_bcrypt import Bcrypt
from Errors.handlers import errors
from Accountant.routes import accountant
from Admin.routes import admin
from Auth.routes import auth
from Clerk.routes import clerk
from LabTech.routes import lab_tech
from StockController.routes import stock_controller
from datetime import datetime
from collections import Counter
import folium
import pandas as pd
from sqlalchemy.sql import func, cast, literal_column
from sqlalchemy.types import String
from itertools import chain

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)
app.register_blueprint(accountant)
app.register_blueprint(errors)
app.register_blueprint(admin)
app.register_blueprint(auth)
app.register_blueprint(clerk)
app.register_blueprint(lab_tech)
app.register_blueprint(stock_controller)
login_manager = LoginManager()
login_manager.blueprint_login_views = {
  'auth': '/auth/signin',
}
login_manager.login_message="Please Login or Sign Up to access this page"
login_manager.login_message_category="danger"
login_manager.refresh_view = "/auth/signin"
login_manager.needs_refresh_message = (
  "Your account has been inactive for a long time please login."
)
login_manager.needs_refresh_message_category = "info"
login_manager.init_app(app)
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
  try:
    return Staff.query.filter_by(unique_id = user_id).first()
  except:
    flash("Failed to login the user", "danger")

# @app.route("/")
# @app.route("/home")
# @login_required
# @fresh_login_required
# def home():
#   clients = Clients.query.all()
#   medicines = Medicine.query.all()
#   client_medicines = ClientMedicine.query.all()
#   payments = ClientPayment.query.all()
#   diseases = Diseases.query.all()
#   #Most diagnosed disease
#   diagnosed_data= ClientDisease.query.all()
#   diagnosed_disease_ids = []

#   if diagnosed_data:
#     for diagnosis in diagnosed_data:
#       diagnosed_disease_ids.append(diagnosis.disease_id)
#     diagnosis = Counter(diagnosed_disease_ids)
#     most_diagnosed_diseases, diagnosed_count = diagnosis.most_common(1)[0]

#     #Most prescribed medication
#     prescription_data = Prescriptions.query.all()
#     prescribed_medicine_ids = []
#     for prescription in prescription_data:
#       prescribed_medicine_ids.append(prescription.medicine_id)
#     prescriptions = Counter(prescribed_medicine_ids)
#     most_prescribed_medicine, prescribed_count = prescriptions.most_common(1)[0]
    
#     #Paste below here
#     result = (
#       db.session.query(
#           ClientLocation.region,
#           func.string_agg(cast(ClientDisease.disease_id, String(10)), literal_column("','")).label("disease_ids")
#       )
#       .join(Clients, Clients.location == ClientLocation.id)
#       .join(ClientDisease, ClientDisease.client_id == Clients.id)
#       .group_by(ClientLocation.region)
#       .all()
#     )
#     output = {row.region: [int(d) for d in row.disease_ids.split(",")] if row.disease_ids else [] for row in result}
#     regions_with_data = list(output.keys())
#     values = list(output.values())

#     # Load Tanzania GeoJSON data
#     with open("tanzania.geojson", "r", encoding="utf-8") as f:
#       tanzania_geo = json.load(f)
    
#     data = {
#       "Region": regions_with_data,
#       "Disease": values
#     }
#     state_data = pd.DataFrame(data)

#     # Create a map centered on Tanzania
#     m = folium.Map(location=[-6.369028, 34.888822], zoom_start=6)

#     folium.GeoJson(
#           tanzania_geo,
#           name="Region Borders",
#           style_function=lambda feature: {
#               "fillColor": "yellow",  # Keep regions yellow
#               "color": "black",  # Border color
#               "weight": 2,  # Border thickness
#           },
#           tooltip=folium.GeoJsonTooltip(
#               fields=["shapeName"],  # Adjust based on your GeoJSON properties
#               aliases=["Region:"],
#               sticky=True
#           )
#       ).add_to(m)


#     for feature in tanzania_geo["features"]:
#       region_name = feature["properties"]["shapeName"]
#       feature["properties"]["DiseaseCount"] = len(output.get(region_name, []))
#       diagnosed_diseases = output.get(region_name, [])
#       most_diagnosed_disease = Counter(diagnosed_diseases).most_common(1)
#       if most_diagnosed_disease:
#         x,y = most_diagnosed_disease[0]
#         most_diagnosed_disease_name= [disease.name for disease in diseases if disease.id == x]
#         feature["properties"]["MostDiagnosed"] = [most_diagnosed_disease_name[0]] if most_diagnosed_disease_name else ["none"]
#       else:
#         feature["properties"]["MostDiagnosed"] = ["none"]

#       feature["properties"]["DiseaseNames"] = [disease.name for disease in diseases for disease_id in output.get(region_name, []) if disease.id == disease_id]

#     # Add a hover tooltip to display region name & disease count
#     folium.GeoJson(
#         tanzania_geo,
#         style_function=lambda feature: {
#             "fillColor": "transparent", 
#             "color": "transparent"
#         },
#         tooltip=folium.GeoJsonTooltip(
#             fields=["shapeName","DiseaseCount","DiseaseNames","MostDiagnosed"],
#             aliases=["Region:","Disease count:","Disease name:","Most diagnosed:"],
#             labels=True,
#             sticky=False
#         )
#         # Manually add disease count data to each region in GeoJSON

#       ).add_to(m)

#     # Add layer control
#     folium.LayerControl().add_to(m)

#     # Store map HTML in a variable
#     map_html = m.get_root().render()
#     with open("templates/tanzania_map.html", "w", encoding="utf-8") as f:
#       f.write(map_html)
#     return render_template("home.html",clients=clients, medicines=medicines, diseases=diseases ,client_medicines=client_medicines,payments=payments, prescriptions=prescriptions, most_prescribed_medicine=most_prescribed_medicine, prescribed_count=prescribed_count, most_diagnosed_diseases=most_diagnosed_diseases, diagnosed_count=diagnosed_count)
#   else:
#     return render_template("home.html",clients=clients, medicines=medicines, diseases=diseases ,client_medicines=client_medicines, payments=payments)

# @app.route("/map")
# def map():
#   try:
#     return render_template("tanzania_map.html")
#   except:
#     return "No data to display on the map"

# @app.route("/Clients")
# def Client():
#   """
#   querying/getting/retreiving data from database
#   client records table
#   10 records

#   get data

#   Must
#   1. Class Name
#   2. Query - get the data
#   optional
#   3. filter
#   4. Number of records - (first | all)
#   """

#   """
#   Clients.query.all() -> a bunch objects(1115)
#   object1 -> clients, object2 -> clients
#   [object1,object2......object1115] -> clients

#   for loop -> access the objects
#   """

#   clients = Clients.query.all()

#   return render_template("client.html",clients=clients)

# @app.route("/Diseases")
# def Disease():
#   diseases = Diseases.query.all()
#   return render_template("disease.html",diseases=diseases)

# @app.route("/edit-disease/<int:disease_id>", methods=["POST", "GET"])
# def edit_disease(disease_id):
#   disease = Diseases.query.get(disease_id)
#   if not disease:
#     flash("disease not found", category="danger")
#     return redirect(url_for("Disease"))
#   if request.method == "POST":
#     disease.name = request.form.get("dname")
#     db.session.commit()
#     flash("Disease record updated successfully", category="success")
#     return redirect(url_for('Disease'))
#   else:
#     return render_template("new_disease.html", disease=disease)

# @app.route("/remove-disease/<int:disease_id>")
# def remove_disease(disease_id):
#   disease = Diseases.query.get(disease_id)
#   if not disease:
#     flash("Disease not found", category="danger")
#   else:
#     db.session.delete(disease)
#     db.session.commit()
#     flash("Disease removed successfully", category="success")
#   return redirect(url_for("Disease"))

# @app.route("/Medicine")
# def Medicines():
#   medicines = Medicine.query.all()
#   return render_template("medicine.html",medicines=medicines)

# @app.route("/edit-medicine/<int:medicine_id>", methods=["POST", "GET"])
# @login_required
# def edit_medicine(medicine_id):
#   medicine = Medicine.query.get(medicine_id)
#   if not medicine:
#     flash("medicine not found", category="danger")
#     return redirect(url_for("Medicine"))
#   if request.method == "POST":
#     medicine.name = request.form.get("Mname")
#     medicine.price = request.form.get("Mprice")
#     db.session.commit()
    
#     flash("Medicine record updated successfully", category="success")


#     return redirect(url_for('home'))
#   else:
#     return render_template("new_medicine.html", medicine=medicine)

# @app.route("/prescribe-patient/<int:patient_id>", methods=["POST"])
# def prescribe_patient(patient_id):
#   patient = Clients.query.get(patient_id)
#   medicine = Medicine.query.get(request.form.get("medication"))
#   """
#   check the quantity of the medicine to be prescribed
#   if the quantity is greater than 0 or if the quantity is less than 1
#   if it is -> presribe
#   update the quantity -> deduct
#   if it's not flash a message
#   """
#   if medicine.quantity > 0:
#     exisiting_prescription = ClientMedicine.query.filter_by(client_id=patient.id, is_paid=False).first()

#     if not exisiting_prescription:
#       client_medicine = ClientMedicine(
#         client_id = patient.id,
#       )
#       db.session.add(client_medicine)
#       db.session.commit()
#       new_prescription = Prescriptions(
#         medicine_id = medicine.id,
#         client_medicine_id = client_medicine.id
#       )
#       db.session.add(new_prescription)
#       medicine.quantity = medicine.quantity - 1
#       db.session.commit()
#     else:
#       new_prescription = Prescriptions(
#         medicine_id = medicine.id,
#         client_medicine_id = exisiting_prescription.id
#       )
#       db.session.add(new_prescription)
#       db.session.commit()
#       medicine.quantity = medicine.quantity - 1
#       db.session.commit()
#     flash("Medicine prescribed successfully", category="success")
#   else:
#     flash("Out of Stock kindly restock", category="warning")
#     return redirect(url_for('medicine_stock',medicine_id=medicine.id))

#   return redirect(url_for('clients_detail', clients_id=patient.id))

# @app.route("/medicine-payment/<int:client_id>")
# def medicine_payment(client_id):
#   # The client
#   # The prescription's associated with the client - More than 1
#   # The status of the prescription
#   #   -> if is_paid is False -> mark that prescription as paid
  
#   client = Clients.query.get(client_id)
#   if not client:
#     flash("Client not found", category="danger")
#     return redirect(url_for("home"))
#   client_prescription = ClientMedicine.query.filter_by(client_id = client.id, is_paid = False).first()
#   prescriptions = Prescriptions.query.filter_by(client_medicine_id = client_prescription.id).all()
#   total = sum([medicine.price for medicine in Medicine.query.all() for prescription in prescriptions if medicine.id == prescription.medicine_id])
#   new_payment = ClientPayment(
#     amount = total,
#     is_paid = True,
#     date_paid = datetime.now()
#   )
#   db.session.add(new_payment)
#   db.session.commit()
#   client_prescription.client_payment_id = new_payment.id
#   client_prescription.is_paid = True 
#   db.session.commit()
#   flash("Payment successfull", category="success")
#   return redirect(url_for("clients_detail", clients_id=client.id))


# @app.route("/medicine-stock/<int:medicine_id>", methods=["POST","GET"])
# @login_required  
# def medicine_stock(medicine_id):
#   medicine = Medicine.query.get(medicine_id)
#   if request.method == "POST":
#     stock_amount = request.form.get("stock")
#     medicine.quantity = stock_amount
#     db.session.commit()
#     flash("Stock added succesfully", category='success')

#   return render_template("stock.html",medicine=medicine)

# @app.route("/remove-medicine/<int:medicine_id>")
# def remove_medicine(medicine_id):
#   medicine = Medicine.query.get(medicine_id)
#   if not medicine:
#     flash("Medicine not found", category="danger")
#   else:
#     db.session.delete(medicine)
#     db.session.commit()
#     flash("Medicine removed successfully", category="success")
#   return redirect(url_for("home"))

# @app.route("/Client_details/<int:clients_id>")
# @login_required
# def clients_detail(clients_id):
#   clients_details = Clients.query.get(clients_id)
#   all_diseases = Diseases.query.all()
#   all_medicines = Medicine.query.all()
#   locations = ClientLocation.query.all()
#   client_diseases = ClientDisease.query.filter_by(client_id=clients_details.id).all()
#   client_medicines= ClientMedicine.query.filter_by(client_id=clients_details.id).all()
#   client_payments = ClientPayment.query.all()

#   if not clients_details:
#     return "Invalid client ID. No matching client found"
#   return render_template('client_details.html', clients_details=clients_details, all_diseases=all_diseases, client_diseases=client_diseases,all_medicines=all_medicines,client_medicines=client_medicines, locations=locations, client_payments=client_payments)

# @app.route("/edit-client/<int:client_id>", methods=["POST", "GET"])
# @login_required
# def edit_client(client_id):
#   client = Clients.query.get(client_id)
#   location = ClientLocation.query.all()
#   if not client:
#     flash("Client not found", category="danger")
#     return redirect(url_for("Client"))
#   if request.method == "POST":
#     client.full_name = request.form.get("fname")
#     client.specific_location = request.form.get("loc1")
#     client.phone_number_1 = request.form.get("phone1")
#     client.phone_number_2 = request.form.get("phone2")
#     client.age = request.form.get("age")
#     client.gender = request.form.get("Gender")
#     db.session.commit()
#     flash("Client record updated successfully", category="success")
#     return redirect(url_for('clients_detail', clients_id=client.id))
#   else:
#     return render_template("new_patient.html", client=client, location=location)

# @app.route("/update-location/<int:patient_id>", methods=["POST"])
# def update_location(patient_id):
#   """
#   ID the client - From DB
#   handle the form submission
#     - Route must handle POST request
#     - 1st input - location input field (name of 'location')
#       - The location ID - INT
#     - 2nd input - specific location input field (name of 'specific_location')
#       - Name of the specific location - String

#   Save our db - with the changes
#   redirect to the client details page
#   """
#   client = Clients.query.get(patient_id)
#   location_name = request.form.get("location")
#   client.location = location_name
#   db.session.commit()
#   flash("Location saved succesfully", category="success")
#   return redirect(url_for('clients_detail',clients_id=client.id))

# @app.route("/diagnose-patient/<int:patient_id>", methods=["POST"])
# def diagnose_patient(patient_id):
#   patient = Clients.query.get(patient_id)
#   disease = Diseases.query.get(request.form.get("disease"))
#   client_disease = ClientDisease(
#     client_id = patient.id,
#     disease_id = disease.id
#   )
#   db.session.add(client_disease)
#   db.session.commit()
#   flash("Patient diaginosed successfully", category="success")
#   return redirect(url_for('clients_detail', clients_id=patient.id))

# @app.route("/Client_feedback/<int:client_id>", methods=["POST"])
# def client_feedback(client_id):
#   client = Clients.query.get(client_id)
#   feedback = ClientFeedback(
#     clients_id = client_id,
#     status = request.form.get("feedback")
#   )
#   db.session.add(feedback) 
#   db.session.commit()

#   flash('feedback added', category="success")

#   return redirect(url_for('clients_detail',clients_id = client.id))

# @app.route("/Client_delete/<int:clients_id>")
# def clients_delete(clients_id):
#   client_delete = Clients.query.get(clients_id)
#   if not client_delete:
#     flash('Cannot delete a record that does not exist',category="danger")

#   db.session.delete(client_delete)
#   db.session.commit()

#   flash('Record deleted succesfuly',category="success")
#   return redirect(url_for('home'))

# @app.route("/New_patient", methods=["GET", "POST"])
# @login_required
# def New_patient():
#   location= ClientLocation.query.all()
#   if request.method=="POST":
#     full_name = request.form.get("fname")
#     Phonenumber1 = request.form.get("phone1")
#     Phonenumber2 = request.form.get("phone2")
#     age = request.form.get("age")
#     gender = request.form.get("Gender")
#     specific_location = request.form.get("loc1")


#     Add_patient = Clients(
#       full_name = full_name,
#       phone_number_1 = Phonenumber1,
#       phone_number_2 = Phonenumber2,
#       age = age,
#       gender = gender,
#       specific_location = specific_location
#     )
#     db.session.add(Add_patient)
#     db.session.commit()
#     flash("Details added", category='success')
    
#     return redirect(url_for('home'))
#   return render_template('new_patient.html', location=location)

# @app.route("/New_disease", methods=["GET", "POST"])
# @login_required
# def New_disease():
#   if request.method == "POST":
#     Disease_name=request.form.get("dname")
    
#     Add_Disease = Diseases(
#       name = Disease_name,
      
#     )
#     db.session.add(Add_Disease)
#     db.session.commit()
#     flash("Disease added", category='success')
#     return redirect(url_for('Disease'))
#   return render_template('new_disease.html')

# @app.route("/New_medicine", methods=["GET", "POST"])
# @login_required
# def New_medicine():

#   if request.method == "POST":
#     Medicine_name=request.form.get("Mname")
#     Medicine_price=request.form.get("Mprice")

#     Add_Medicine = Medicine(
#       name = Medicine_name,
#       price = Medicine_price,
#     )
#     db.session.add(Add_Medicine)
#     db.session.commit()
#     flash("Medicine added", category='success')
#     return redirect(url_for('home'))
#   return render_template('new_medicine.html')

if __name__ == "__main__":
  app.run(debug=True)
