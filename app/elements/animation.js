function animation() {

    var stage = this.stage = new PIXI.Stage(this.backgroundColor);
    var renderer = this.renderer = PIXI.autoDetectRenderer(this.width, this.height, {
        view: this.$.view,
        transparent: this.transparent,
        antialias: this.antialias,
        preserveDrawingBuffer: this.preserveDrawingBuffer,
        resolution: this.resolution
    });
    startAnimate=false;
    var spriteContainer = new PIXI.DisplayObjectContainer();
    var initTileGrid = this.initTileGrid = function(options) {

        if(options.gridWidth) this.gridWidth = options.gridWidth;
        if(options.gridHeight) this.gridHeight = options.gridHeight;
        if(options.tileSize) this.tileSize = options.tileSize;

        var canvasBackgroundTexture = PIXI.Texture.fromImage(options.canvasBackground);
        var canvasBackground = new PIXI.TilingSprite(canvasBackgroundTexture, this.width, this.height);

        var backgroundTexture = PIXI.Texture.fromImage(options.background);
        var background = new PIXI.TilingSprite(backgroundTexture, this.gridWidth * this.tileSize, this.gridHeight * this.tileSize);
        background.anchor.x = 0.5;
        background.anchor.y = 0.5;
        background.position.x = this.width / 2;
        background.position.y = this.height / 2;
        this.x0 = (this.width - background.width + this.tileSize) / 2;
        this.y0 = (this.height - background.height + this.tileSize) / 2;
        stage.removeChildren();
        stage.addChild(canvasBackground);
        stage.addChild(background);
    	stage.addChild(spriteContainer);
    	for (var name in options.spritesUrl){
    		loadSpriteTexture(name,options.spritesUrl[name]);
    	}
    	startAnimate=true;
    	requestAnimFrame(animate);
    }.bind(this);

    var createTileSprite = this.createTileSprite = function(texture, x, y) {
        var tileSprite = new PIXI.Sprite(texture);
        tileSprite.anchor.x = 0.5;
        tileSprite.anchor.y = 0.5;
        tileSprite.width = this.tileSize;
        tileSprite.height = this.tileSize;
        tileSprite.position.x = this.x0 + x * this.tileSize;
        tileSprite.position.y = this.y0 + y * this.tileSize;
        outerThis=this
        tileSprite.moveTo=function(x,y){
            this.position.x = outerThis.x0 + x * outerThis.tileSize;
            this.position.y = outerThis.y0 + y * outerThis.tileSize;
        }.bind(tileSprite)
        return tileSprite;
    }.bind(this);

    var resetCanvas=this.resetCanvas=function(){
        spriteContainer.removeChildren();
    }.bind(this);

    this.spriteTextures = {
    };

    var loadSpriteTexture=this.loadSpriteTexture=function(name,url){
    	this.spriteTextures[name]=PIXI.Texture.fromImage(url);
    }.bind(this);

    var addSprite = this.addSprite = function(name, x, y) {
        var sp=createTileSprite(this.spriteTextures[name], x, y)
        spriteContainer.addChild(sp);
        return sp;
    }.bind(this);

    var makeSprite = this.makeSprite = function(name, x, y) {
        return createTileSprite(this.spriteTextures[name], x, y);
    }.bind(this);

    var removeSprite = this.removeSprite = function(sprite) {
        spriteContainer.removeChild(sprite);
    };

    var removeAllSprites = this.removeAllSprites = function() {
        spriteContainer.removeChildren();
    };

    this.updateGrid= function (sprites){
        startAnimate=false;
        this.removeAllSprites();
        for (var name in sprites){
            this.addSprite(name,sprites[name].x,sprites[name].y);
        }
        startAnimate=true;
    }.bind(this);

    function animate() {

        renderer.render(stage);

        if(startAnimate) requestAnimFrame(animate);

    }

    (function(){


        Sprite=Sk.misceval.buildClass({"__name__":"animation"},function($gbl, $loc){

            $loc.__init__ = new Sk.builtin.func(function (self,name,x,y) {
                self.name=name.v;
                self.x=x.v;
                self.y=y.v;
                self.sprite=addSprite(self.name,self.x,self.y);

            });

            $loc.moveTo=new Sk.builtin.func(function(self,x,y){
                self.x=x.v;
                self.y=y.v;
                self.sprite.moveTo(self.x,self.y);
            });

            $loc.position=$loc.moveTo;

            $loc.hide=$loc.remove=new Sk.builtin.func(function(self){
                removeSprite(self.sprite);
            });

            $loc.show=$loc.putBack=new Sk.builtin.func(function(self){
                spriteContainer.addChild(self.sprite);
            });


        },"Sprite");

        Sk.builtin.Sprite=Sprite;
        goog.exportSymbol("Sk.builtin.Sprite", Sk.builtin.Sprite);
        Sk.builtins["Sprite"]=Sk.builtin.Sprite;


        Sk.builtin.removeAllSprites=function(){
            spriteContainer.removeChildren();
        }
        goog.exportSymbol("Sk.builtin.removeAllSprites", Sk.builtin.removeAllSprites);
        Sk.builtins["removeAllSprites"]=Sk.builtin.removeAllSprites;

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
}
