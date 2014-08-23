from flask import render_template, url_for, request, session, jsonify, redirect, flash
import pusher
from datetime import datetime
from time import time
from app import app, facebook


@app.route('/')
def index():
    if session.get('oauth_token'):
        return redirect(url_for('chat'))
    return render_template('main.html')


@app.route('/chat')
def chat():
    if not session.get('oauth_token'):
        flash('You have to login first.')
        return redirect(url_for('index'))
    return render_template('chat.html')


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get(
                                               'next') or request.referrer or None,
                                               _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        flash('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('index'))
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    session['username'] = me.data['name']
    session['user_id'] = me.data['id']
    return redirect(url_for('chat'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/pusher/auth', methods=['POST'])
def push_auth():
    p = pusher.Pusher(
        app_id='79303', key='fa9cb7cec3e2a3894ece', secret='a2d2e12e773f78d131b4')
    socket_id = request.form.get('socket_id')
    channel_name = request.form.get('channel_name')
    username = session['username']

    channel_data = {'user_info': {'username': username}}  # member.data
    channel_data['user_id'] = session['user_id']
    response = p[channel_name].authenticate(socket_id, channel_data)

    return jsonify(response)


@app.route('/send_msg', methods=['POST'])
def send_message():
    p = pusher.Pusher(
        app_id='79303', key='fa9cb7cec3e2a3894ece', secret='a2d2e12e773f78d131b4')

    msg = request.form.get('msg')  # message
    t = time()
    st = datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    username = session['username']
    user_id = session['user_id']
    p['presence-yyko'].trigger(
        'new_msg', {'msg': html_escape(msg), 'username': username, 'user_id': user_id, 'time': st})
    return jsonify(success=True)

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)
