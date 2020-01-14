'''
Channel function endpoints
'''
from json import dumps
from flask import Blueprint, request, abort
channel = Blueprint('channel', __name__)
import functions.channel

#curl "127.0.0.1:5000/channels/list?token=token"
@channel.route('/channels/list', methods=['GET'])
def channelslist():
    return dumps(functions.channel.channels_list(request.args.get('token')))

#curl "127.0.0.1:5000/channels/listall?token=token"
@channel.route('/channels/listall', methods=['GET'])
def channelslistall():
    return dumps(functions.channel.channels_listall(request.args.get('token')))

#curl -X POST 127.0.0.1:5000/channels/create -F token=token -F name=channelName -F is_public=True
@channel.route('/channels/create', methods=['POST'])
def channelscreate():
    return dumps(functions.channel.channels_create(request.form.get('token'), request.form.get('name'), request.form.get('is_public')))

@channel.route('/channel/invite', methods=['POST'])
def channelinvite():
    return dumps(functions.channel.channel_invite(request.form.get('token'), request.form.get('channel_id'), request.form.get('u_id')))

@channel.route('/channel/join', methods=['POST'])
def channeljoin():
    return dumps(functions.channel.channel_join(request.form.get('token'), request.form.get('channel_id')))

@channel.route('/channel/leave', methods=['POST'])
def channelleave():
    return dumps(functions.channel.channel_leave(request.form.get('token'), request.form.get('channel_id')))

@channel.route('/channel/messages', methods=['GET'])
def channelmessage():
    return dumps(functions.channel.channel_messages(request.args.get('token'), request.args.get('channel_id'), request.args.get('start')))

@channel.route('/search', methods=['GET'])
def searchmessages():
    return dumps(functions.channel.search(request.args.get('token'), request.args.get('query_str')))

@channel.route('/channel/details', methods=['GET'])
def channeldetails():
    return dumps(functions.channel.channel_details(request.args.get('token'), request.args.get('channel_id')))

@channel.route('/channel/addowner', methods=['POST'])
def channeladdowner():
    return dumps(functions.channel.channel_addowner(request.form.get('token'), request.form.get('channel_id'), request.form.get('u_id')))

@channel.route('/channel/removeowner', methods=['POST'])
def channelremoveowner():
    return dumps(functions.channel.channel_removeowner(request.form.get('token'), request.form.get('channel_id'), request.form.get('u_id')))
