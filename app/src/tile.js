function tile(canvas,options) {

    var options=typeof options !== 'undefined' && options !== null ?options:{};


    var stage = this.stage = new PIXI.Stage(options.backgroundColor);
    var renderer = PIXI.autoDetectRenderer(options.width || canvas.width,options.height ||  canvas.height, {
        view: canvas,
        transparent: options.transparent || false ,
        antialias: options.antialias!== 'undefined'? options.antialias:true,
        preserveDrawingBuffer: options.preserveDrawingBuffer || false,
        resolution: options.resolution || 1
    });
    var startAnimate=false;
    var spriteContainer = new PIXI.DisplayObjectContainer();

    var gridWidth = options.gridWidth || 21,
    gridHeight = options.gridHeight || 21,
    tileSize = options.tileSize || Math.min(canvas.width/(gridWidth+1),canvas.height/(gridHeight+1));

    var canvasBackground;
    if(options.canvasBackground){
        var canvasBackgroundTexture = PIXI.Texture.fromImage(options.canvasBackground);
        canvasBackground = new PIXI.TilingSprite(canvasBackgroundTexture, canvas.width, canvas.height);
        stage.addChild(canvasBackground);
    }

    var background;
    if(options.background){
        var backgroundTexture =PIXI.Texture.fromImage(options.background);
        background = new PIXI.TilingSprite(backgroundTexture, gridWidth * tileSize, gridHeight * tileSize);
        background.anchor.x = 0.5;
        background.anchor.y = 0.5;
        background.position.x = canvas.width / 2;
        background.position.y = canvas.height / 2;
        stage.addChild(background);
    }

    var x0 = (canvas.width - gridWidth * tileSize + tileSize) / 2;
    var y0 = (canvas.height - gridHeight * tileSize + tileSize) / 2;

	stage.addChild(spriteContainer);

    var spriteTextures = {};
	for (var name in options.spritesUrl){
        spriteTextures[name]=PIXI.Texture.fromImage(options.spritesUrl[name]);
	}

	startAnimate=true;
	requestAnimFrame(animate);

    var resizeCanvas = function(width,height){
        tileSize = Math.min(width/(gridWidth+1),height/(gridHeight+1));
        if(canvasBackground){
            canvasBackground.height=height;
            canvasBackground.width=width;
        }
        if(background){
            background.height=gridHeight * tileSize;
            background.width=gridWidth * tileSize;
            background.position.x = width / 2;
            background.position.y = height / 2;
        }
        x0 = (canvas.width - gridWidth * tileSize + tileSize) / 2;
        y0 = (canvas.height - gridHeight * tileSize + tileSize) / 2;
        for(var sp in spriteContainer.children){
            var tileSprite=spriteContainer.children[sp];
            tileSprite.width = tileSize;
            tileSprite.height = tileSize;
            tileSprite.position.x = x0 + tileSprite.gridX * tileSize;
            tileSprite.position.y = y0 + tileSprite.gridY * tileSize;
        }
        renderer.resize(width,height);
    };

    var createTileSprite = function(texture, x, y) {
        var tileSprite = new PIXI.Sprite(texture);
        tileSprite.anchor.x = 0.5;
        tileSprite.anchor.y = 0.5;
        tileSprite.width = tileSize;
        tileSprite.height = tileSize;
        tileSprite.gridX=x;
        tileSprite.gridY=y;
        tileSprite.position.x = x0 + x * tileSize;
        tileSprite.position.y = y0 + y * tileSize;
        tileSprite.moveTo=function(x,y){
            this.gridX=x;
            this.gridY=y;
            this.position.x = x0 + x * tileSize;
            this.position.y = y0 + y * tileSize;
        }.bind(tileSprite);
        return tileSprite;
    };

    var resetCanvas = function(){
        spriteContainer.removeChildren();
    };


    var addSprite = function(name, x, y) {
        var sp=createTileSprite(spriteTextures[name], x, y);
        spriteContainer.addChild(sp);
        return sp;
    };

    var makeSprite = function(name, x, y) {
        return createTileSprite(spriteTextures[name], x, y);
    };

    var removeSprite = function(sprite) {
        spriteContainer.removeChild(sprite);
    };

    var removeAllSprites = function() {
        spriteContainer.removeChildren();
    };

    function animate() {

        renderer.render(stage);

        if(startAnimate) requestAnimFrame(animate);

    }

    if(Sk) (function(){
        var Sprite=Sk.misceval.buildClass({"__name__":"animation"},function($gbl, $loc){

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

            $loc.setTexture = new Sk.builtin.func(function (self,name) {
                self.name=name.v;
                self.sprite.setTexture(spriteTextures[self.name]);
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
        };
        goog.exportSymbol("Sk.builtin.removeAllSprites", Sk.builtin.removeAllSprites);
        Sk.builtins["removeAllSprites"]=Sk.builtin.removeAllSprites;

    })();
    return {createTileSprite:createTileSprite,
            resetCanvas:resetCanvas,
            addSprite:addSprite,
            makeSprite:makeSprite,
            removeSprite:removeSprite,
            removeAllSprites:removeAllSprites,
            stage:stage,
            spriteContainer:spriteContainer,
            resizeCanvas:resizeCanvas
        };
}
