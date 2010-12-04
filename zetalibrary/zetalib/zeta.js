// Zeta base support
// --------------------

require("jquery.js");
require("_.js");

( function( $ ){
    
    // Zeta
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
