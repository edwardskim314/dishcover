"""
To run locally:
    python3 server.py
Go to http://localhost:3000 in your browser.
"""
import os, json, uuid
from random import choice
  # accessible as a variable in index.html:
from flask import Flask, request, render_template, g, redirect, Response, redirect, url_for, session, jsonify



tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_dir, static_folder = static_dir)
app.config['SECRET_KEY'] = os.urandom(32)

#Where user uploaded images go
umi_path = app.config['UPLOAD_FOLDER'] = './static/user_mission_images'
#create_mission user uploaded images and publish_mission user uploaded images respectively
cumi_path = umi_path + "/create_user_mission_images"
pumi_path = umi_path + "/publish_user_mission_images"

db_path = "./restaurant_database.json" #path to restaurant database
cm_path = "./create_missions_database.json" #path to create mission requests
pm_path = "./publish_missions_database.json" #path to published mission posts


#Necessary for making forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, FileField
from wtforms.validators import DataRequired, ValidationError, Regexp, NumberRange, Optional

#Method that makes image names secure strings
from werkzeug.utils import secure_filename

from flask import render_template, Flask


#Class for creating the create mission form
class CreateMissionForm(FlaskForm):
    friend_name = StringField('Friend Username', validators=[DataRequired()], render_kw={"placeholder": "Friend's Username*"})
    dish_name = StringField('Dish Name', validators=[DataRequired()], render_kw={"placeholder": "Dish Name*"})
    dish_address = StringField('Location for Dish', validators=[DataRequired()], render_kw={"placeholder": "Where can you find this dish?*"})
    dish_cost = FloatField('Approximate Cost', validators=[NumberRange(min=0.0)], render_kw={"placeholder": "Approximate Cost*"})
    dish_restrictions = StringField('Restrictions Present in Dish', render_kw={"placeholder": "Restrictions present in dish"})
    message = StringField('Add A Message', render_kw={"placeholder": "Add a message"})
    image = FileField("Upload Picture", validators=[DataRequired()])
    submit = SubmitField('Create Mission')


#Class for creating the publish mission form
class PublishMissionForm(FlaskForm):
    mission_name = StringField('Mission Name', validators=[DataRequired()], render_kw={"placeholder": "Mission Name*"})
    mission_members = StringField('People on mission', validators=[DataRequired()], render_kw={"placeholder": "People on mission*"})
    dish_name = StringField('Dish Name', validators=[DataRequired()], render_kw={"placeholder": "Dish Name*"})
    dish_address = StringField('Location for Dish', validators=[DataRequired()], render_kw={"placeholder": "Where can you find this dish?*"})
    dish_cost = FloatField('Approximate Cost', validators=[NumberRange(min=0.0)], render_kw={"placeholder": "Approximate Cost*"})
    dish_restrictions = StringField('Restrictions Present in Dish', render_kw={"placeholder": "Restrictions present in dish"})
    message = StringField('Share your experience', render_kw={"placeholder": "Share your experience"})
    image = FileField("Upload Picture", validators=[DataRequired()])
    submit = SubmitField('Publish Mission')




#List of correct guide names and their actual titles
#NOTE TODO: In the future, this should be part of a database with the HTML files pulling from the database
#rather than being hardcoded here
guide_list = {
  "eatsunder15": "Eats Under $15",
  "bagels":"Best Bagels",
  "pizza": "Pizza, Pizza, Pizza!",
  "desserts": "Sweetest Treats!",
  "asian": "Best of Asian Cuisine",
  "coffeeandtea": "Love Coffee A Latte"
}




###Uploads image to user_images
def save_image(data, save_path):
    try:
  ##Generate image name
      print("Creating image name:")
      image_name = secure_filename(data.filename)

    #Checks that the image has a name
      if image_name == "":
        image_name = str(uuid.uuid4()) + ".jpg"

      print(f"Created image name: {image_name}")
      
    #Makes sure that image name isn't already in database
      file_list = os.listdir(save_path)
      if image_name in file_list:
        base_name, extension = os.path.splitext(image_name)

        #Removes the last _ in an image name (thus turning image_1 into image)
        bn_underscore_ind = base_name.rfind('_')
        if bn_underscore_ind != -1:
            base_name = base_name[:bn_underscore_ind]
        
        #Renames image to prevent duplicates
        dup_count = 0
        while image_name in file_list:
            dup_count += 1
            new_name = f"{base_name}_({dup_count}){extension}"
            image_name = new_name

      print("create_mission Image name is: ", image_name)
      print(f"Saving {image_name}...")

  ##Saves image into the folder
      data.save(os.path.join(
        os.path.abspath(os.path.dirname(__file__)),save_path, image_name)
      )

      print(f"{image_name} saved!")

      return(image_name)
    
    except:
      print("IMAGE DID NOT SAVE")
      return("")



#Adds submitted created mission to JSON database
def save_new_mission(new_entry, db_path):
  #Whether to print publish_missions or create_missions
  if "publish" in db_path:
    c_or_p = "publish"
  else:
    c_or_p = "create"


  #Creates the JSON database if it doesn't exist
  if not os.path.exists(db_path):
    temp=[]
    with open(db_path, 'w') as f:
      json.dump(temp, f)

  #Loads the database JSON file   
  print(f"Loading {c_or_p}_missions_database.json...")
  with open(db_path) as f:
    db = json.load(f)
  print(f"{c_or_p}_missions_database.json loaded!")

  #Adds new object to existing list and writes it back into the database
  db.append(new_entry)
  with open(db_path, "w") as f:
    json.dump(db, f)




###############################################
##### START OF RENDER FUNCTIONS ###############
###############################################

#Renders home page
@app.route('/', methods=['GET', 'POST'])
def index():

  #Will pass in list of published missions
  if not os.path.exists(pm_path):
      pm=[]
  else: 
      with open(pm_path, "r") as f:
        pm = json.load(f)

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('index.html', pms=pm)


#Renders create missions page
@app.route('/createmission', methods=['GET', 'POST'])
def createMission():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  form = CreateMissionForm()
  friend_name=""
  dish_name=""
  dish_address=""
  dish_cost=0.0
  dish_restrictions=[]
  message=""
  image_data = ""

  if form.validate_on_submit():
    friend_name=form.friend_name.data
    dish_name=form.dish_name.data
    dish_address=form.dish_address.data
    dish_cost= float("{:.2f}".format(float(form.dish_cost.data))) #Rounds floats to 2 decimal places
    dish_restrictions= (form.dish_restrictions.data).split(",")
    message=form.message.data
    image_data = form.image.data

    mission_key = str(uuid.uuid4())


    #Saves image
    image_name = save_image(image_data, cumi_path)
    assert(image_name != "")


    #Saves new entry into the database
    
    new_entry = {
      "friend_name": friend_name,
      "dish_name": dish_name,
      "dish_address": dish_address,
      "dish_cost": dish_cost,
      "dish_restrictions": dish_restrictions,
      "message": message,
      "image_name": image_name,
      "mission_key": mission_key
    }
    save_new_mission(new_entry, cm_path)

    return render_template('sent-mission.html', **new_entry)

  return render_template('create-mission.html', form=form)


#Renders updated missions page
@app.route('/createmissionupdated', methods=['GET', 'POST'])
def createMissionUpdated():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('create-mission-updated.html')


#Renders accepted mission page
@app.route('/currentacceptedmission', methods=['GET', 'POST'])
def createCurrentAcceptedMission():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('current-accepted-mission.html')

#Renders second accepted mission page
@app.route('/currentacceptedmission2', methods=['GET', 'POST'])
def createCurrentAcceptedMission2():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('current-accepted-mission2.html')




#Renders guide page with ability to specify the guide rendered
#Note <> in the subdirectory and the variable in the create function must be the same name
@app.route('/exampleofguide/<guide_name>', methods=['GET', 'POST'])
def createExampleOfGuide(guide_name):
  # DEBUG: this is debugging code to see what request looks like
  print(request.args)
  
  #Only allows existing guides to be rendered
  if guide_name not in guide_list:
    return redirect("/createmissionupdated")
  

  #list of restaurants in the guide being loaded
  with open(db_path, "r") as f:
    db = json.load(f)


  #rl is the list of restaurants with the same category term as the guide's guide_name
  rl = [obj for obj in db if (guide_name in obj.get("category"))]
  

  return render_template('exampleof-guide.html', guide_name=guide_list[guide_name], restaurant_list=rl)



#Renders notifications page
@app.route('/notifications', methods=['GET', 'POST'])
def createNotifications():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('notifications.html')


#Renders pending mission page
'''
@app.route('/pendingmission', methods=['GET', 'POST'])
def createPendingMission():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('pending-mission.html')
'''


#Renders profile page
@app.route('/profile', methods=['GET', 'POST'])
def createProfile():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('profile.html')


#Renders publish mission page
@app.route('/publishmission', methods=['GET', 'POST'])
def createPublishMission():

  form = PublishMissionForm()
  
  mission_name = ""
  mission_members = []
  dish_name = ""
  dish_address = ""
  dish_cost = 0.0
  dish_restrictions = []
  message = ""
  image_data = ""

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  if form.validate_on_submit():
    mission_name=form.mission_name.data
    mission_members=(form.mission_members.data).split(",")
    dish_name=form.dish_name.data
    dish_address=form.dish_address.data
    dish_cost= float("{:.2f}".format(float(form.dish_cost.data))) #Rounds floats to 2 decimal places
    dish_restrictions= (form.dish_restrictions.data).split(",")
    message=form.message.data
    image_data = form.image.data

    mission_key = str(uuid.uuid4())


    #Saves image
    image_name = save_image(image_data, pumi_path)
    assert(image_name != "")


    #Saves new entry into the database
    new_entry = {
      "mission_name": mission_name,
      "mission_members": mission_members,
      "dish_name": dish_name,
      "dish_address": dish_address,
      "dish_cost": dish_cost,
      "dish_restrictions": dish_restrictions,
      "message": message,
      "image_name": image_name,
      "mission_key": mission_key
    }
    save_new_mission(new_entry, pm_path)


    return redirect("yourmissions")
  

  return render_template('publish-mission.html', form=form)




#Renders sent missions page
#Note <> in the subdirectory and the variable in the create function must be the same name
@app.route('/sentmission/<mission_key>', methods=['GET', 'POST'])
def createSentMission(mission_key):

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  #Loads up created mission database to identify the sent mission needed
  sent_mission = ""
  with open(cm_path, "r") as f:
    cm_db = json.load(f)
    sent_mission = [obj for obj in cm_db if (mission_key == obj.get("mission_key"))]

  try:
    assert len(sent_mission) <= 1
    if len(sent_mission) < 1:
      return redirect("/sentmissionsupdated")
  except:
    print(len(sent_mission))
    print(sent_mission)
  
    
  sent_mission = sent_mission[0]


  return render_template('sent-mission.html', **sent_mission)


#Renders updated page for sent missions
@app.route('/sentmissionsupdated', methods=['GET', 'POST'])
def createSentMissionsUpdated():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #Will pass in list of created (aka sent to others) missions
  if not os.path.exists(cm_path):
      cm_db =[]
  else: 
    with open(cm_path, "r") as f:
      cm_db = json.load(f)
  

  return render_template('sent-missions-updated.html', sent_missions = cm_db)


#Renders your missions page
@app.route('/yourmissions', methods=['GET', 'POST'])
def createYourMissions():

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  return render_template('your-missions.html')


#404 error
@app.errorhandler(404)
#default error function
def not_found(e): 
  return render_template("404.html") 



#Creates folders in umi_path, cumi_path, and pumi_path
def create_user_img_dirs():
  for dir in [umi_path, cumi_path, pumi_path]:
    #Makes sure that the folders exist
    if not os.path.exists(dir):
      os.makedirs(dir)


if __name__ == "__main__":
  import click
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=3000, type=int)

  def run(debug, threaded, host, port):

    create_user_img_dirs()

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
