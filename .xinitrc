xset r rate 200 30
xset m 2 4
xsetroot -cursor_name left_ptr

xbindkeys

sh ~/.fehbg &

# processes are killed after quitting i3
urxvtd >/dev/null 2>&1 &
#devmon --no-unmount >~/logs/devmon.log 2>&1 & 

[ -z "$(pidof urxvtd)" ] && urxvtd >/dev/null 2>&1 &                                                                                                                                                                                                                                                                       
#[ -z "$(pidof -x devmon)"] && devmon --no-unmount >~/logs/devmon.log 2>&1 & 

# cleanup
killall --signal 9 i3status-wrapper >/dev/null 2>&1

xmodmap ~/.Xmodmap

~/bin/cloud &

exec i3 >~/logs/i3.log 2>&1

