// Zeta base support
// --------------------

require("f/jquery.js");


(function($){
    
    // Zeta
    zeta = window.zeta = {

        blocks: {},

        history: [],

        el: {},

        start: function(context, selector) {

            context = context || document;

            selector = selector || '.zeta';

            $(context).find(selector).each(function(){

                var block = $(this),

                    params = this.onclick ? this.onclick() : {},

                    name = params.name || this.className.split(' ')[0] || '',

                    init = zeta.blocks[name];

                if (init && !block.data(name)) {

                    block
                        .data(name, true)
                        .addClass(name + '_js');

                    zeta.el[ name ] = zeta.el[ name ] || [];
                    zeta.el[ name ].push(block);
                    init.call(block, params);
                }

            });
        }
    };

    zeta.log = function(){
        zeta.history.push(arguments);
        if(window.console) window.console.log(Array.prototype.slice.call(arguments));
    };

    document.documentElement.className += 'js'

    $(document).ready(function(){ zeta.start() });

})(jQuery);
