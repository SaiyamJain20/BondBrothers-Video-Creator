from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from MySQL import User, retrieve_users_from_mysql, save_data_to_mysql, retrieve_image_from_mysql, retrieve_profile_image, upload_profile_image, AdminRetrieve, AdminRetrieveProfilePic, retrieve_audio_from_mysql, save_image_to_mysql, save_audio_to_mysql, start_connection_pool, close_connection_pool, sort_mysql, search_mysql, deleteUser, deleteAllImages, deleteAllAudio
from video import createVideo
import os
import base64
import jwt
import atexit

app = Flask(__name__)
SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY

@app.before_request
def auto_authenticate():
    if 'jwt_token' in session:
        token = session.get('jwt_token')
        if token:
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                if "userId" in data:
                    session["userId"] = data["userId"]
                    session["username"] = data["username"]
                    session["userEmail"] = data["userEmail"]
                    session["userIsAdmin"] = data["userIsAdmin"]
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                pass

start_connection_pool()

@app.route('/')
def home():
    token = session.get('jwt_token')
    if not token:
        return render_template('index.html', isAdmin = "False", user = "False")
    
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        if "userId" in session:
            if session["userIsAdmin"] == "True":
                return render_template('index.html', isAdmin = "True", user = "True", username = session["username"])
            else:
                return render_template('index.html', isAdmin = "False", user = "True", username = session["username"])
    
    except jwt.ExpiredSignatureError:
        return redirect(url_for('signin'))
    
    except jwt.InvalidTokenError:
        return redirect(url_for('signin'))

    return render_template('index.html', isAdmin = "False", user = "False")

@app.route('/signin')
def signin():
    return render_template('login.html', signin="True", signup="False", ForgetPassword="False")

@app.route('/signup')
def signup():
    return render_template('login.html', signin = "False", signup = "True", ForgetPassword = "False")

@app.route('/forgetpassword')
def forgetPassword():
    return render_template('login.html', signin = "False", signup = "False", ForgetPassword = "True")

@app.route('/SignIn', methods=['POST'])
def signinFunc():
    email = request.form['email']
    password = request.form['password']
    user = retrieve_users_from_mysql(email)
    if user == None:
        flash('No User Found')
        return redirect(url_for('signin'))
    elif check_password_hash(user.password, password):
        session["userId"] = user.id
        session["username"] = str(user.username)
        session["userEmail"] = user.email
        session["userIsAdmin"] = user.isAdmin
        if user.isAdmin:
            flash('Admin SignIn Successfull')
        else:
            flash('SignIn Successfull')
        
        token = jwt.encode({'username': user.username}, app.config['SECRET_KEY'], algorithm='HS256')
        session['jwt_token'] = token
        
        return redirect(url_for('home'))
        
    else:
        flash('Incorrect password')
        return redirect(url_for('signin'))

@app.route('/SignUp', methods=['POST'])
def signupFunc():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    hashPassword = generate_password_hash(password, method='pbkdf2')

    if retrieve_users_from_mysql(email) == None:
        user = User(name, username, email, hashPassword, isAdmin="False")
        save_data_to_mysql(user)
        user = retrieve_users_from_mysql(email)
        upload_profile_image(user.id, "./static/Images/alt_image.jpg")
        session["userId"] = user.id
        session["username"] = user.username
        session["userEmail"] = user.email
        session["userIsAdmin"] = user.isAdmin
        flash('Registration Successful')
        
        token = jwt.encode({'username': user.username}, app.config['SECRET_KEY'], algorithm='HS256')
        session['jwt_token'] = token
        
        return redirect(url_for('home'))

    else:
        flash('Email already exists')
        return redirect(url_for('signup'))

@app.route('/profile/<username>', methods=['GET'])
def profileData(username):
    try:
        if "userId" in session:
            UserEmail = session["userEmail"]
            user = retrieve_users_from_mysql(UserEmail)
            profile_image = retrieve_profile_image(user.id)
            if profile_image == None:
                upload_profile_image(user.id, "./static/Images/alt_image.jpg")
                profile_image = retrieve_profile_image(user.id)
            profileImage = base64.b64encode(profile_image.file_data).decode('utf-8')

            return render_template('profile.html', user = user, profileImage = profileImage, username = user.username, isAdmin = user.isAdmin)
        else:
            return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/getUploadedImages')
def getUploadedImages():
    try:
        userId = session["userId"]
        images = retrieve_image_from_mysql(userId)
        imageData = []
        for i in images:
            encoded_image = base64.b64encode(i.file_data).decode('utf-8')
            img = {'data' : encoded_image, 'name': i.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/getSortedImageName')
def getSortedImageName():
    try:
        userId = session.get("userId")
        images = sort_mysql(userId, "file_name")
        imageData = []
        for image in images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            img = {'data': encoded_image, 'name': image.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/getSortedImageFileSize')
def getSortedImageFileSize():
    try:
        userId = session.get("userId")
        images = sort_mysql(userId, "file_size")
        imageData = []
        for image in images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            img = {'data': encoded_image, 'name': image.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/getSortedImageDate')
def getSortedImageDate():
    try:
        userId = session.get("userId")
        images = sort_mysql(userId, "uploaded_at")
        imageData = []
        for image in images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            img = {'data': encoded_image, 'name': image.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/getPreloadedAudio')
def getPreloadedAudio():
    try:
        userId = 1
        audio = retrieve_audio_from_mysql(userId)
        audioData = []
        for a in audio:
            encoded_audio = base64.b64encode(a.file_data).decode('utf-8')
            ad = {'data': encoded_audio, 'name': a.file_name}
            audioData.append(ad)
        return jsonify(audioData)
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/getUploadedAudio')
def getUploadedAudio():
    try:
        audioData = []   
        userId = session.get("userId")
        audio = retrieve_audio_from_mysql(userId)
        for a in audio:
            encoded_audio = base64.b64encode(a.file_data).decode('utf-8')
            ad = {'data': encoded_audio, 'name': a.file_name}
            audioData.append(ad)            
        return jsonify(audioData)
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/searchBy', methods=['POST'])
def search_by():
    try:
        search_value = request.json.get('search', '')
        userId = session.get("userId")
        images = search_mysql(userId, search_value)
        imageData = []
        for image in images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            img = {'data': encoded_image, 'name': image.file_name}
            imageData.append(img)

        return jsonify(imageData)
    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/videoCreate', methods=['POST'])
def videoCreate():
    try:
        imgDuration = request.json.get('imgDuration', '5')
        Transition = request.json.get('Transition', None)
        vidResolution = request.json.get('vidResolution', '360p')
        quality = request.json.get('quality', 'low')
        
        createVideo(f'./Selected/user{session["userId"]}',f'./SelectedAudio/user{session["userId"]}', session["userId"], timePerImage=imgDuration, resolution=vidResolution, tranistion = Transition, quality= quality)
        video_path = f'../static/output/user{session["userId"]}/output_video.mp4'
        return jsonify({'message': 'Video generation successful', 'video_path': video_path})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/profileUpload', methods=['POST'])
def uploadProfileImage():
    try:
        user_id = session["userId"]
        image_file = request.files['image']

        TEMP_DIR = './temp/'

        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        image_path = f"./temp/{user_id}_profile_image.jpg"
        image_file.save(image_path)

        upload_profile_image(user_id, image_path)
        with open(image_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
        img = [{'data': encoded_image}]

        if os.path.exists(TEMP_DIR):
            for file_name in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(TEMP_DIR)
            
        return jsonify(img)
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/adminPage')
def Admin():
    try:
        if "userIsAdmin" in session:
            if session["userIsAdmin"] == 'True':
                users = AdminRetrieve()
                profilePictures = AdminRetrieveProfilePic()

                profilePic = []
                for pic in profilePictures:
                    encoded_image = base64.b64encode(pic.file_data).decode('utf-8')
                    profilePic.append(encoded_image)

                NumberOfAccounts = len(users)
                return render_template('adminPage.html', NumberOfAccounts = NumberOfAccounts, user = users, profilePic = profilePic, username = session["username"])
            else:
                return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/upload')
def upload():
    try:
        if "userId" in session:
                return render_template('uploadPage.html', username = session["username"], isAdmin = session["userIsAdmin"])
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/Upload-images', methods=['POST'])
def upload_images():
    if 'files[]' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('files[]')

    TEMP_DIR = f'./tempImg/user{session["userId"]}/'

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    for file in files:
        if file.filename != '':
            filepath = os.path.join(TEMP_DIR, file.filename)
            file.save(filepath)
            save_image_to_mysql(session["userId"], filepath, file.filename)

    if os.path.exists(TEMP_DIR):
        for file_name in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(TEMP_DIR)

    return "Images uploaded successfully"

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audioFile' not in request.files:
        return "No audio file uploaded", 400

    audio_files = request.files.getlist('audioFile')
    TEMP_DIR = f'./tempAudio/user{session["userId"]}/'

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    for audio_file in audio_files:
        if audio_file.filename != '':
            filepath = os.path.join(TEMP_DIR, audio_file.filename)
            audio_file.save(filepath)
            save_audio_to_mysql(session.get("userId"), filepath, audio_file.filename)

    if os.path.exists(TEMP_DIR):
        for file_name in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(TEMP_DIR)

    return "Audio file uploaded successfully"

@app.route('/workspace')
def create():
    try:
        if "userId" in session:
            return render_template('workspace.html', username = session["username"], isAdmin = session["userIsAdmin"])

    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/toggle-image', methods=['POST'])
def toggle_selected_images():
    image_data = request.json.get('image')
    image_name = image_data['name']

    TEMP_DIR = f'./Selected/user{session["userId"]}/'
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    image_path = os.path.join(TEMP_DIR, image_name)
    image_selected = os.path.exists(image_path)

    if image_selected:
        os.remove(image_path)
        selected = False
    else:
        with open(image_path, 'wb') as f:
            image_bytes = base64.b64decode(image_data['data'])
            f.write(image_bytes)
        selected = True
    return jsonify({'selected': selected})

@app.route('/toggle-audio', methods=['POST'])
def toggle_selected_audio():
    audio_data = request.json.get('audio')
    audio_name = audio_data['name']

    TEMP_DIR = f'./SelectedAudio/user{session["userId"]}/'
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    audio_path = os.path.join(TEMP_DIR, audio_name)
    audio_selected = os.path.exists(audio_path)

    if audio_selected:
        os.remove(audio_path)
    else:
        with open(audio_path, 'wb') as f:
            audio_bytes = base64.b64decode(audio_data['data'])
            f.write(audio_bytes)
    return jsonify({'message' : 'audio selected/deselected'})

@app.route('/empty-selected', methods=['POST'])
def remove_all_selected():
    print("Removind all selected images/audio")
    TEMP_DIR = f'./Selected/user{session["userId"]}/'
    if os.path.exists(TEMP_DIR):
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(TEMP_DIR)

    TEMP_DIR = f'./SelectedAudio/user{session["userId"]}/'
    if os.path.exists(TEMP_DIR):
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(TEMP_DIR)
    
    return jsonify({'message': 'All images and audios removed from selection'})

@app.route('/delete-video', methods=['POST'])
def delVid():
    try:
        TEMP_DIR = f'./static/output/user{session["userId"]}/'
        if os.path.exists(TEMP_DIR):
            for filename in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(TEMP_DIR)
        return jsonify({'message': 'Video deleted successfully'})
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/deleteAllImagesofUser')
def deleteAllImagesofUser():
    try:
        userId = session["userId"]
        deleteAllImages(userId)
        return jsonify({'message': 'successfully'})
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/deleteAllAudiosofUser')
def deleteAllAudiosofUser():
    try:
        userId = session["userId"]
        deleteAllAudio(userId)
        return jsonify({'message': 'successfully'})
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/deleteUser')
def delUser():
    try:
        userId = session["userId"]
        session.clear()
        deleteUser(userId)
        return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

atexit.register(close_connection_pool)

if __name__ == '__main__':
    app.run(debug=True)
