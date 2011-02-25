(function( $, zeta ){

    zeta.blocks[ 'z-placeholder' ] = function( params ){

        var self = this,
            input = $('#' + self.attr('for')),
            hide = function(){ self.hide() },
            show = function(){ self.show() },
            check = function(){ focused || input.val() ? hide() : show() },
            focused = false;

        input
            .bind('focus blur', function(e){ focused = e.type == 'focus'; check() })
            .bind('change mouseover', check);

        self.click(function(){ input.focus() });

        input.change();

    };
    
})( jQuery, window.zeta );           

