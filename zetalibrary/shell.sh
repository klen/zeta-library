if [ -n "$BASH" ] ; then
    _zeta_comp () {
        COMPREPLY=( $( \
            COMP_WORDS="${COMP_WORDS[*]}" \
            COMP_CWORD=$COMP_CWORD \
            ARGH_AUTO_COMPLETE=1 $1 ) ) 
    }
    complete -o default -F _zeta_comp zeta
fi
