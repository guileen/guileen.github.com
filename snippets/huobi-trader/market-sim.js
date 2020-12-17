var env = {
    tick: 0,
    price: 1,
    targets: [], // [{tick:100, target:2}],
    cycleTimes: [4,13,50,200], // [6, 30, 300, 700], 3~10个小周期为一大周期, 隐藏变量，待发现。
    deltas: [0.1,0.3,0.5,1],
    tickMaxDelta: 0.1,
    // delta 分布概率, 更准确
}

function genTargetTick(deltaTick, deltaRange) {
    var delta = 1 + (Math.random() * 2 - 1) * deltaTick

    var targetOffset = 0
    if(env.targets.length>0) {
        var first = env.targets[0]
        targetOffset = (first.target-env.price) * deltaTick / (first.tick - env.tick)
    }

    // console.log(deltaTick, delta, targetOffset)

    env.targets.unshift({
        tick: env.tick + deltaTick,
        target: env.price * delta + targetOffset,
    })
}

function genTickPrice() {
    if(env.targets.length==0) {
        // max cycle target
        var deltaTick = env.cycleTimes[env.cycleTimes.length - 1]
        genTargetTick(deltaTick, env.deltas[env.cycleTimes.length-1])
    }
    env.tick += 1
    if(env.targets[0].tick == env.tick) {
        env.price =  env.targets[0].target
        env.targets.shift()
        return
    }
    // gen next cycle target
    for(var i=env.cycleTimes.length-1;i>=0;i--) {
        var dtick = env.targets[0].tick - env.tick
        if(dtick>env.cycleTimes[i]) {
            genTargetTick(env.cycleTimes[i], env.deltas[i])
        }
    }
    env.price = env.price * (1+Math.random()* 2 * env.tickMaxDelta - env.tickMaxDelta) + (env.targets[0].target-env.price)/2
}

for(var i = 0; i < 100; i++) {
    genTickPrice()
    // console.log(env.tick, env.price, env.targets)
    console.log(env.tick, env.price)
}