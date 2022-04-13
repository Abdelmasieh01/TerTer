const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/socket/'
    )

    function like(tweet_id){
        socket.send(JSON.stringify({
            'tweet_id': tweet_id
        }));
    }
 
    socket.onmessage = function(event){
        let data = JSON.parse(event.data)
        if (data['count'] != null){
            document.getElementById('react'+data['id']).innerHTML = '    ' + data['count']
        }
    }