

(function(){

    Sk.builtin.alert= new Sk.builtin.func(function(text) {
        alert(text.v);
    });
    goog.exportSymbol("Sk.builtin.alert", Sk.builtin.alert);
    Sk.builtins["alert"]=Sk.builtin.alert;

    Sk.builtin.prompt= new Sk.builtin.func(function(text,value) {
        return Sk.ffi.remapToPy(prompt(text.v,value.v));
    });
    goog.exportSymbol("Sk.builtin.prompt", Sk.builtin.prompt);
    Sk.builtins["prompt"]=Sk.builtin.prompt;


    Sk.builtin.cleanUpEvents= new Sk.builtin.func(function(text,value) {
        Sk.cleanUpEvents()
    });
    goog.exportSymbol("Sk.builtin.cleanUpEvents", Sk.builtin.cleanUpEvents);
    Sk.builtins["cleanUpEvents"]=Sk.builtin.cleanUpEvents;

})();
