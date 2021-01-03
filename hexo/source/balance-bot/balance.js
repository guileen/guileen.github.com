var ballsCount;
var ballsStatus = new Array();
var balls = new Array(new Array(),new Array(),new Array());
var lenballs = new Array(0,0,0);

function setBallsCount(num){
	ballsCount=num;
	for(var i=0;i<num;i++){
		ballsStatus[i] = 0;
		balls[0][i] = i;
	}
	lenballs[0]=num;
}
var tianpinStatus;
function judge(){
	switch(tianpinStatus){
	case 0:

		for(var i=0;i<lenballs[1];i++)
			ballsStatus[balls[1][i]] = 3;
		for(var i=0;i<lenballs[2];i++)
			ballsStatus[balls[2][i]] = 3;
		break;
	case 1:

		for(var i=0;i<lenballs[1];i++){
			if(ballsStatus[balls[1][i]]==2)
				ballsStatus[balls[1][i]]=3;
			else if(ballsStatus[balls[1][i]]==0)
				ballsStatus[balls[1][i]]=1;
		}
		for(var i=0;i<lenballs[2];i++){
			if(ballsStatus[balls[2][i]]==1)
				ballsStatus[balls[2][i]]=3;
			else if(ballsStatus[balls[2][i]]==0)
				ballsStatus[balls[2][i]]=2;
		}
		for(var i=0;i<lenballs[0];i++)
			ballsStatus[balls[0][i]]=3;
		break;
	case 2:

		for(var i=0;i<lenballs[1];i++){
			if(ballsStatus[balls[1][i]]==1)
				ballsStatus[balls[1][i]]=3;
			else if(ballsStatus[balls[1][i]]==0)
				ballsStatus[balls[1][i]]=2;
		}
		for(var i=0;i<lenballs[2];i++){
			if(ballsStatus[balls[2][i]]==2)
				ballsStatus[balls[2][i]]=3;
			else if(ballsStatus[balls[2][i]]==0)
				ballsStatus[balls[2][i]]=1;
		}
		for(var i=0;i<lenballs[0];i++)
			ballsStatus[balls[0][i]]=3;
		break;
	}
}

function decide(){

		var C=0;//possible=c[0]+c[1]+c[2]
		var c=new Array(0,0,0,0,0,0);
		for(var i=ballsCount-1;i>=0;i--){
			c[ballsStatus[i]]++;
			if(ballsStatus[i]>=0 && ballsStatus[i] <=2)
				C++;
		}
		
		if(C==0)
			return -1;
		else if(C==1)
			return 1;
		resetTianpin();
	
		var l=0,r=0;
		if(C==2){
			moveBallTo(pickBallByStatus(-1),1);
			moveBallTo(pickBallByStatus(3),2);
		}

		else if(C==c[0]){

			if(C==5 && ballsCount>5){
				l=2;
				r=1;
				moveBallTo(pickBallByStatus(3),2);
			}
			else{
				l=mydiv(C+1,3);
				r=l;
			}
			for(var i=0;i<l;i++){
				moveBallTo(pickBallByStatus(0),1);
			}
			for(var i=0;i<r;i++){
				moveBallTo(pickBallByStatus(0),2);
			}
		}
		else{

			var t=mydiv(C+1,3);
			var y=C-2*t;
			t=(c[1]>c[2])?2:1;
			if(y<=c[t]){
				c[t]-=y;
				C-=y;
			}
			else{
				c[t==1?2:1]-=(y-c[t]);
				c[t]=0;
				C-=y;
			}
			l=mydiv(c[1],2);
			r=c[1]-l;
			for(var i=0;i<l;i++){
				moveBallTo(pickBallByStatus(1),1);
			}
			for(var i=0;i<r;i++){
				moveBallTo(pickBallByStatus(1),2);
			}
			r=mydiv(c[2],2);
			l=c[2]-r;
			for(var i=0;i<l;i++){
				moveBallTo(pickBallByStatus(2),1);
			}
			for(var i=0;i<r;i++){
				moveBallTo(pickBallByStatus(2),2);
			}
		}
		return 0;		
}

function mydiv(i,j){
	return (i-i%j)/j
}

function pickBallByStatus(stat){
	var ret=-1;
	if(stat==-1){

		for(var i=0;i<lenballs[0];i++){
			if (ret!=-1)
				balls[0][i]=balls[0][i+1];
			else if ( ballsStatus[balls[0][i]] == 0){
				lenballs[0]--;
				ret=balls[0][i];
				balls[0][i]=balls[0][i+1];
			}
		}
		if(ret!=-1){

			return ret;
		}
	}
	for (var i = 0; i < lenballs[0]; i++) {
		var bs = ballsStatus[balls[0][i]];
		if (ret!=-1)
			balls[0][i]=balls[0][i+1];
		else if ((stat == -1 && bs >= 0 && bs <= 2)||(bs == stat)){
			lenballs[0]--;
			ret= balls[0][i];
			balls[0][i]=balls[0][i+1];
		}
	}
	return ret;
}

function moveBallTo(b,pos){
	balls[pos][lenballs[pos]]=b;
	lenballs[pos]++;
}

function resetTianpin(){
	for(var i=0;i<ballsCount;i++){
		balls[0][i]=i;
	}
	lenballs[0]=ballsCount;
	lenballs[1]=0;
	lenballs[2]=0;
}

function getBallsAt(pos){
	var ret="";
	ret=balls[pos][0]+1;
	for(var i=1;i<lenballs[pos];i++)
		ret=ret+", "+(balls[pos][i]+1);
	return ret;
}
function getAnswer(){
	for(var i=0;i<ballsCount;i++){
		if(ballsStatus[i] == 0){
			return "答案是"+(i+1)+"号球";
		}else if(ballsStatus[i] == 1||ballsStatus[i] == 4){
			return "答案是"+(i+1)+"号球，并且此球是重球";
		}if(ballsStatus[i] == 2||ballsStatus[i] == 5){
			return "答案是"+(i+1)+"号球，并且此球是轻球";
		}
	}
	if(ret!=-1){
		return ret;
	}	
}
function showBalls(){
	var e="";
	for(var i=0;i<ballsCount;i++)
		e=e+ballsStatus[i]+",";
	println("状态："+e);
	for(var i=0;i<3;i++){
		e="";
		for(var j=0;j<lenballs[i];j++)
			e=e+balls[i][j]+",";
		println("位置"+i+"上"+e);
	}
}
