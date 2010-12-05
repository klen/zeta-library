// ==============================
// Zeta import: 'zetalibrary/zetalib/_.js'
// From: 'zetalibrary/zetalib/zeta.js'
window.log = function(){
  log.history = log.history || [];   
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};

(function(doc){
    
    var write = doc.write;
    doc.write = function(q){ 
        log('document.write(): ',arguments); 
        if (/docwriteregexwhitelist/.test(q)) write.apply(doc,arguments);  
    };
    
    doc.documentElement.className += 'js'
})(document);


// ==============================
// Zeta import: 'zetalibrary/zetalib/zeta.js'
// From: '/home/klen/Projects/github.com/zeta-library/tests/res/test.js'
( function( $ ){
    
    
    Zeta = window.Zeta = {

        blocks: {},

        blockInit: function( context, selector ) {

            context = context || document;

            selector = selector || '.zeta';

            $(context).find(selector).each(function(){

                var block = $(this),

                    params = this.onclick ? this.onclick() : {},

                    name = params.name || this.className.split(' ')[0] || '',

                    init = Zeta.blocks[name];

                if (init && !block.data(name)) {

                    block
                        .data(name, true)
                        .addClass(name + '_js');

                    init.call(block, params);

                }

            });
        }
    };

    $(document).ready(Zeta.blockInit);

} )( jQuery );


// ==============================
// Zeta import: '/home/klen/Projects/github.com/zeta-library/tests/res/test.js'
// From: 'None'
alert(1);


