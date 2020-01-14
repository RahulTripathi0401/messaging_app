from json import dumps
from flask import Blueprint, request, abort
message=Blueprint('message', __name__)
import functions.standup
import functions.message

@message.route('/message/send', methods=['POST'])
def messagesend():
    return dumps(functions.message.message_send(request.form.get('token'), request.form.get('channel_id'), request.form.get('message')))

@message.route('/message/sendlater', methods=['POST'])
def messagesendlater():
    return dumps(functions.message.message_sendlater(request.form.get('token'), request.form.get('channel_id'), request.form.get('message'), request.form.get('time_sent')))

@message.route('/standup/start', methods=['POST'])
def standupstart():
    return dumps(functions.standup.standup_start(request.form.get('token'), request.form.get('channel_id'), request.form.get('length')))

@message.route('/message/remove', methods=['DELETE'])
def messageremove():
    return dumps(functions.message.message_remove(request.form.get('token'), request.form.get('message_id')))

@message.route('/standup/send', methods=['POST'])
def standupsend():
    return dumps(functions.standup.standup_send(request.form.get('token'), request.form.get('channel_id'), request.form.get('message')))

@message.route('/message/edit', methods=['PUT'])
def messageedit():
    return dumps(functions.message.message_edit(request.form.get('token'), request.form.get('message_id'), request.form.get('message')))

@message.route('/message/react', methods=['POST'])
def messagereact():
    return dumps(functions.message.message_react(request.form.get('token'), request.form.get('message_id'), request.form.get('react_id')))

@message.route('/message/unreact', methods=['POST'])
def messageunreact():
    return dumps(functions.message.message_unreact(request.form.get('token'), request.form.get('message_id'), request.form.get('react_id')))

@message.route('/message/pin', methods=['POST'])
def messagepin():
    return dumps(functions.message.message_pin(request.form.get('token'), request.form.get('message_id')))

@message.route('/message/unpin', methods=['POST'])
def messageunpin():
    return dumps(functions.message.message_unpin(request.form.get('token'), request.form.get('message_id')))

@message.route('/standup/active', methods=['GET'])
def standupactive():
    return dumps(functions.standup.standup_active(request.args.get('token'), request.args.get('channel_id')))
