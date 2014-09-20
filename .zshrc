# The following lines were added by compinstall

zstyle ':completion:*' completer _expand _complete _ignored _approximate
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' matcher-list '' '' '' 'r:|[._-]=* r:|=*'
zstyle :compinstall filename '/home/tap/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -v
# End of lines configured by zsh-newuser-install

#----------------------------------------------------------------------------------
#
# FROM ~/.bashrc
#
#----------------------------------------------------------------------------------

#======================================================
# ALIASES
#======================================================

alias df='df -h'
alias du='du -sh'
alias free='free -m'
alias ll='ls -al --color=auto'
alias ls='ls --color=auto'
alias mp='mplayer'
alias mp2='mplayer2'
alias mpxv='mplayer -vo xv'
alias q='gqview'
alias t='tmux'
alias y='yaourt'
alias yg='yaourt-gui'
alias yy='y -Syu --aur'

#------------------------------------------------------
# LVM

alias lv='sudo lvdisplay'
alias pv='sudo pvdisplay'
alias vg='sudo vgdisplay'

#------------------------------------------------------
# colour output of different commands
# http://muhas.ru/?p=54

if [ -f /usr/bin/grc ]; then
  alias diff="grc --colour=auto diff"
  alias make="grc --colour=auto make"
  alias netstat="grc --colour=auto netstat"
  alias ping="grc --colour=auto ping"
fi

PS1='[\u@\h \W]\$ '

#======================================================
# VARIABLES
#======================================================

#------------------------------------------------------
# PATH

[[ -d ~/bin ]] && PATH=~/bin:"${PATH}"
[[ -d ~/scripts ]] && PATH=~/scripts:"${PATH}"

export PATH

#------------------------------------------------------
# CDPATH

export CDPATH=~

#------------------------------------------------------
# INPUTRC

export INPUTRC=~/.inputrc

#------------------------------------------------------
# colour less output (including man)
# http://muhas.ru/?p=181

export LESS_TERMCAP_mb=$'\E[01;31m'       # начала мигающего
export LESS_TERMCAP_md=$'\E[01;38;5;74m'  # начало жирного текста
export LESS_TERMCAP_me=$'\E[0m'           # окончание
export LESS_TERMCAP_so=$'\E[38;5;246m'    # начала текста в инфобоксе
export LESS_TERMCAP_se=$'\E[0m'           # конец его
export LESS_TERMCAP_us=$'\E[04;38;5;146m' # начало подчеркнутого
export LESS_TERMCAP_ue=$'\E[0m'           # конец подчеркнутого


PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting

