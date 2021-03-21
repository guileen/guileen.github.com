document.onreadystatechange = function() {
  startGame()
}
const node_radius = 30
const timeout_width = 5
const sw = 800
const sh = 400

const RAFT_FOLLOWER = 0
const RAFT_CANDIDATE = 1
const RAFT_LEADER = 2
var node_colors = ['#baf5ff', '#03d7fc', '#00aaff']
var node_strokes = ['#baf5ff', '#fce303', '#000000']

const heartbeatInterval = 50
const heartbeatTimeoutRange = [1500, 3000]

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
}

function onHeartbeat(node) {
  console.log('onHeartbeat', node)
  node.hbTS = Date.now()
  node.timeout = node.hbTS + heartbeatTimeoutRange[0] + Math.random()*(heartbeatTimeoutRange[1] - heartbeatTimeoutRange[0])
}

function updateNode(i, node) {
  console.log('udpateNode', node)
  if(node.isCandidating) {

  }
  // 如果超过一定时间没有收到心跳，则进入选举状态
  if(node.timeout == null) {
    // 初始化心跳
    onHeartbeat(node)
  }
  if(Date.now() > node.timeout) {
    // 超时，进入选举状态，发送选举消息
  }
}

function update() {
  for(var i = 0; i < data.nodes.length; i++) {
    updateNode(i, data.nodes[i])
  }
}

function render() {
  var nodes = data.nodes
  var round_radius = Math.min(sw/2,sh/2) - node_radius - timeout_width - 10
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
    var x = sw/2 + Math.cos(positionAngle) * round_radius
    var y = sh/2 + Math.sin(positionAngle) * round_radius
    // draw circle
    ctx.beginPath()
    ctx.fillStyle = node_colors[node.nodeState]
    ctx.strokeStyle = node_strokes[node.nodeState]
    ctx.arc(x,y,node_radius,0,Math.PI*2)
    ctx.fill()
    ctx.stroke()
    // draw timeout
    // console.log(ts, node.hbTS, node.timeout)
    var percent = (ts-node.hbTS) / (node.timeout - node.hbTS)
    console.log("percent", percent)
    ctx.beginPath()
    ctx.strokeStyle = '#888888'
    ctx.arc(x,y,node_radius + timeout_width , -Math.PI/2, -Math.PI/2 + (percent) * Math.PI * 2)
    ctx.stroke()
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
