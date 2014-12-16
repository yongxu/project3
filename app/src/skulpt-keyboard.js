(function(){

    if(!Sk.cleanUpEventList) Sk.cleanUpEventList=[];
    if(!Sk.cleanUpEvents) Sk.cleanUpEvents=function(){
        if(Sk.cleanUpEventList)
            for(var i in Sk.cleanUpEventList){
                Sk.cleanUpEventList[i]();
            }
    };
    Sk.builtin.keydown= new Sk.builtin.func(function(f) {

        function kd(event){
            var key = event.keyCode || event.which;
            if(event.keyIdentifier=="U+0020" || event.keyIdentifier=="Up" || event.keyIdentifier=="Down" ||
                event.keyIdentifier=="Right" || event.keyIdentifier=="Left")
                event.preventDefault();
            Sk.misceval.callsimOrSuspend(f,Sk.ffi.remapToPy(event.keyCode),Sk.ffi.remapToPy(event.keyIdentifier));
        }

        Sk.cleanUpEventList.push(function(){
            window.removeEventListener("keydown",kd);
        });

        return window.addEventListener("keydown",kd);

    });
    goog.exportSymbol("Sk.builtin.keydown", Sk.builtin.keydown);
    Sk.builtins["keydown"]=Sk.builtin.keydown;
    
})();