$(document).ready(function () {
	pusher = new Pusher('fa9cb7cec3e2a3894ece');
	my_channel = pusher.subscribe('presence-yyko');
	
	my_channel.bind('pusher:subscription_succeeded', function(members){ 
		console.log('subscription success!!');
		members.each(function(member){
			$('#members').append('<li id="member_' + member.id +'">' + member.info.username + '</li>');
		})	
	})
	my_channel.bind('pusher:member_added', function(member){ 
		console.log('Member added');
		$('#chat-table').append('<tr><td colspan=2>' + member.info.username + '님이 입장하셨습니다.</td></tr>');
		$('#members').append('<li id="member_' + member.id +'">' + member.info.username +  '</li>');
		scrollToBottom();
	})
	my_channel.bind('pusher:member_removed', function(member){ 
		console.log('Member removed');
		$('#chat-table').append('<tr><td colspan=2>' + member.info.username + '님이 퇴장하셨습니다.</td></tr>');
		$('#member_'+member.id).remove();
		scrollToBottom();

	})
	my_channel.bind('new_msg', function(data){ 
		$('#chat-table').append('<tr><td style="width: 50px;padding-right: 8px;"><img src="http://graph.facebook.com/' + data.user_id + '/picture"></td><td><p><strong>' + data.username + ': </strong>' + data.msg + '</p><small>'+ data.time + '</small></td></tr>');
		scrollToBottom();
	})
	$('#chat-btn').click(function(){
		$.ajax({
			url: '/send_msg',
			type: 'POST',
			dataType: 'JSON',
			data:{
				msg: $('#chatting').val()
			},
			success: function(data) {
				if(data.success){
					username = data.username;
					$('#chatting').val("");
					console.log('send msg success!');
				}
				else{
					console.log('send msg fail!');
				}
			},
			error: function(data) {
				console.log('Server error!');
			}	
		})
	})
	$('#chatting').keypress(function(e) {
		if (e.keyCode == 13) {
			e.preventDefault();
			$('#chat-btn').trigger('click');
			return false;
		}
	});
});

function scrollToBottom() {
	$('#chat-pannel').scrollTop($('#chat-room').height());
}
