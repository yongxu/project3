(function(){

    Sk.builtin.asyncLoop= new Sk.builtin.func(function(f,delay) {

        id=setInterval(function(){
            Sk.misceval.callsimOrSuspend(f);
        },Sk.ffi.remapToJs(delay)*1000);
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

        return setTimeout(function(){
            Sk.misceval.callsimOrSuspend(f);
        },Sk.ffi.remapToJs(delay)*1000);

    });
    goog.exportSymbol("Sk.builtin.async", Sk.builtin.async);
    Sk.builtins["async"]=Sk.builtin.async;


    Sk.builtin.clearAsync= new Sk.builtin.func(function(id) {
        clearTimeout(id);
    });
    goog.exportSymbol("Sk.builtin.clearAsync", Sk.builtin.clearAsync);
    Sk.builtins["clearAsync"]=Sk.builtin.clearAsync;

})();