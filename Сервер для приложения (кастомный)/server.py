from flask import Flask, render_template, url_for, request, redirect, abort, make_response, session, send_from_directory
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import json
import string
import system
import os

"""
Made By Xsarz
GitHub: https://github.com/xXxCLOTIxXx
YouTube: https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q
Telegram group: https://t.me/DxsarzUnion
Telegram: @DXsarz
Library for this server: https://github.com/xXxCLOTIxXx/ChatixApi
"""

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")



host="192.168.31.18"
port="4567"

with open("database.json", "r") as file:
	chat = json.load(file)
background_url = chat['background']
adminId = '3aeegfb81-8dds815-47cffe4-9bwdwd65-a0e375qqeq5ew0rae24'

height = '350'
width = '200'


html1 = """
<!DOCTYPE html>

<html>
	<head>
	<script type="text/javascript">
	function reload() {
	setTimeout(function(){
	location.reload();}, 1200);
	}
	reload()
	</script>


  <style type="text/css">
   BODY {
    background: url("""



html2 = """);
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment:fixed
   }
   .message{
   background-color: #eee4e1;
   color: black;
   border-radius: 10px;
   padding: 5px;
   max-width: 60%;
   display: inline-block;
   }

   .Mymessage{
   background-color: #7fc8f8;
   color: black;
   border-radius: 10px;
   padding: 10px;
   max-width: 60%;
   float: right;
   display: inline-block;
	}

   .changeBackground{
   text-align: center;
   background-color: #f8edeb;
   color: black;
   max-width: 80%;
   margin: auto;
   border-radius: 10px;
   padding: 5px;
   opacity: .8;
   }
  </style>
  </head>
  <body>
"""
html3 = """
  </body>
  </html>
"""



app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
UPLOAD_FOLDER= 'static/files'
baned_user = []

@app.route("/", methods=["get", "post"])
def root():
	if str(request.args.get('uid')) == 'None' or str(request.args.get('name')) == 'None':
		return 'incorrect request⚠'
	if request.args.get('adminId') == adminId:
		return "Waiting for admin command..."
	else:
		return "You don't have permission⚠"

@app.route("/getMessage", methods=["get"])
def getMess():
	with open("database.json", "r") as file:
		chat = json.load(file)
	background_url = chat['background']
	with open("database.json", "r") as file:
		chat = json.load(file)
	try:
		response = ''
		amount = request.args.get('amount')

		if str(amount) == 'None' or int(amount) > len(chat['chat']):
			amount = len(chat['chat'])
		else:
			amount = int(request.args.get('amount'))
		if str(request.args.get('uid')) == 'None':
			return 'incorrect request⚠'
		if str(request.args.get('uid')) in baned_user:
			return "You are baned"
		if chat['chat'] == []:
			return  f"{html1} {background_url} {html2}{html3}"
		for i in range(amount):
			if amount != len(chat['chat']):
				i = int("-"+str(amount))
			message = chat['chat'][i]['message']
			name = chat['chat'][i]['name']+':<br>'
			userId = chat['chat'][i]['uid']
			if userId == request.args.get('uid'):
				classMess = 'Mymessage'
				name = ''
			else:
				classMess = 'message'
			if chat['chat'][i]['messageType'] == '2':
				url=f'static/files/{message}'
				response = f'{response}<br><br> <div class="{classMess}">{name}<a href='f'{url}><img src="{url}" height="{height}px" width="{width}px" alt="Image Not Found"></a></div><br><br>'
			elif chat['chat'][i]['messageType'] == '5':
				response = f'{response}<br><br> <div class="{classMess}">{name} <a href='f'{message}><img src="{message}" height="{height}px" width="{width}px" alt="Image Not Found"></a></div><br><br>'
			elif chat['chat'][i]['messageType'] == '1':
				response = f'{response}<br><div class="changeBackground">{message}</div><br><br>'
			elif chat['chat'][i]['messageType'] == '0':
				response = f'{response}<br>  <div class="{classMess}">{name} {message}</div><br><br>'
			elif chat['chat'][i]['messageType'] == '4':
				audio=f'static/files/{message}'
				response = f'{response}<br><br> <a href='f'{audio}><div class="{classMess}">{name}:<br><audio controls src="{audio}"></audio></div></a><br><br>'
			elif chat['chat'][i]['messageType'] == '3':
				messageUrl =''
				for i in range(len(message.split(" "))):
					if message.split(" ")[i][0:3] == "http" or message.split(" ")[i][0:4] == "https":
						messageUrl = message.split(" ")[i]
				response = f'{response}<br><br> <a href="{messageUrl}"><div class="{classMess}">{name}{message}</div></a> <br>'
			amount -=1
		response = f"{html1} {background_url} {html2}{response}{html3}"
		return response
	except Exception as ex:
		print(ex)
		return "Server error, try again later"

@app.route("/postMessage")
def postMess():
	try:
		if str(request.args.get('uid')) == 'None' or str(request.args.get('name')) == 'None' or str(request.args.get('message')) == 'None':
			return 'incorrect request⚠'
		if str(request.args.get('uid')) in baned_user:
			return "You are baned"
		name = request.args.get('name')
		message = request.args.get('message')
		urlCheck = system.urlCheck(message)
		if urlCheck == "noUrl":
			messageType = '0'
		elif urlCheck == "url":
			messageType = '3'
		else:
			messageType = '0'
		for_json = {"name": name, "message": message, "messageId": system.generateId(16), "messageType": messageType, "uid": str(request.args.get('uid'))}
		with open("database.json", "r") as file:
			chat = json.load(file)
		if chat['onlyViewMode'] == 'on' and request.args.get('adminId') != adminId:
			return 'Вы не можете отправить сообщение, режим чата "Только просмотр"'
		else:
			chat['chat'].append(for_json)
			with open("database.json", "w") as file:
				json.dump(chat,file)
			return "Succesful✅✔☑"
	except:
		return 'message send error'

@app.route("/updateBackground", methods=['GET',"POST"])
def changeBackground():
	try:
		imgUrl = dict(request.form)
		if str(request.args.get('uid')) == 'None' or str(request.args.get('name')) == 'None':
			return 'incorrect request⚠'
		if str(request.args.get('uid')) in baned_user:
			return "You are baned"
		with open("database.json", "r") as file:
			chat = json.load(file)
		name = request.args.get('name')
		admin = request.args.get('adminId')
		uid = request.args.get('uid')
		if imgUrl != {}:
			if chat['background'] == imgUrl['url']:
				return 'This picture is already set🎎'
			for_json = {"name": name, "message": f'{name} Изменил(а) фон чата', "messageId": system.generateId(16), "messageType": "1", "uid": str(request.args.get('uid'))}
			chat['chat'].append(for_json)
			chat['background'] = imgUrl['url']
			with open("database.json", "w") as file:
				json.dump(chat, file)
			return 'Successful✅✔☑'

		
		
		global background_url
		form = UploadFileForm()
		if request.args.get('adminId') == adminId:
			if form.validate_on_submit():
				file = form.file.data
				filename = secure_filename(file.filename)
				file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
				background_url = f'static/files/{filename}'
				for_json = {"name": name, "message": f'{name} Изменил(а) фон чата', "messageId": system.generateId(16), "messageType": "1", "uid": str(request.args.get('uid'))}
				chat['chat'].append(for_json)
				chat['background'] = background_url
				with open("database.json", "w") as file:
					json.dump(chat, file)
				return "Succesful✅✔☑"
			return render_template('changeBackground.html', form=form, name=name, uid=uid,adminId=admin)
		else:
			return "You don't have permission⚠"
	except:
		return 'Server error'

@app.route("/clearChat")
def clearChat():
	if str(request.args.get('name')) == 'None' or str(request.args.get('uid')) == 'None':
		return 'incorrect request⚠'
	if str(request.args.get('uid')) in baned_user:
		return "You are baned"
	if request.args.get('adminId') == adminId:
		name = request.args.get('name')
		for_json = {"name": name, "message": f'{name} Очистил(а) чат', "messageId": system.generateId(16), "messageType": "1", "uid": str(request.args.get('uid'))}
		with open("database.json", "r") as file:
			chat = json.load(file)
		chat['chat'] = []
		chat['chat'].append(for_json)
		with open("database.json", "w") as file:
			json.dump(chat, file)
			return "Chat cleared successfully✅✔☑"
	else:
		return "You don't have permission⚠"


@app.route("/onlyViewMode")
def onlyViewMode():
	try:
		if str(request.args.get('name')) == 'None' or str(request.args.get('uid')) == 'None':
			return 'incorrect request⚠'
		if str(request.args.get('uid')) in baned_user:
			return "You are baned"
		if request.args.get('adminId') == adminId:
			name = request.args.get('name')
			onlyView = request.args.get('onlyView').lower()
			with open("database.json", "r") as file:
				chat = json.load(file)
			if onlyView == chat['onlyViewMode']:
				return "This mode is already set🎯"
			else:
				if onlyView == 'on':
					for_json = {"name": name, "message": f'<div class="changeBackground">{name} Изменил(а) режим чата на "Только просмотр"</div>', "messageId": system.generateId(16), "messageType": "1", "uid": str(request.args.get('uid'))}
					chat['onlyViewMode'] = 'on'
					chat['chat'].append(for_json)
					with open("database.json", "w") as file:
						json.dump(chat, file)
						return "Succesful✅✔☑"
				elif onlyView == 'off':
					for_json = {"name": name, "message": f'<div class="changeBackground">{name} Выключил(а) режим чата "Только просмотр"</div>', "messageId": system.generateId(16), "messageType": "1", "uid": str(request.args.get('uid'))}
					chat['onlyViewMode'] = 'off'
					chat['chat'].append(for_json)
					with open("database.json", "w") as file:
						json.dump(chat, file)
						return "Succesful✅✔☑"
				else:
					return "incorrect request⚠"

		else:
			return "You don't have permission⚠"
	except:
		return 'error'


@app.route("/getJson")
def getJson():
	if str(request.args.get('uid')) == 'None' or str(request.args.get('name')) == 'None':
		return 'incorrect request⚠'
	if str(request.args.get('uid')) in baned_user:
		return "You are baned"
	if request.args.get('adminId') == adminId:
		with open("database.json", "r") as file:
			chat = json.load(file)
		return chat
	else:
		return "You don't have permission⚠"



@app.route("/sendFileUrl", methods=['GET',"POST"])
def postPhoto():
	name = request.args.get('name')
	if str(name) == 'None' or str(request.args.get('uid')) == 'None':
		return 'incorrect request⚠'
	if str(request.args.get('uid')) in baned_user:
		return "You are baned"
	with open("database.json", "r") as file:
		chat = json.load(file)
	if chat['onlyViewMode'] == 'on' and request.args.get('adminId') != adminId:
		return 'Вы не можете отправить сообщение, режим чата "Только просмотр"'
	else:
		urlFile = dict(request.form)['url']
		if urlFile[-3:] == 'mp3':
			messageType = '4'
		elif urlFile[-3:] == 'gif' or urlFile[-3:] == 'png' or urlFile[-4:] == 'jpeg' or urlFile[-3:] == 'jpg':
			messageType = "5"
		else:
			return 'File type not supported'
		for_json = {"name": name, "message": urlFile, "messageId": system.generateId(16), "messageType": messageType, "uid": str(request.args.get('uid'))}
		with open("database.json", "r") as file:
			chat = json.load(file)
		chat['chat'].append(for_json)
		with open("database.json", "w") as file:
			json.dump(chat,file)
		return "Succesful✅✔☑"


@app.route('/sendFile', methods=['GET',"POST"])
def saveFile():
	try:
		name = request.args.get('name')
		if str(name) == 'None' or str(request.args.get('uid')) == 'None':
			return 'incorrect request⚠'
		if str(request.args.get('uid')) in baned_user:
			return "You are baned"
		with open("database.json", "r") as file:
			chat = json.load(file)
		if chat['onlyViewMode'] == 'on' and request.args.get('adminId') != adminId:
			return 'Вы не можете отправить сообщение, режим чата "Только просмотр"'
		else:
			form = UploadFileForm()
			print(form)
			if form.validate_on_submit():
				file = form.file.data
				filename = secure_filename(file.filename)
				file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),UPLOAD_FOLDER,secure_filename(file.filename)))
				if filename[-3:] == 'mp3':
					messageType = '4'
				elif filename[-3:] == 'gif' or filename[-3:] == 'png' or filename[-4:] == 'jpeg' or filename[-3:] == 'jpg':
					messageType = "2"
				else:
					return 'File type not supported'
				for_json = {"name": name, "message": filename, "messageId": system.generateId(16), "messageType": messageType, "uid": str(request.args.get('uid'))}
				chat['chat'].append(for_json) 
				with open("database.json", "w") as file:
					json.dump(chat, file)
				return "Succesful✅✔☑"
			return render_template('sendFile.html', form=form, name=name, uid=request.args.get('uid'), adminId=request.args.get('adminId'))
	except:
		return 'File upload error'

@app.route('/banUser')
def ban():
	print(baned_user)
	if str(request.args.get('uid')) == 'None' or str(request.args.get('name')) == 'None' or str(request.args.get('banUid')) == 'None':
		return 'incorrect request⚠'
	if str(request.args.get('uid')) in baned_user:
		return "You are baned"
	if request.args.get('adminId') == adminId:
		if str(request.args.get('banUid')) in baned_user:
			return "This user is already banned✨"
		else:
			baned_user.append(str(request.args.get('banUid')))
			with open("database.json", "r") as file:
				chat = json.load(file)
			name = request.args.get('name')
			for_json = {"name": name, "message": f'{name} Забанил(а) пользователя', "messageId": system.generateId(16), "messageType": "1", "uid": str(request.args.get('uid'))}
			chat['chat'].append(for_json)
			with open("database.json", "w") as file:
				json.dump(chat, file)
			return "Succesful✅✔☑"
	else:
		return "You don't have permission⚠"


@app.route('/unbanUser')
def unban():
	if str(request.args.get('uid')) == 'None' or str(request.args.get('name')) == 'None' or str(request.args.get('unbanUid')) == 'None':
		return 'incorrect request⚠'
	if str(request.args.get('uid')) in baned_user:
		return "You are baned"
	if request.args.get('adminId') == adminId:
		if str(request.args.get('unbanUid')) not in baned_user:
			return "This user is not banned🛑"
		else:
			baned_user.remove(str(request.args.get('unbanUid')))
			with open("database.json", "r") as file:
				chat = json.load(file)
			name = request.args.get('name')
			for_json = {"name": name, "message": f'{name} Разбанил(а) пользователя', "messageId": system.generateId(16), "messageType": "1", "uid": str(request.args.get('uid'))}
			chat['chat'].append(for_json)
			with open("database.json", "w") as file:
				json.dump(chat, file)
			return "Succesful✅✔☑"
	else:
		return "You don't have permission⚠"


@app.route('/getUid')
def getUid():
	if str(request.args.get('uid')) == 'None' or str(request.args.get('name')) == 'None' or str(request.args.get('adminId')) == 'None':
		return 'incorrect request⚠'
	if str(request.args.get('uid')) in baned_user:
		return "You are baned"
	if request.args.get('adminId') != adminId:
		return "You don't have permission⚠"
	uids = 'Все пользователи, отправившие сообщение:<br>'
	for i in range(len(chat['chat'])):
		userName = chat['chat'][i]['name']
		userId = chat['chat'][i]['uid']
		if f'{userName}:     {userId}' in uids:
			pass
		else:
			uids = f'{uids}<br>{userName}:     {userId}'
	return f'<p>{uids}</p>'


app.run(debug=True, port=port, host=host)

#Made By Xsarz

#P.s: There are various "dirty moments" in the code, in which the code could be optimized, but I'll deal with that some other time (probably)
