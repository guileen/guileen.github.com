document.onreadystatechange = function() {
  startGame()
}
const node_radius = 30
const timeout_width = 5
const msg_radius = 10
const sw = 800
const sh = 400

const RAFT_FOLLOWER = 0
const RAFT_CANDIDATE = 1
const RAFT_LEADER = 2
var node_colors = ['#baf5ff', '#03d7fc', '#00aaff']
var node_strokes = ['#baf5ff', '#fce303', '#000000']

const heartbeatInterval = 50
const heartbeatTimeoutRange = [1500, 3000]
const networkLatency = 150

var msgIdSeq = 0

var ctx = null;
var data = {
  nodes: [
    {
      nodeState: RAFT_FOLLOWER,
    },
    {
      nodeState: RAFT_CANDIDATE,
    },
    {
      nodeState: RAFT_LEADER,
    }
  ],
  msgs: [],
}

function onHeartbeat(node) {
  console.log('onHeartbeat', node)
  node.hbTS = Date.now()
  node.timeout = node.hbTS + heartbeatTimeoutRange[0] + Math.random()*(heartbeatTimeoutRange[1] - heartbeatTimeoutRange[0])
}

function sendMsg(msg) {
  msg.id = ++msgIdSeq
  msg.x = msg.from.x
  msg.y = msg.from.y
  msg.velocity = {
    x: (msg.to.x - msg.from.x) / networkLatency,
    y: (msg.to.y - msg.from.y) / networkLatency,
  }
  data.msgs.push(msg)
}

function onMessage(msg) {
  for(var i = 0; i < data.msgs.length; i++) {
    if(data.msgs[i].id == msg.id) {
      data.msgs.splice(i,1)
      break
    }
  }
}

function updateNode(node) {
  if(node.isCandidating) {
    return
  }
  // 如果超过一定时间没有收到心跳，则进入选举状态
  if(node.timeout == null) {
    // 初始化心跳
    onHeartbeat(node)
  }
  if(Date.now() > node.timeout) {
    // 超时，进入选举状态，发送选举消息
    node.isCandidating = true
    for(var j = 0; j < data.nodes.length; j++) {
      if (j==node.id) continue;
      sendMsg({
        from: node,
        to: data.nodes[j],
        text: "hello world",
      })
    }
  }
}

function update() {
  for(var i=0;i<data.msgs.length;i++) {
    var msg = data.msgs[i]
    msg.x += msg.velocity.x
    msg.y += msg.velocity.y
    if(Math.abs(msg.x-msg.to.x) < 10 && Math.abs(msg.y-msg.to.y) < 10) {
      onMessage(msg)
    }
  }
  for(var i = 0; i < data.nodes.length; i++) {
    var node = data.nodes[i]
    node.id = i
    updateNode(node)
  }
}

function render() {
  var nodes = data.nodes
  var round_radius = Math.min(sw/2,sh/2) - node_radius - timeout_width - 10
  ctx.clearRect(0,0,sw,sh)
  // draw round circle
  ctx.beginPath()
  ctx.lineWidth = 5
  ctx.strokeStyle = '#eeeeee'
  ctx.arc(sw/2,sh/2,round_radius, 0, Math.PI*2)
  ctx.stroke()
  ctx.lineWidth = 5
  var ts = Date.now()
  for(var i = 0; i < nodes.length; i++) {
    var node = nodes[i]
    var positionAngle = -Math.PI/2 + i * Math.PI * 2 / nodes.length
    node.x = sw/2 + Math.cos(positionAngle) * round_radius
    node.y = sh/2 + Math.sin(positionAngle) * round_radius
    // draw circle
    ctx.beginPath()
    ctx.fillStyle = node_colors[node.nodeState]
    ctx.strokeStyle = node_strokes[node.nodeState]
    ctx.arc(node.x,node.y,node_radius,0,Math.PI*2)
    ctx.fill()
    ctx.stroke()
    // draw timeout
    // console.log(ts, node.hbTS, node.timeout)
    var percent = (ts-node.hbTS) / (node.timeout - node.hbTS)
    ctx.beginPath()
    ctx.strokeStyle = '#888888'
    ctx.arc(node.x,node.y,node_radius + timeout_width , -Math.PI/2, -Math.PI/2 + (percent) * Math.PI * 2)
    ctx.stroke()
  }
  for(var i = 0; i < data.msgs.length; i++) {
    var msg = data.msgs[i]
    ctx.beginPath()
    ctx.fillStyle = '#f743fa'
    ctx.arc(msg.x,msg.y,msg_radius, 0, Math.PI*2)
    ctx.fill()
    if(msg.text) {
      ctx.font = "24px Sans"
      ctx.fillStyle = '#0388fc'
      var tsize = ctx.measureText(msg.text)
      ctx.fillText(msg.text, msg.x - tsize.width/2, msg.y)
    }
  }
}

function startGame() {
  var canvas = document.getElementById("canvas")
  ctx = canvas.getContext("2d")
  setInterval(function(){
    update()
    render()
  }, 30)
}
