(function(){

    Sk.builtin.keydown= new Sk.builtin.func(function(f) {

        return window.addEventListener("keydown",function(event){
            var key = event.keyCode || event.which;
            if(event.keyIdentifier=="U+0020" || event.keyIdentifier=="Up" || event.keyIdentifier=="Down" ||
                event.keyIdentifier=="Right" || event.keyIdentifier=="Left")
                event.preventDefault();
            Sk.misceval.callsimOrSuspend(f,Sk.ffi.remapToPy(event.keyCode),Sk.ffi.remapToPy(event.keyIdentifier));
        });

    });
    goog.exportSymbol("Sk.builtin.keydown", Sk.builtin.keydown);
    Sk.builtins["keydown"]=Sk.builtin.keydown;
    
})();