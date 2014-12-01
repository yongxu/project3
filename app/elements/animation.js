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
        return tileSprite;
    }.bind(this);



    this.spriteTextures = {
 /*       'wall': PIXI.Texture.fromImage("../assets/crystal_wall02.png"),
        'teapot': PIXI.Texture.fromImage("../assets/magic_lamp.png"),
        'gold pile': PIXI.Texture.fromImage("../assets/gold_pile.png"),
        'apple': PIXI.Texture.fromImage("../assets/apple.png"),
        'coin': PIXI.Texture.fromImage("../assets/hud_coins.png"),
        'blue gem': PIXI.Texture.fromImage("../assets/hud_gem_blue.png"),
        'red gem': PIXI.Texture.fromImage("../assets/hud_gem_red.png"),
        'yellow gem': PIXI.Texture.fromImage("../assets/hud_gem_yellow.png"),
        'dragon': PIXI.Texture.fromImage("../assets/swamp_dragon.png"),
        'draco green': PIXI.Texture.fromImage("../assets/draco-base-green.png")*/
    };

    var loadSpriteTexture=this.loadSpriteTexture=function(name,url){
    	this.spriteTextures[name]=PIXI.Texture.fromImage(url);
    }.bind(this);

    var addSprite = this.addSprite = function(name, x, y) {
        spriteContainer.addChild(createTileSprite(this.spriteTextures[name], x, y));
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

    console.log(Sk);
}
