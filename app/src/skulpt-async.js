(function(){

    if(!Sk.cleanUpEventList) Sk.cleanUpEventList=[];
    if(!Sk.cleanUpEvents) Sk.cleanUpEvents=function(){
        if(Sk.cleanUpEventList)
            for(var i in Sk.cleanUpEventList){
                Sk.cleanUpEventList[i]();
            }
    };

    Sk.builtin.asyncLoop= new Sk.builtin.func(function(f,delay) {

        var id=setInterval(function(){
            Sk.misceval.callsimOrSuspend(f);
        },Sk.ffi.remapToJs(delay)*1000);

        Sk.cleanUpEventList.push(function(){
            clearInterval(id);
        });
        return id;
    });
    goog.exportSymbol("Sk.builtin.asyncLoop", Sk.builtin.asyncLoop);
    Sk.builtins["asyncLoop"]=Sk.builtin.asyncLoop;


    Sk.builtin.clearAsyncLoop= new Sk.builtin.func(function(id) {
        clearInterval(id);
    });
    goog.exportSymbol("Sk.builtin.clearAsyncLoop", Sk.builtin.clearAsyncLoop);
    Sk.builtins["clearAsyncLoop"]=Sk.builtin.clearAsyncLoop;



    Sk.builtin.async= new Sk.builtin.func(function(f,delay) {
        var id=setTimeout(function(){
            Sk.misceval.callsimOrSuspend(f);
        },Sk.ffi.remapToJs(delay)*1000);
        return id;

        Sk.cleanUpEventList.push(function(){
            clearTimeout(id);
        });
    });
    goog.exportSymbol("Sk.builtin.async", Sk.builtin.async);
    Sk.builtins["async"]=Sk.builtin.async;


    Sk.builtin.clearAsync= new Sk.builtin.func(function(id) {
        clearTimeout(id);
    });
    goog.exportSymbol("Sk.builtin.clearAsync", Sk.builtin.clearAsync);
    Sk.builtins["clearAsync"]=Sk.builtin.clearAsync;

})();