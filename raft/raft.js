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
const networkLatency = 40

const numNodes = 5

var msgIdSeq = 0

var ctx = null;
var data = {
  nodes: [],
  msgs: [],
}
// raft 协议
function initData() {
  console.log('initData')
  for(var i=0; i<numNodes; i++) {
    var now = Date.now()
    // 初始化节点
    data.nodes.push({
      currentTerm: 0,
      votedFor: null,
      log: [],
      commitIndex: 0,
      lastApplied: 0,
      lastLogTerm: 0,

      nextIndex: [],
      matchIndex: [],
      state: RAFT_FOLLOWER,
      hbTS: now,
      timeout: now + heartbeatTimeoutRange[0] + Math.random()*(heartbeatTimeoutRange[1] - heartbeatTimeoutRange[0]),
    })
  }
}

function onHeartbeat(node) {
  node.hbTS = Date.now()
  node.timeout = node.hbTS + heartbeatTimeoutRange[0] + Math.random()*(heartbeatTimeoutRange[1] - heartbeatTimeoutRange[0])
}

function onStateChange(node, state) {
  if(state == node.state) {
    return
  }
  node.state = state
  if(state==RAFT_LEADER) {
    // become leader
    node.timeout = Number.MAX_VALUE
    appendEntriesRPC(node)
    node.timer = setInterval(function() {
      appendEntriesRPC(node)
    }, 500)
  } else {
    if(node.timer != null) {
      clearTimeout(node.timer)
    }
  }
}

function appendEntriesRPC(node) {
  broadcastMsg(node, 'AppendEntries', {
    term: node.currentTerm,
    leaderId: node.id,
  }, function(res){

  })
}

function sendMsg(msg, callback) {
  // RPC from client
  msg.id = ++msgIdSeq
  msg.x = msg.from.x
  msg.y = msg.from.y
  msg.velocity = {
    x: (msg.to.x - msg.from.x) / networkLatency,
    y: (msg.to.y - msg.from.y) / networkLatency,
  }
  msg.callback = callback
  data.msgs.push(msg)
}

function onMessage(node, msg) {
  for(var i = 0; i < data.msgs.length; i++) {
    if(data.msgs[i].id == msg.id) {
      data.msgs.splice(i,1)
      break
    }
  }
  if(msg.args.term > node.currentTerm) {
    onStateChange(node, RAFT_FOLLOWER)
    onHeartbeat(node)
  }
  // RPC server handler
  if(msg.cmd=='AppendEntries') {
    onHeartbeat(node)
  } else if(msg.cmd=='RequestVote') {
    if(msg.args.term > node.currentTerm) {
      console.log('onRequestVote', msg)
      node.votedFor = msg.args.candidateId
      node.currentTerm = msg.args.term
      msg.callback({term:node.currentTerm, voteGranted:true})
    } else if(msg.args.term == node.currentTerm && msg.args.candidateId == node.votedFor) {
      msg.callback({term:node.currentTerm, voteGranted:true})
    } else {
      msg.callback({term:node.currentTerm, voteGranted:false})
    }
  }
}

function broadcastMsg(node, cmd, args, callback) {
  data.nodes.forEach(function (toNode, j) {
    if (j == node.id) return;
    sendMsg({
      from: node,
      to: toNode,
      cmd: cmd,
      args: args,
    }, callback)
  })
}

function updateNode(node) {
  // 如果超过一定时间没有收到心跳，则进入选举状态
  if(node.timeout == null) {
    // 初始化心跳
    onHeartbeat(node)
  }
  if(Date.now() > node.timeout) {
    // 超时，进入选举状态，发送选举消息
    node.state = RAFT_CANDIDATE
    node.currentTerm++
    // vote for self
    node.votedFor = node.id
    node.gotVotes = 1
    node.timeout = Date.now() + 1500 + Math.random() * 1500
    broadcastMsg(node, 'RequestVote', {
      term: node.currentTerm,
      candidateId: node.id,
      lastLogIndex: node.lastApplied,
      lastLogTerm: node.lastLogTerm,
    }, function (res) {
      if (res.term > node.currentTerm) {
        onStateChange(node, RAFT_FOLLOWER)
        return
      }
      if (res.voteGranted) {
        if (++node.gotVotes > numNodes / 2) {
          // 转换为leader
          onStateChange(node, RAFT_LEADER)
        }
      }
    })
  }
}

// update
function update() {
  for(var i=0;i<data.msgs.length;i++) {
    var msg = data.msgs[i]
    msg.x += msg.velocity.x
    msg.y += msg.velocity.y
    if(Math.abs(msg.x-msg.to.x) < 10 && Math.abs(msg.y-msg.to.y) < 10) {
      onMessage(msg.to, msg)
    }
  }
  for(var i = 0; i < data.nodes.length; i++) {
    var node = data.nodes[i]
    node.id = i
    updateNode(node)
  }
}

// render logics
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
    ctx.fillStyle = node_colors[node.state]
    ctx.strokeStyle = node_strokes[node.state]
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
    ctx.font = '30px serif'
    ctx.fillStyle = '#001122'
    ctx.fillText(''+node.term, node.x, node.y)
  }
  for(var i = 0; i < data.msgs.length; i++) {
    var msg = data.msgs[i]
    ctx.beginPath()
    if(msg.cmd == 'RequestVote') {
      ctx.fillStyle = '#f743fa'
    } else {
      ctx.fillStyle = '#77ff77'
    }
    ctx.arc(msg.x,msg.y,msg_radius, 0, Math.PI*2)
    ctx.fill()
    msg.text = msg.args.term
    if(msg.text) {
      ctx.font = "24px Sans"
      ctx.fillStyle = '#0388fc'
      var tsize = ctx.measureText(msg.text)
      ctx.fillText(msg.text, msg.x - tsize.width/2, msg.y)
    }
  }
}

var started = false
function startGame() {
  if(started) return
  started = true
  var canvas = document.getElementById("canvas")
  ctx = canvas.getContext("2d")
  initData()
  setInterval(function(){
    update()
    render()
  }, 30)
}
