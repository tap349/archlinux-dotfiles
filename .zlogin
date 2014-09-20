#---------------------------------------------------------------
# https://wiki.archlinux.org/index.php/Start_X_at_Login
#---------------------------------------------------------------

VT=$(fgconsole 2>/dev/null)
(( VT == 1 )) && startx -- vt$VT &> ~/logs/startx.log
unset VT

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*

xmodmap ~/.Xmodmap 
