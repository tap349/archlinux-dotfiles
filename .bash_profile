#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

#---------------------------------------------------------------
# https://wiki.archlinux.org/index.php/Start_X_at_Login
#---------------------------------------------------------------

VT=$(fgconsole 2>/dev/null)
(( VT == 1 )) && startx -- vt$VT &> ~/logs/startx.log
unset VT

#---------------------------------------------------------------
# http://forum.xbmc.org/showthread.php?tid=139349&pid=1181646#pid1181646
#---------------------------------------------------------------

#if [ -z "$DISPLAY" ]
#then
#	startx
#fi

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*

