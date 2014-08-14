(function (window , undefined){

    var Shake = {
        support : undefined ,

        SHAKE_THRESHOLD : 3000 , //摇动速度阀值

        TIME_THRESHOLD  : 100  , //监测时间阀值

        init : function (opts){
            var self = this;

            opts.support = opts.support ? opts.support : function (){};
            opts.unsupport = opts.unsupport ? opts.unsupport : function (){};  
            this.checkCallback(opts.support , opts.unsupport) ;

            this.shaking_callback = opts.shaking_callback ? opts.shaking_callback : function (){}    

            if (this.support){
                window.addEventListener('devicemotion', function (eventData){
                    self.deviceMotionHandler.call(self , eventData);
                }, false);
            }     
        } , 

        checkCallback : function (supportCallback , unsupportCallback){
            if (window.DeviceMotionEvent) {
                this.support = true;

                supportCallback();
            }
            else{
                this.support = false;  
                unsupportCallback();      
            }
        } , 

        deviceMotionHandler : (function (){
            var lastUpdate = 0;
            // 紧接着定义x、y、z记录三个轴的数据以及上一次出发的时间
            var x;
            var y;
            var z;
            var lastX;
            var lastY;
            var lastZ;

            return function (eventData){
                var self = this;

                // 获取含重力的加速度
　　　　        var acceleration = eventData.accelerationIncludingGravity; 
                // 获取当前时间
            　　var curTime = new Date().getTime(); 
            　　var diffTime = curTime - lastUpdate;

            　　if (diffTime > 100) {
                    lastUpdate = curTime; 

            　　　　x = acceleration.x; 
            　　　　y = acceleration.y; 
            　　　　z = acceleration.z; 

            　　　　var speed = Math.abs(x + y + z - lastX - lastY - lastZ) / diffTime * 10000; 
            　　　　if (speed > self.SHAKE_THRESHOLD) { 
            　　　　　　self.shaking_callback(eventData);
            　　　　}

            　　　　lastX = x; 
            　　　　lastY = y; 
            　　　　lastZ = z; 
            　　}                 
            };
        })()
    } ; 

    window.Shake = Shake;
    
})(window);