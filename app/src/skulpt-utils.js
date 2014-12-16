

(function(){

    Sk.builtin.alert= new Sk.builtin.func(function(text) {
        alert(text.v);
    });
    goog.exportSymbol("Sk.builtin.alert", Sk.builtin.alert);
    Sk.builtins["alert"]=Sk.builtin.alert;

})();
